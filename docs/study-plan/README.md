# 학습 계획서

> Container Orchestration Platform 전체를 이해하기 위한 단계별 학습 계획
> 각 항목에 관련 문서, 코드, 논문 링크를 포함하여 바로 공부할 수 있도록 구성

---

## 학습 로드맵 (전체 4주)

```
Week 1: 기초 (Docker + Python 오케스트레이션)
Week 2: 운영 (CI/CD + 모니터링 + Shell Script)
Week 3: 심화 (Java API + SQL + 오토스케일링)
Week 4: AI Ops (MCP + Agent + 논문 리뷰)
```

---

## Week 1: Container Orchestration 기초

### Day 1-2: Docker 기초 및 Container Manager 이해

**학습 목표:** Docker SDK로 컨테이너를 프로그래밍 방식으로 관리하는 원리 이해

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | 전체 아키텍처 파악 | [시스템 아키텍처 문서](../architecture/overview.md) |
| 2 | Docker SDK 기반 컨테이너 관리 코드 분석 | [orchestrator/container.py](../../orchestrator/container.py) |
| 3 | ContainerConfig, 레이블 관리, 메트릭 수집 계산식 | [컴포넌트 상세 문서 §1](../guides/component-details.md) |
| 4 | 서비스 정의 YAML 구조 | [configs/examples/service.yaml](../../configs/examples/service.yaml) |
| 5 | (논문) Google Borg — K8s의 직접적 전신 | [Borg, EuroSys 2015](https://dl.acm.org/doi/10.1145/2741948.2741964) |
| 6 | (논문) Borg→Omega→K8s 10년 교훈 | [ACM Queue 2016](https://queue.acm.org/detail.cfm?id=2898444) |

**실습:**
```bash
python -m orchestrator.cli deploy configs/examples/service.yaml
python -m orchestrator.cli list
python -m orchestrator.cli stats nginx-0
```

---

### Day 3-4: 헬스체크 및 Self-Healing

**학습 목표:** 자동 장애 감지 → 복구 메커니즘의 동작 원리 이해

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | 헬스체크 3가지 방식(status/http/tcp) 코드 분석 | [orchestrator/health_checker.py](../../orchestrator/health_checker.py) |
| 2 | 장애 판정 로직 (failure_count, retries) | [컴포넌트 상세 문서 §2](../guides/component-details.md) |
| 3 | 오케스트레이션 엔진 통합 흐름 | [orchestrator/engine.py](../../orchestrator/engine.py) |
| 4 | (논문) 마이크로서비스 장애 진단 서베이 (98편 분석) | [ACM TOSEM 2025](https://dl.acm.org/doi/10.1145/3715005) |
| 5 | (논문) Netflix 카오스 엔지니어링 자동화 | [ICSE-SEIP 2019](https://dl.acm.org/doi/10.1109/ICSE-SEIP.2019.00012) |
| 6 | Self-Healing 논문 전체 리뷰 | [research/self_healing/](../../research/self_healing/README.md) |

**실습:**
```bash
python -m orchestrator.cli daemon  # 데몬 시작 후 컨테이너를 수동으로 죽여보기
docker stop nginx-0                # 자동 재시작 확인
```

---

### Day 5: 오토 스케일링

**학습 목표:** CPU/메모리 기반 자동 스케일링 알고리즘 이해

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | ScalingPolicy, AutoScaler 코드 분석 | [orchestrator/scaler.py](../../orchestrator/scaler.py) |
| 2 | 스케일링 판단 기준 (임계치, cooldown) | [컴포넌트 상세 문서 §3](../guides/component-details.md) |
| 3 | (논문) K8s 커스텀 스케줄러 서베이 | [ACM CSUR 2022](https://dl.acm.org/doi/full/10.1145/3544788) |
| 4 | (논문) K8s HPA vs ML 기반 예측 스케일링 비교 | [Auto-Scaling 논문 리뷰](../../research/auto_scaling/README.md) |

**실습:**
```bash
python -m orchestrator.cli scale nginx --replicas=3
python -m orchestrator.cli list
```

---

## Week 2: CI/CD + 모니터링

### Day 1-2: CI/CD 파이프라인 (Shell Script)

**학습 목표:** 빌드→테스트→배포→롤백 파이프라인의 각 단계 이해

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | 빌드 파이프라인 (4단계) | [scripts/cicd/build.sh](../../scripts/cicd/build.sh) |
| 2 | 배포 스크립트 (프리체크→배포→포스트체크) | [scripts/cicd/deploy.sh](../../scripts/cicd/deploy.sh) |
| 3 | 롤백 처리 | [scripts/cicd/rollback.sh](../../scripts/cicd/rollback.sh) |
| 4 | 테스트 자동화 | [scripts/cicd/test.sh](../../scripts/cicd/test.sh) |
| 5 | CI/CD 파이프라인 흐름 | [아키텍처 문서 §5](../architecture/overview.md) |
| 6 | (논문) CI 실천 방법 실증 검증 | [IEEE TSE 2021](https://ieeexplore.ieee.org/document/9374092/) |
| 7 | (논문) DevOps 개념 서베이 | [ACM CSUR 2019](https://dl.acm.org/doi/abs/10.1145/3359981) |
| 8 | CI/CD 논문 전체 리뷰 | [research/cicd_pipeline/](../../research/cicd_pipeline/README.md) |

**실습:**
```bash
./scripts/cicd/build.sh myapp v1.0.0
./scripts/cicd/deploy.sh myapp v1.0.0 dev
./scripts/cicd/rollback.sh myapp dev
```

---

### Day 3-4: 모니터링 시스템 (Python)

**학습 목표:** 메트릭 수집 → 알림 → 대시보드 파이프라인 이해

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | 메트릭 수집기 코드 분석 | [monitoring/collector.py](../../monitoring/collector.py) |
| 2 | 알림 매니저 (Dedup, Slack/Email) | [monitoring/alerting/alert_manager.py](../../monitoring/alerting/alert_manager.py) |
| 3 | 터미널 대시보드 (Rich 라이브러리) | [monitoring/dashboard.py](../../monitoring/dashboard.py) |
| 4 | 임계치 체크 및 트렌드 분석 로직 | [컴포넌트 상세 문서 §4, §5](../guides/component-details.md) |
| 5 | (논문) 컨테이너 이상 탐지 (학습 없는 레플리카 비교) | [NDSS 2024](https://www.ndss-symposium.org/ndss-paper/replicawatcher-training-less-anomaly-detection-in-containerized-microservices/) |
| 6 | (논문) Google Dapper 분산 추적 | [Google Research](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/) |
| 7 | Monitoring 논문 전체 리뷰 | [research/monitoring/](../../research/monitoring/README.md) |

**실습:**
```bash
python -m monitoring.dashboard  # 실시간 대시보드 실행
```

---

### Day 5: 운영 스크립트

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | 환경 설정/정리 | [scripts/deploy/setup.sh](../../scripts/deploy/setup.sh), [teardown.sh](../../scripts/deploy/teardown.sh) |
| 2 | 백업 스크립트 | [scripts/ops/backup.sh](../../scripts/ops/backup.sh) |
| 3 | 로그 로테이션 | [scripts/ops/log_rotate.sh](../../scripts/ops/log_rotate.sh) |
| 4 | Makefile 단축 명령어 | [Makefile](../../Makefile) |

---

## Week 3: Java API + SQL + 테스트

### Day 1-2: Java REST API 서버

**학습 목표:** Spring Boot로 플랫폼 관리 API를 제공하는 구조 이해

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | Spring Boot 진입점 | [PlatformApplication.java](../../api/src/main/java/com/platform/PlatformApplication.java) |
| 2 | Controller 계층 (HTTP 엔드포인트) | [ContainerController.java](../../api/src/main/java/com/platform/controller/ContainerController.java) |
| 3 | Service 계층 (비즈니스 로직) | [ContainerService.java](../../api/src/main/java/com/platform/service/ContainerService.java) |
| 4 | 모니터링 API | [MonitoringController.java](../../api/src/main/java/com/platform/controller/MonitoringController.java), [MonitoringService.java](../../api/src/main/java/com/platform/service/MonitoringService.java) |
| 5 | 파이프라인 API | [PipelineController.java](../../api/src/main/java/com/platform/controller/PipelineController.java), [PipelineService.java](../../api/src/main/java/com/platform/service/PipelineService.java) |
| 6 | Model 클래스 | [Container.java](../../api/src/main/java/com/platform/model/Container.java), [Metric.java](../../api/src/main/java/com/platform/model/Metric.java), [Pipeline.java](../../api/src/main/java/com/platform/model/Pipeline.java) |
| 7 | API 엔드포인트 목록 | [실행 가이드 §8](../guides/setup-and-run.md) |

---

### Day 3: SQL 스키마 및 DB 관리

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | DB 스키마 (6개 테이블) | [db/schema.sql](../../db/schema.sql) |
| 2 | DB 매니저 (CRUD, 메트릭 평균, 정리) | [db/db_manager.py](../../db/db_manager.py) |
| 3 | 인덱스 전략 및 WAL 모드 | [아키텍처 문서 - DB 스키마 설계](../architecture/overview.md) |

---

### Day 4-5: 테스트 코드 분석

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | DB 테스트 (CRUD, 이벤트, 메트릭, 파이프라인, 알림) | [tests/test_db.py](../../tests/test_db.py) |
| 2 | 오케스트레이터 테스트 (Mock 기반) | [tests/test_orchestrator.py](../../tests/test_orchestrator.py) |
| 3 | 모니터링 테스트 (수집기, 알림) | [tests/test_monitoring.py](../../tests/test_monitoring.py) |

**실습:**
```bash
make test          # 전체 37개 테스트 실행
make test-db       # DB 테스트만
make test-monitoring  # 모니터링 테스트만
```

---

## Week 4: AI Ops + 논문 리뷰

### Day 1-2: MCP Server 및 AI Agent

**학습 목표:** MCP 프로토콜 기반 AI 운영 자동화 이해

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | MCP 서버 구조 (도구 목록, 호출 처리) | [mcp_server/server.py](../../mcp_server/server.py) |
| 2 | 도구 구현 (10개 도구, 디스패치 패턴) | [mcp_server/tools.py](../../mcp_server/tools.py) |
| 3 | MCP 서버 흐름 및 도구 목록 | [컴포넌트 상세 문서 §8](../guides/component-details.md) |
| 4 | (논문) LLM 기반 K8s 관리 에이전트 | [KubeIntellect, arXiv](https://arxiv.org/abs/2509.02449) |
| 5 | (논문) LLM 기반 자동 근본 원인 분석 | [RCACopilot, EuroSys 2024](https://arxiv.org/abs/2305.15778) |
| 6 | (논문) 멀티 에이전트 CloudOps 프레임워크 | [MOYA, CAIN 2025](https://arxiv.org/abs/2501.08243) |
| 7 | AIOps 논문 전체 리뷰 | [research/ai_ops/](../../research/ai_ops/README.md) |

---

### Day 3-5: 논문 전체 리뷰

| 순서 | 학습 내용 | 자료 |
|:----:|----------|------|
| 1 | **전체 42편 논문 요약본 (링크 포함)** | [research/summaries/](../../research/summaries/README.md) |
| 2 | Container Orchestration 논문 7편 | [research/container_orchestration/](../../research/container_orchestration/README.md) |
| 3 | CI/CD Pipeline 논문 7편 | [research/cicd_pipeline/](../../research/cicd_pipeline/README.md) |
| 4 | Monitoring System 논문 7편 | [research/monitoring/](../../research/monitoring/README.md) |
| 5 | Auto-Scaling 논문 7편 | [research/auto_scaling/](../../research/auto_scaling/README.md) |
| 6 | Self-Healing 논문 7편 | [research/self_healing/](../../research/self_healing/README.md) |
| 7 | AIOps 논문 7편 | [research/ai_ops/](../../research/ai_ops/README.md) |

---

## 빠른 참조 (오늘 공부할 문서 찾기)

### 문서 인덱스

| 문서 | 내용 | 링크 |
|------|------|------|
| 시스템 아키텍처 | 전체 구조, 데이터 흐름, 설계 결정 | [overview.md](../architecture/overview.md) |
| 환경 구성 및 실행 가이드 | 설치부터 실행까지 전체 가이드 | [setup-and-run.md](../guides/setup-and-run.md) |
| 컴포넌트별 상세 동작 원리 | 각 모듈의 내부 구현 상세 설명 | [component-details.md](../guides/component-details.md) |
| 논문 요약본 (42편) | 전체 논문 링크 + 1-2줄 요약 | [summaries/README.md](../../research/summaries/README.md) |

### 코드 인덱스

| 모듈 | 파일 | 핵심 기능 |
|------|------|-----------|
| 오케스트레이션 엔진 | [orchestrator/engine.py](../../orchestrator/engine.py) | 배포, 스케일링, 데몬 통합 관리 |
| 컨테이너 관리 | [orchestrator/container.py](../../orchestrator/container.py) | Docker SDK 래핑, CRUD, 메트릭 |
| 헬스체크 | [orchestrator/health_checker.py](../../orchestrator/health_checker.py) | 3방식 체크, 자동 복구 |
| 오토스케일러 | [orchestrator/scaler.py](../../orchestrator/scaler.py) | CPU/메모리 기반 자동 스케일링 |
| CLI | [orchestrator/cli.py](../../orchestrator/cli.py) | Click 기반 커맨드라인 |
| 메트릭 수집 | [monitoring/collector.py](../../monitoring/collector.py) | 주기적 메트릭 수집 + 임계치 체크 |
| 알림 매니저 | [monitoring/alerting/alert_manager.py](../../monitoring/alerting/alert_manager.py) | Slack/Email 알림, 중복 방지 |
| 대시보드 | [monitoring/dashboard.py](../../monitoring/dashboard.py) | Rich 기반 터미널 UI |
| DB 매니저 | [db/db_manager.py](../../db/db_manager.py) | SQLite CRUD, 메트릭 평균 |
| DB 스키마 | [db/schema.sql](../../db/schema.sql) | 6개 테이블 정의 |
| MCP 서버 | [mcp_server/server.py](../../mcp_server/server.py) | MCP 프로토콜 서버 |
| MCP 도구 | [mcp_server/tools.py](../../mcp_server/tools.py) | 10개 AI 운영 도구 |
| 플랫폼 설정 | [configs/platform.yaml](../../configs/platform.yaml) | 전역 설정 |
| 서비스 정의 예시 | [configs/examples/service.yaml](../../configs/examples/service.yaml) | Nginx+Redis+PostgreSQL 스택 |
