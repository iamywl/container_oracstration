#!/bin/bash
# CI/CD 빌드 파이프라인
# Usage: ./build.sh <app_name> <version> [environment]

set -euo pipefail

APP_NAME="${1:?Usage: $0 <app_name> <version> [environment]}"
VERSION="${2:?Usage: $0 <app_name> <version> [environment]}"
ENVIRONMENT="${3:-dev}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"
LOG_DIR="$PROJECT_ROOT/logs/cicd"
PIPELINE_ID="$(date +%Y%m%d%H%M%S)-$(head -c 4 /dev/urandom | xxd -p)"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    local level="$1"
    shift
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${timestamp} [${level}] $*"
    echo "${timestamp} [${level}] $*" >> "$LOG_DIR/build-${PIPELINE_ID}.log"
}

info()  { log "${BLUE}INFO${NC}" "$@"; }
warn()  { log "${YELLOW}WARN${NC}" "$@"; }
error() { log "${RED}ERROR${NC}" "$@"; }
success() { log "${GREEN}OK${NC}" "$@"; }

# 파이프라인 상태를 DB에 기록
record_pipeline() {
    local stage="$1"
    local status="$2"
    python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from db.db_manager import DBManager
db = DBManager()
db.create_pipeline_run('$PIPELINE_ID', '$APP_NAME', '$VERSION', '$stage')
" 2>/dev/null || true
}

# 초기화
mkdir -p "$BUILD_DIR" "$LOG_DIR"

echo ""
echo "=========================================="
echo "  CI/CD Build Pipeline"
echo "=========================================="
echo "  App:         $APP_NAME"
echo "  Version:     $VERSION"
echo "  Environment: $ENVIRONMENT"
echo "  Pipeline ID: $PIPELINE_ID"
echo "=========================================="
echo ""

# Stage 1: 소스 검증
info "Stage 1/4: Source Validation"
record_pipeline "validate" "running"

if [ ! -f "$PROJECT_ROOT/configs/examples/service.yaml" ]; then
    warn "Service definition not found, using defaults"
fi

# Dockerfile 존재 여부 확인
DOCKERFILE="$PROJECT_ROOT/Dockerfile"
if [ -f "$DOCKERFILE" ]; then
    info "Dockerfile found"
else
    info "Dockerfile not found - creating default"
    cat > "$BUILD_DIR/Dockerfile.generated" << 'DOCKERFILE_CONTENT'
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

CMD ["python", "-m", "orchestrator.cli", "daemon"]
DOCKERFILE_CONTENT
    DOCKERFILE="$BUILD_DIR/Dockerfile.generated"
fi

success "Source validation passed"

# Stage 2: 테스트 실행
info "Stage 2/4: Running Tests"
record_pipeline "test" "running"

if [ -d "$PROJECT_ROOT/tests" ]; then
    cd "$PROJECT_ROOT"
    if python3 -m pytest tests/ -v --tb=short 2>&1 | tee -a "$LOG_DIR/build-${PIPELINE_ID}.log"; then
        success "All tests passed"
    else
        error "Tests failed"
        record_pipeline "test" "failed"
        exit 1
    fi
else
    warn "No tests directory found, skipping"
fi

# Stage 3: Docker 이미지 빌드
info "Stage 3/4: Building Docker Image"
record_pipeline "build" "running"

IMAGE_TAG="${APP_NAME}:${VERSION}"
IMAGE_LATEST="${APP_NAME}:latest"

if command -v docker &> /dev/null; then
    cd "$PROJECT_ROOT"
    if docker build -t "$IMAGE_TAG" -t "$IMAGE_LATEST" -f "$DOCKERFILE" . 2>&1 | tee -a "$LOG_DIR/build-${PIPELINE_ID}.log"; then
        success "Docker image built: $IMAGE_TAG"
        docker images "$APP_NAME" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | head -5
    else
        error "Docker build failed"
        record_pipeline "build" "failed"
        exit 1
    fi
else
    warn "Docker not available - skipping image build"
fi

# Stage 4: 아티팩트 저장
info "Stage 4/4: Saving Artifacts"
record_pipeline "artifacts" "running"

ARTIFACT_DIR="$BUILD_DIR/$APP_NAME/$VERSION"
mkdir -p "$ARTIFACT_DIR"

# 빌드 메타데이터 저장
cat > "$ARTIFACT_DIR/build-info.json" << EOF
{
    "app_name": "$APP_NAME",
    "version": "$VERSION",
    "environment": "$ENVIRONMENT",
    "pipeline_id": "$PIPELINE_ID",
    "image_tag": "$IMAGE_TAG",
    "build_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "git_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"
}
EOF

success "Build artifacts saved to $ARTIFACT_DIR"

# 완료
echo ""
echo "=========================================="
echo -e "  ${GREEN}Build Pipeline Completed${NC}"
echo "  Image: $IMAGE_TAG"
echo "  Pipeline ID: $PIPELINE_ID"
echo "=========================================="

record_pipeline "complete" "success"
