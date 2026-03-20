# Container Orchestration Platform

연구소 환경을 위한 컨테이너 플랫폼 개발/운영 도구

컨테이너 오케스트레이션, CI/CD 파이프라인, 모니터링 시스템을 통합 제공하는 플랫폼 엔지니어링 프로젝트

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Agent (AI Ops)                    │
│              AI 기반 컨테이너 운영 자동화                   │
├─────────────────────────────────────────────────────────┤
│                  Java REST API Server                    │
│         플랫폼 관리 API / 대시보드 엔드포인트               │
├──────────┬──────────────────┬───────────────────────────┤
│Container │   CI/CD Pipeline │   Monitoring System       │
│Orchestr. │                  │                           │
│(Python)  │  (Shell Script)  │   (Python)                │
│          │                  │                           │
│- 배포    │  - Build         │  - Metrics 수집           │
│- 스케일링│  - Test          │  - Health Check           │
│- 헬스체크│  - Deploy        │  - Alert                  │
│- 자동복구│  - Rollback      │  - 로그 수집              │
├──────────┴──────────────────┴───────────────────────────┤
│                   SQLite Database                        │
│     컨테이너 상태 / 배포 이력 / 메트릭 / 파이프라인 이력    │
├─────────────────────────────────────────────────────────┤
│                   Docker Engine                          │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

| 기술 | 용도 |
|------|------|
| **Python** | 컨테이너 오케스트레이션 엔진, 모니터링 시스템, MCP 서버 |
| **Java** | REST API 서버 (플랫폼 관리 API) |
| **Shell Script** | CI/CD 파이프라인, 배포 자동화, 운영 스크립트 |
| **SQL (SQLite)** | 컨테이너 상태, 배포 이력, 메트릭, 파이프라인 이력 저장 |
| **MCP/Agent** | AI 기반 컨테이너 운영 자동화 (Model Context Protocol) |

## Project Structure

```
container_orchestration/
├── orchestrator/           # Python 컨테이너 오케스트레이션 엔진
│   ├── engine.py           #   오케스트레이션 코어 엔진
│   ├── container.py        #   컨테이너 라이프사이클 관리
│   ├── health_checker.py   #   헬스체크 및 자동 복구
│   ├── scaler.py           #   오토 스케일링
│   └── cli.py              #   CLI 인터페이스
│
├── monitoring/             # Python 모니터링 시스템
│   ├── collector.py        #   메트릭 수집기
│   ├── dashboard.py        #   메트릭 대시보드 (터미널 UI)
│   └── alerting/
│       └── alert_manager.py#   알림 매니저
│
├── api/                    # Java REST API 서버
│   └── src/main/java/com/platform/
│       ├── PlatformApplication.java
│       ├── controller/
│       │   ├── ContainerController.java
│       │   ├── PipelineController.java
│       │   └── MonitoringController.java
│       ├── service/
│       │   ├── ContainerService.java
│       │   ├── PipelineService.java
│       │   └── MonitoringService.java
│       └── model/
│           ├── Container.java
│           ├── Pipeline.java
│           └── Metric.java
│
├── scripts/                # Shell Script 자동화
│   ├── cicd/
│   │   ├── build.sh        #   빌드 파이프라인
│   │   ├── test.sh         #   테스트 실행
│   │   ├── deploy.sh       #   배포 실행
│   │   └── rollback.sh     #   롤백 처리
│   ├── deploy/
│   │   ├── setup.sh        #   환경 초기 설정
│   │   └── teardown.sh     #   환경 정리
│   └── ops/
│       ├── backup.sh       #   백업 스크립트
│       └── log_rotate.sh   #   로그 로테이션
│
├── db/                     # SQL 스키마 및 마이그레이션
│   ├── schema.sql          #   전체 스키마
│   ├── migrations/         #   마이그레이션 파일
│   └── db_manager.py       #   DB 매니저
│
├── mcp_server/             # MCP Server (AI 기반 운영)
│   ├── server.py           #   MCP 서버
│   └── tools.py            #   MCP 도구 정의
│
├── configs/                # 설정 파일
│   ├── platform.yaml       #   플랫폼 설정
│   └── examples/
│       └── service.yaml    #   서비스 정의 예시
│
├── tests/                  # 테스트
│   ├── test_orchestrator.py
│   ├── test_monitoring.py
│   └── test_db.py
│
├── requirements.txt
├── Makefile
└── README.md
```

## Features

### 1. Container Orchestration (Python)
- Docker SDK를 활용한 컨테이너 라이프사이클 관리 (생성/시작/중지/삭제)
- YAML 기반 서비스 정의 및 멀티 컨테이너 배포
- 헬스체크 기반 자동 복구 (Self-Healing)
- 컨테이너 오토 스케일링 (CPU/메모리 기반)
- 롤링 업데이트 및 롤백

### 2. CI/CD Pipeline (Shell Script)
- 빌드 → 테스트 → 배포 자동화 파이프라인
- 단계별 실행 및 실패 시 자동 롤백
- 배포 이력 관리 및 원클릭 롤백
- 환경별 배포 지원 (dev/staging/prod)

### 3. Monitoring System (Python)
- 실시간 컨테이너 메트릭 수집 (CPU, Memory, Network, Disk)
- 임계치 기반 알림 시스템 (Slack, Email 연동)
- 터미널 기반 실시간 대시보드
- 메트릭 이력 저장 및 트렌드 분석 (SQL)

### 4. AI Operations - MCP Agent
- Model Context Protocol 기반 AI 운영 에이전트
- 자연어 명령으로 컨테이너 관리 ("nginx 3개로 스케일 아웃해줘")
- 장애 자동 분석 및 복구 제안
- 운영 이력 기반 최적화 추천

## Quick Start

### Prerequisites
- Docker Engine
- Python 3.10+
- Java 17+
- SQLite3

### Installation
```bash
# 환경 설정
./scripts/deploy/setup.sh

# Python 의존성 설치
pip install -r requirements.txt

# DB 초기화
python db/db_manager.py init
```

### Usage

```bash
# 서비스 배포
python -m orchestrator.cli deploy configs/examples/service.yaml

# 컨테이너 목록 조회
python -m orchestrator.cli list

# 헬스체크 실행
python -m orchestrator.cli health

# 스케일링
python -m orchestrator.cli scale nginx --replicas=3

# 모니터링 대시보드
python -m monitoring.dashboard

# CI/CD 파이프라인 실행
./scripts/cicd/build.sh myapp v1.0.0

# API 서버 실행
cd api && ./gradlew bootRun

# MCP 서버 실행
python -m mcp_server.server
```

## CI/CD Pipeline Flow

```
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐
│  Build  │───▶│  Test   │───▶│  Deploy  │───▶│  Verify  │
│         │    │         │    │          │    │          │
│ build.sh│    │ test.sh │    │deploy.sh │    │health.py │
└─────────┘    └─────────┘    └──────────┘    └──────────┘
                                                   │
                                              ┌────▼─────┐
                                              │ Rollback │
                                              │(on fail) │
                                              └──────────┘
```

## Monitoring Architecture

```
Container ──▶ Collector ──▶ SQLite ──▶ Dashboard
                │                        │
                ▼                        ▼
          Alert Manager           Trend Analysis
                │
                ▼
         Slack / Email
```
