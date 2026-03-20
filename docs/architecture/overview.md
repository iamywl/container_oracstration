# 시스템 아키텍처 상세 문서

> 이 문서를 읽으면 프로젝트 전체 구조와 각 컴포넌트의 동작 원리를 이해하고 재현할 수 있다.

---

## 전체 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Agent (AI Ops)                    │
│              mcp_server/server.py                        │
│         자연어 명령 → 도구 호출 → 결과 반환               │
├─────────────────────────────────────────────────────────┤
│                  Java REST API Server                    │
│            api/src/main/java/com/platform/              │
│     GET /api/containers, /api/monitoring, /api/pipelines │
├──────────┬──────────────────┬───────────────────────────┤
│Container │   CI/CD Pipeline │   Monitoring System       │
│Orchestr. │                  │                           │
│(Python)  │  (Shell Script)  │   (Python)                │
│          │                  │                           │
│engine.py │  build.sh        │  collector.py             │
│containe… │  test.sh         │  dashboard.py             │
│health_c… │  deploy.sh       │  alert_manager.py         │
│scaler.py │  rollback.sh     │                           │
├──────────┴──────────────────┴───────────────────────────┤
│                   SQLite Database                        │
│              db/schema.sql + db_manager.py               │
│     containers | events | metrics | pipeline_runs |      │
│     deployments | alerts                                 │
├─────────────────────────────────────────────────────────┤
│                   Docker Engine                          │
│              unix:///var/run/docker.sock                  │
└─────────────────────────────────────────────────────────┘
```

---

## 데이터 흐름

### 1. 서비스 배포 흐름

```
사용자 → CLI (cli.py)
         → engine.py (YAML 파싱)
         → container.py (Docker SDK 호출)
         → Docker Engine (컨테이너 생성)
         → db_manager.py (상태 DB 저장)
         → health_checker.py (헬스체크 등록)
         → scaler.py (오토스케일링 정책 등록)
```

**상세 과정:**

1. `cli.py`의 `deploy` 커맨드가 YAML 경로를 받음
2. `engine.py`의 `load_service_definition()`이 YAML을 파싱
3. `services` 섹션의 각 서비스에 대해:
   - `replicas` 수만큼 반복하며 `ContainerConfig` 생성
   - `container.py`의 `create()`가 Docker SDK `client.containers.run()` 호출
   - 레이블에 `orchestrator.managed=true`, `orchestrator.service={name}` 부여
4. `health_check` 섹션이 있으면 `HealthCheck` 객체를 생성하여 `HealthChecker`에 등록
5. `scaling` 섹션이 있으면 `ScalingPolicy`를 생성하여 `AutoScaler`에 등록
6. 모든 배포 이벤트는 `db_manager.py`의 `log_event()`로 DB에 기록

### 2. 헬스체크 + 자동 복구 흐름

```
HealthChecker._loop() (백그라운드 스레드)
  → 등록된 모든 HealthCheck를 순회
  → check_container() 호출
    ├─ type="status" → Docker 컨테이너 상태 확인
    ├─ type="http"   → HTTP GET 요청 (200 여부)
    └─ type="tcp"    → TCP 소켓 연결 시도
  → 실패 시: failure_count 증가
  → failure_count >= retries:
    → container_mgr.restart() 호출
    → db에 auto_restart 이벤트 기록
  → 성공 시: failure_count 초기화
```

**핵심 설계:**
- `threading.Thread(daemon=True)`로 백그라운드 실행
- 각 HealthCheck마다 `interval`, `timeout`, `retries` 독립 설정
- 중복 재시작 방지: `retries` 도달 후 재시작, 이후 `failure_count` 리셋

### 3. 오토 스케일링 흐름

```
AutoScaler._loop() (백그라운드 스레드)
  → 등록된 모든 ScalingPolicy를 순회
  → evaluate() 호출:
    1. get_avg_metrics() → 전체 레플리카의 평균 CPU/메모리 조회
    2. CPU > threshold 또는 Memory > threshold?
       → scale_up: 현재 + scale_up_step (max_replicas 제한)
    3. CPU < threshold*0.5 AND Memory < threshold*0.5?
       → scale_down: 현재 - scale_down_step (min_replicas 제한)
    4. cooldown 기간 내이면 스킵 (과도한 스케일링 방지)
