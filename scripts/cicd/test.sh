#!/bin/bash
# 테스트 실행 스크립트
# Usage: ./test.sh [test_path]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_PATH="${1:-tests/}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  Running Tests"
echo "=========================================="
echo ""

cd "$PROJECT_ROOT"

# Python 테스트
if [ -d "$PROJECT_ROOT/tests" ]; then
    echo -e "${YELLOW}[Python Tests]${NC}"
    if python3 -m pytest "$TEST_PATH" -v --tb=short; then
        echo -e "${GREEN}Python tests passed${NC}"
    else
        echo -e "${RED}Python tests failed${NC}"
        exit 1
    fi
    echo ""
fi

# Java 테스트
if [ -f "$PROJECT_ROOT/api/build.gradle" ]; then
    echo -e "${YELLOW}[Java Tests]${NC}"
    cd "$PROJECT_ROOT/api"
    if [ -f "./gradlew" ]; then
        if ./gradlew test --quiet; then
            echo -e "${GREEN}Java tests passed${NC}"
        else
            echo -e "${RED}Java tests failed${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Gradle wrapper not found, skipping Java tests${NC}"
    fi
    cd "$PROJECT_ROOT"
    echo ""
fi

# Shell Script 문법 검사
echo -e "${YELLOW}[Shell Script Lint]${NC}"
SHELL_ERRORS=0
for script in scripts/**/*.sh; do
    if [ -f "$script" ]; then
        if bash -n "$script" 2>/dev/null; then
            echo "  OK: $script"
        else
            echo -e "  ${RED}FAIL: $script${NC}"
            SHELL_ERRORS=$((SHELL_ERRORS + 1))
        fi
    fi
done

if [ "$SHELL_ERRORS" -gt 0 ]; then
    echo -e "${RED}Shell script lint: $SHELL_ERRORS error(s)${NC}"
    exit 1
else
    echo -e "${GREEN}Shell script lint passed${NC}"
fi

echo ""
echo "=========================================="
echo -e "  ${GREEN}All Tests Passed${NC}"
echo "=========================================="
