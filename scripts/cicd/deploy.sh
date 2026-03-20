#!/bin/bash
# 배포 실행 스크립트
# Usage: ./deploy.sh <app_name> <version> [environment]

set -euo pipefail

APP_NAME="${1:?Usage: $0 <app_name> <version> [environment]}"
VERSION="${2:?Usage: $0 <app_name> <version> [environment]}"
ENVIRONMENT="${3:-dev}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEPLOY_ID="$(date +%Y%m%d%H%M%S)"
LOG_FILE="$PROJECT_ROOT/logs/deploy/deploy-${DEPLOY_ID}.log"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    local msg="$(date '+%Y-%m-%d %H:%M:%S') $*"
    echo -e "$msg"
    echo "$msg" >> "$LOG_FILE"
}

# 배포 이력을 DB에 기록
record_deployment() {
    local status="$1"
    python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from db.db_manager import DBManager
db = DBManager()
db.create_deployment('$APP_NAME', '${APP_NAME}:${VERSION}', '$VERSION', 1, '$ENVIRONMENT')
" 2>/dev/null || true
}

echo ""
echo "=========================================="
echo "  Deployment"
echo "=========================================="
echo "  App:         $APP_NAME"
echo "  Version:     $VERSION"
echo "  Environment: $ENVIRONMENT"
echo "  Deploy ID:   $DEPLOY_ID"
echo "=========================================="
echo ""

# Pre-deploy 체크
log "${BLUE}[Pre-Deploy]${NC} Checking prerequisites..."

IMAGE_TAG="${APP_NAME}:${VERSION}"

if command -v docker &> /dev/null; then
    if docker image inspect "$IMAGE_TAG" &> /dev/null; then
        log "${GREEN}[OK]${NC} Image found: $IMAGE_TAG"
    else
        log "${RED}[ERROR]${NC} Image not found: $IMAGE_TAG"
        log "Run build.sh first: ./scripts/cicd/build.sh $APP_NAME $VERSION"
        exit 1
    fi
else
    log "${YELLOW}[WARN]${NC} Docker not available"
fi

# 기존 컨테이너 확인
EXISTING=$(docker ps -a --filter "name=${APP_NAME}" --format "{{.Names}}" 2>/dev/null || true)
if [ -n "$EXISTING" ]; then
    log "${YELLOW}[INFO]${NC} Existing containers found, performing rolling update..."

    for container in $EXISTING; do
        log "  Stopping: $container"
        docker stop "$container" --time 10 2>/dev/null || true
        docker rm "$container" 2>/dev/null || true
    done

    log "${GREEN}[OK]${NC} Old containers removed"
fi

# 배포 실행
log "${BLUE}[Deploy]${NC} Starting deployment..."

# 서비스 정의 파일에서 설정 읽기
SERVICE_CONFIG="$PROJECT_ROOT/configs/examples/service.yaml"
if [ -f "$SERVICE_CONFIG" ]; then
    log "  Using service config: $SERVICE_CONFIG"
    python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from orchestrator.engine import OrchestrationEngine
from db.db_manager import DBManager
db = DBManager()
db.init()
engine = OrchestrationEngine(db_manager=db)
deployed = engine.deploy('$SERVICE_CONFIG')
print(f'Deployed: {deployed}')
" 2>&1 | tee -a "$LOG_FILE"
else
    # 기본 배포
    log "  Deploying with defaults..."
    docker run -d \
        --name "$APP_NAME" \
        --label "orchestrator.managed=true" \
        --label "orchestrator.service=$APP_NAME" \
        --restart unless-stopped \
        "$IMAGE_TAG" 2>&1 | tee -a "$LOG_FILE"
fi

# Post-deploy 헬스체크
log "${BLUE}[Post-Deploy]${NC} Running health check..."
sleep 5

if docker ps --filter "name=${APP_NAME}" --filter "status=running" --format "{{.Names}}" | grep -q "$APP_NAME"; then
    log "${GREEN}[OK]${NC} Container is running"
    record_deployment "deployed"
else
    log "${RED}[FAIL]${NC} Container is not running"
    log "Rolling back..."
    "$SCRIPT_DIR/rollback.sh" "$APP_NAME" "$ENVIRONMENT"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "  ${GREEN}Deployment Completed${NC}"
echo "  Container: $APP_NAME"
echo "  Image: $IMAGE_TAG"
echo "  Environment: $ENVIRONMENT"
echo "=========================================="
