#!/bin/bash
# 플랫폼 초기 환경 설정 스크립트
# Usage: ./setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "=========================================="
echo "  Container Platform Setup"
echo "=========================================="
echo ""

# 1. 필수 도구 확인
echo -e "${BLUE}[1/5] Checking prerequisites...${NC}"

check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "  ${GREEN}✓${NC} $1 $(command -v "$1")"
        return 0
    else
        echo -e "  ${RED}✗${NC} $1 not found"
        return 1
    fi
}

MISSING=0
check_command "docker" || MISSING=$((MISSING + 1))
check_command "python3" || MISSING=$((MISSING + 1))
check_command "java" || MISSING=$((MISSING + 1))
check_command "sqlite3" || MISSING=$((MISSING + 1))

if [ "$MISSING" -gt 0 ]; then
    echo -e "\n${YELLOW}[WARN] $MISSING tool(s) missing. Some features may not work.${NC}"
fi

# 2. Docker 상태 확인
echo -e "\n${BLUE}[2/5] Checking Docker...${NC}"
if docker info &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Docker daemon is running"
    DOCKER_VERSION=$(docker version --format '{{.Server.Version}}' 2>/dev/null || echo "unknown")
    echo -e "  ${GREEN}✓${NC} Docker version: $DOCKER_VERSION"
else
    echo -e "  ${RED}✗${NC} Docker daemon is not running"
    echo "  Please start Docker and re-run this script"
fi

# 3. 디렉토리 구조 생성
echo -e "\n${BLUE}[3/5] Creating directories...${NC}"
DIRS=(
    "logs/cicd"
    "logs/deploy"
    "logs/monitoring"
    "build"
    "data"
    "db/migrations"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$PROJECT_ROOT/$dir"
    echo "  Created: $dir/"
done

# 4. Python 의존성 설치
echo -e "\n${BLUE}[4/5] Installing Python dependencies...${NC}"
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    cd "$PROJECT_ROOT"
    if python3 -m pip install -r requirements.txt --quiet 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Python dependencies installed"
    else
        echo -e "  ${YELLOW}!${NC} pip install failed - try: pip install -r requirements.txt"
    fi
fi

# 5. 데이터베이스 초기화
echo -e "\n${BLUE}[5/5] Initializing database...${NC}"
cd "$PROJECT_ROOT"
if python3 -c "
import sys
sys.path.insert(0, '.')
from db.db_manager import DBManager
db = DBManager()
db.init()
print('OK')
" 2>/dev/null | grep -q "OK"; then
    echo -e "  ${GREEN}✓${NC} Database initialized: db/platform.db"
else
    # fallback: sqlite3 직접 사용
    if command -v sqlite3 &> /dev/null && [ -f "$PROJECT_ROOT/db/schema.sql" ]; then
        sqlite3 "$PROJECT_ROOT/db/platform.db" < "$PROJECT_ROOT/db/schema.sql"
        echo -e "  ${GREEN}✓${NC} Database initialized via sqlite3"
    else
        echo -e "  ${RED}✗${NC} Database initialization failed"
    fi
fi

# .gitignore 설정
echo -e "\n${BLUE}[+] Updating .gitignore...${NC}"
cat > "$PROJECT_ROOT/.gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
dist/

# Java
*.class
api/build/
api/.gradle/
api/bin/

# Database
db/*.db
db/*.db-shm
db/*.db-wal

# Logs & Build
logs/
build/
data/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
EOF
echo -e "  ${GREEN}✓${NC} .gitignore updated"

echo ""
echo "=========================================="
echo -e "  ${GREEN}Setup Completed${NC}"
echo ""
echo "  Next steps:"
echo "    1. python -m orchestrator.cli deploy configs/examples/service.yaml"
echo "    2. python -m orchestrator.cli list"
echo "    3. python -m monitoring.dashboard"
echo "=========================================="
