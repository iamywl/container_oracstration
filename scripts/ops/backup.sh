#!/bin/bash
# 데이터베이스 및 설정 백업 스크립트
# Usage: ./backup.sh [backup_dir]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BACKUP_BASE="${1:-$PROJECT_ROOT/data/backups}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$BACKUP_BASE/$TIMESTAMP"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[Backup] Starting backup...${NC}"

mkdir -p "$BACKUP_DIR"

# DB 백업
if [ -f "$PROJECT_ROOT/db/platform.db" ]; then
    sqlite3 "$PROJECT_ROOT/db/platform.db" ".backup '$BACKUP_DIR/platform.db'"
    echo "  DB backed up: platform.db"
fi

# 설정 파일 백업
if [ -d "$PROJECT_ROOT/configs" ]; then
    cp -r "$PROJECT_ROOT/configs" "$BACKUP_DIR/configs"
    echo "  Configs backed up"
fi

# 컨테이너 상태 스냅샷
if command -v docker &> /dev/null; then
    docker ps -a --filter "label=orchestrator.managed=true" \
        --format "{{.Names}}\t{{.Image}}\t{{.Status}}" \
        > "$BACKUP_DIR/container_snapshot.txt" 2>/dev/null || true
    echo "  Container snapshot saved"
fi

# 백업 메타데이터
cat > "$BACKUP_DIR/backup-info.json" << EOF
{
    "timestamp": "$TIMESTAMP",
    "backup_dir": "$BACKUP_DIR",
    "hostname": "$(hostname)",
    "git_commit": "$(cd "$PROJECT_ROOT" && git rev-parse HEAD 2>/dev/null || echo 'unknown')"
}
EOF

# 오래된 백업 정리 (7일 이상)
find "$BACKUP_BASE" -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null || true

echo -e "${GREEN}[Backup] Completed: $BACKUP_DIR${NC}"
