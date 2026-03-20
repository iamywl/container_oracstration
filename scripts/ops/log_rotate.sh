#!/bin/bash
# 로그 로테이션 스크립트
# Usage: ./log_rotate.sh [days_to_keep]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/logs"
DAYS_TO_KEEP="${1:-30}"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[Log Rotate] Starting...${NC}"

if [ ! -d "$LOG_DIR" ]; then
    echo "  No log directory found"
    exit 0
fi

# 오래된 로그 압축
COMPRESSED=0
find "$LOG_DIR" -name "*.log" -mtime +1 -not -name "*.gz" | while read -r logfile; do
    gzip "$logfile"
    COMPRESSED=$((COMPRESSED + 1))
done
echo "  Compressed: $COMPRESSED log file(s)"

# 보관 기간 초과 로그 삭제
DELETED=$(find "$LOG_DIR" -name "*.log.gz" -mtime +"$DAYS_TO_KEEP" -delete -print | wc -l)
echo "  Deleted: $DELETED old log file(s) (>${DAYS_TO_KEEP} days)"

# DB 메트릭 정리
python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from db.db_manager import DBManager
db = DBManager()
db.cleanup_old_metrics(days=$DAYS_TO_KEEP)
" 2>/dev/null && echo "  Old metrics cleaned from DB" || true

echo -e "${GREEN}[Log Rotate] Completed${NC}"
