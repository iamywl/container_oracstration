.PHONY: setup test build deploy clean help

# 변수
APP_NAME ?= platform
VERSION ?= latest
ENV ?= dev

help: ## 사용 가능한 명령어 목록
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## 플랫폼 초기 환경 설정
	@chmod +x scripts/**/*.sh
	@./scripts/deploy/setup.sh

test: ## 전체 테스트 실행
	python3 -m pytest tests/ -v --tb=short

test-db: ## DB 테스트만 실행
	python3 -m pytest tests/test_db.py -v

test-monitoring: ## 모니터링 테스트만 실행
	python3 -m pytest tests/test_monitoring.py -v

build: ## Docker 이미지 빌드
	@./scripts/cicd/build.sh $(APP_NAME) $(VERSION) $(ENV)

deploy: ## 서비스 배포
	@./scripts/cicd/deploy.sh $(APP_NAME) $(VERSION) $(ENV)

rollback: ## 마지막 배포 롤백
	@./scripts/cicd/rollback.sh $(APP_NAME) $(ENV)

# 컨테이너 관리
list: ## 관리 중인 컨테이너 목록
	python3 -m orchestrator.cli list

health: ## 헬스체크 실행
	python3 -m orchestrator.cli health

scale: ## 서비스 스케일링 (make scale SERVICE=nginx REPLICAS=3)
	python3 -m orchestrator.cli scale $(SERVICE) --replicas=$(REPLICAS)

logs: ## 컨테이너 로그 (make logs CONTAINER=nginx-0)
	python3 -m orchestrator.cli logs $(CONTAINER)

stats: ## 컨테이너 리소스 현황 (make stats CONTAINER=nginx-0)
	python3 -m orchestrator.cli stats $(CONTAINER)

# 모니터링
dashboard: ## 모니터링 대시보드 실행
	python3 -m monitoring.dashboard

daemon: ## 오케스트레이션 데몬 시작 (헬스체크 + 오토스케일러)
	python3 -m orchestrator.cli daemon

# API 서버
api: ## Java API 서버 실행
	cd api && ./gradlew bootRun

# MCP
mcp: ## MCP 서버 실행
	python3 -m mcp_server.server

# 운영
backup: ## 데이터 백업
	@./scripts/ops/backup.sh

log-rotate: ## 로그 로테이션
	@./scripts/ops/log_rotate.sh

# DB
db-init: ## 데이터베이스 초기화
	python3 db/db_manager.py init

# 정리
clean: ## 환경 정리
	@./scripts/deploy/teardown.sh

clean-force: ## 강제 환경 정리 (DB 포함)
	@./scripts/deploy/teardown.sh --force