```

**핵심 설계:**
- 스케일 아웃: 새 `ContainerConfig`를 생성하여 `container_mgr.create()` 호출
- 스케일 인: 뒤쪽 레플리카부터 `stop()` → `remove()`
- `cooldown` 파라미터로 연쇄 스케일링 방지

### 4. 모니터링 흐름

```
MetricCollector._loop() (백그라운드 스레드)
  → list_managed()로 관리 대상 컨테이너 조회
  → 각 running 컨테이너:
    → get_stats() → Docker stats API 호출
    → CPU%, Memory%, Network 계산
    → db.save_metric()으로 DB 저장
    → _check_thresholds()
      → 임계치 초과 시 AlertManager.fire() 호출

AlertManager.fire()
  → 중복 체크 (_dedup_cache)
  → db.create_alert()
  → severity == "critical" → Slack + Email
  → severity == "warning"  → Slack만
```

### 5. CI/CD 파이프라인 흐름

```
build.sh <app> <version> [env]
  ├─ Stage 1: 소스 검증 (Dockerfile 존재 확인)
  ├─ Stage 2: 테스트 (pytest 실행)
  ├─ Stage 3: Docker 이미지 빌드
  └─ Stage 4: 아티팩트 저장 (build-info.json)

deploy.sh <app> <version> [env]
  ├─ Pre-deploy: 이미지 존재 확인
  ├─ 기존 컨테이너 롤링 업데이트
  ├─ 새 컨테이너 시작
  └─ Post-deploy: 헬스체크 → 실패 시 rollback.sh 호출

rollback.sh <app> [env]
  ├─ 현재 컨테이너 중지/제거
  ├─ DB에서 이전 배포 정보 조회
  └─ 이전 버전으로 재배포 또는 수동 개입 안내
```

### 6. MCP 서버 흐름

```
LLM Agent → stdio (stdin/stdout)
  → MCP Server (server.py)
  → list_tools() → 사용 가능한 도구 목록 반환
  → call_tool(name, arguments)
    → ContainerTools.execute(name, args)
    → _tool_{name}(args) 디스패치
    → OrchestrationEngine / DBManager 호출
    → JSON 결과 반환
```

---

## DB 스키마 설계

```sql
-- 6개 테이블, 각각의 역할:

containers     -- 컨테이너 현재 상태 (UPSERT 방식 갱신)
events         -- 모든 운영 이벤트 로그 (append-only)
metrics        -- 시계열 메트릭 데이터 (주기적 수집)
pipeline_runs  -- CI/CD 파이프라인 실행 이력
deployments    -- 배포 이력 (롤백 추적 포함)
alerts         -- 알림 이력 (해결 여부 추적)
```

**인덱스 전략:**
- 모든 테이블에 `container_name`/`service` 인덱스 → 조회 성능
- `events`, `metrics`에 시간 인덱스 → 시계열 쿼리 최적화
- `alerts`에 `resolved` 인덱스 → 활성 알림 빠른 조회

**WAL 모드:**
- `PRAGMA journal_mode=WAL` → 읽기/쓰기 동시성 향상
- 모니터링 수집기(쓰기)와 대시보드(읽기)가 동시 접근 가능

---

## 주요 설계 결정

### 왜 Docker SDK(Python)를 직접 사용하는가?
- Docker CLI 래핑 대비: 구조화된 응답, 에러 핸들링, 타입 안전성
- `docker.from_env()`로 로컬 Docker 소켓에 직접 연결
- `container.stats(stream=False)`로 1회성 메트릭 수집 (스트림 방식은 리소스 낭비)

### 왜 SQLite인가?
- 외부 DB 서버 불필요 → 단일 바이너리로 동작
- WAL 모드로 동시 읽기/쓰기 지원
- 메트릭 보관 기간(7일)으로 용량 관리 → `cleanup_old_metrics()`

### 왜 스레드 기반 데몬인가?
- `daemon=True`로 메인 프로세스 종료 시 자동 정리
- 헬스체크/메트릭 수집/오토스케일링이 독립적으로 동작
- GIL 이슈: I/O 바운드 작업이므로 스레드로 충분

### 왜 MCP 프로토콜인가?
- 표준화된 LLM ↔ 도구 통신 프로토콜
- stdio 기반으로 어떤 LLM 클라이언트와도 연동 가능
- 도구 스키마(JSON Schema)로 타입 안전한 인터페이스 제공
