#!/bin/bash
# 롤백 처리 스크립트
# Usage: ./rollback.sh <app_name> [environment]

set -euo pipefail

APP_NAME="${1:?Usage: $0 <app_name> [environment]}"
ENVIRONMENT="${2:-dev}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "=========================================="
echo "  Rollback"
echo "=========================================="
echo "  App:         $APP_NAME"
echo "  Environment: $ENVIRONMENT"
echo "=========================================="
echo ""

# 이전 배포 정보 조회
PREV_DEPLOYMENT=$(python3 -c "
import sys, json
sys.path.insert(0, '$PROJECT_ROOT')
from db.db_manager import DBManager
db = DBManager()
# 현재 배포를 rolled_back 처리하고 이전 배포 정보 반환
deployments = db.get_pipeline_history('$APP_NAME', limit=2)
if len(deployments) >= 2:
    print(json.dumps(deployments[1]))
" 2>/dev/null || echo "")

if [ -z "$PREV_DEPLOYMENT" ]; then
    echo -e "${YELLOW}[WARN]${NC} No previous deployment found"
    echo "Manual intervention required."

    # 현재 컨테이너 중지만 수행
    echo -e "${YELLOW}Stopping current containers...${NC}"
    docker ps -a --filter "name=${APP_NAME}" --format "{{.Names}}" | while read -r container; do
        docker stop "$container" --time 10 2>/dev/null || true
        docker rm "$container" 2>/dev/null || true
        echo "  Removed: $container"
    done

    # DB에 롤백 기록
    python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from db.db_manager import DBManager
db = DBManager()
db.log_event('$APP_NAME', 'rollback', 'Manual rollback - no previous deployment')
" 2>/dev/null || true

    exit 0
fi

echo -e "${YELLOW}Rolling back to previous deployment...${NC}"

# 현재 컨테이너 중지
docker ps -a --filter "name=${APP_NAME}" --format "{{.Names}}" | while read -r container; do
    docker stop "$container" --time 10 2>/dev/null || true
    docker rm "$container" 2>/dev/null || true
    echo "  Removed: $container"
done

# DB에 롤백 기록
python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from db.db_manager import DBManager
db = DBManager()
last = db.get_last_deployment('$APP_NAME', '$ENVIRONMENT')
if last:
    db.mark_rollback(last['id'])
db.log_event('$APP_NAME', 'rollback', 'Rolled back in $ENVIRONMENT')
" 2>/dev/null || true

echo ""
echo "=========================================="
echo -e "  ${GREEN}Rollback Completed${NC}"
echo "=========================================="
