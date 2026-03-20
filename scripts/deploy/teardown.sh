#!/bin/bash
# 환경 정리 스크립트
# Usage: ./teardown.sh [--force]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FORCE="${1:-}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "=========================================="
echo "  Platform Teardown"
echo "=========================================="
echo ""

if [ "$FORCE" != "--force" ]; then
    echo -e "${YELLOW}This will stop all managed containers and clean up data.${NC}"
    read -p "Continue? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Aborted."
        exit 0
    fi
fi

# 관리 중인 컨테이너 중지 및 제거
echo -e "${YELLOW}[1/3] Stopping managed containers...${NC}"
CONTAINERS=$(docker ps -a --filter "label=orchestrator.managed=true" --format "{{.Names}}" 2>/dev/null || true)

if [ -n "$CONTAINERS" ]; then
    for container in $CONTAINERS; do
        docker stop "$container" --time 10 2>/dev/null || true
        docker rm "$container" 2>/dev/null || true
        echo "  Removed: $container"
    done
    echo -e "${GREEN}All managed containers removed${NC}"
else
    echo "  No managed containers found"
fi

# 빌드 아티팩트 정리
echo -e "\n${YELLOW}[2/3] Cleaning build artifacts...${NC}"
rm -rf "$PROJECT_ROOT/build"
rm -rf "$PROJECT_ROOT/logs"
echo "  Build artifacts cleaned"

# DB 정리 (선택적)
echo -e "\n${YELLOW}[3/3] Database cleanup...${NC}"
if [ "$FORCE" = "--force" ]; then
    rm -f "$PROJECT_ROOT/db/platform.db"
    rm -f "$PROJECT_ROOT/db/platform.db-shm"
    rm -f "$PROJECT_ROOT/db/platform.db-wal"
    echo "  Database removed"
else
    echo "  Database preserved (use --force to remove)"
fi

echo ""
echo "=========================================="
echo -e "  ${GREEN}Teardown Completed${NC}"
echo "=========================================="
