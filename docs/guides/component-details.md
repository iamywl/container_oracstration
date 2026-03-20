# 컴포넌트별 상세 동작 원리

> 각 컴포넌트의 내부 구현을 이해하고 수정/확장할 수 있도록 정리한 문서

---

## 1. Container Manager (`orchestrator/container.py`)

### 핵심 클래스: `ContainerManager`

Docker SDK의 `docker.from_env()`로 로컬 Docker 엔진에 연결하여 컨테이너 라이프사이클을 관리한다.

**관리 대상 식별 방식:**
- 모든 관리 대상 컨테이너에 `orchestrator.managed=true` 레이블 부여
- `list_managed()`는 이 레이블로 필터링하여 조회
- `orchestrator.service={name}` 레이블로 서비스 그룹핑

**컨테이너 생성 과정:**
```python
# 1. 이미지 pull (없으면 다운로드)
self.client.images.pull(config.image)

# 2. 컨테이너 실행 (detach=True로 백그라운드)
container = self.client.containers.run(
    image=config.image,
    name=config.name,
    detach=True,
    labels=labels,         # 관리 레이블 부여
    ports=config.ports,
    nano_cpus=int(cpu * 1e9),  # CPU 제한 (나노초 단위)
    mem_limit=config.memory_limit,
)
```

**메트릭 수집 계산식:**
```python
# CPU 사용률 계산
cpu_delta = current_total - previous_total
system_delta = current_system - previous_system
cpu_percent = (cpu_delta / system_delta) * num_cpus * 100

# 메모리 사용률 계산
memory_percent = (memory_usage / memory_limit) * 100
```

**롤링 업데이트 절차:**
1. 각 레플리카를 순차적으로 처리
2. 새 이미지로 임시 컨테이너 생성 (`{name}_new`)
3. 5초 대기 후 헬스체크
4. 실패 시: 새 컨테이너 제거, 롤백 중단
5. 성공 시: 기존 컨테이너 중지 → 제거 → 새 컨테이너 이름 변경

---

## 2. Health Checker (`orchestrator/health_checker.py`)

### 3가지 체크 방식

| 방식 | 구현 | 용도 |
|------|------|------|
| `status` | Docker 컨테이너 상태가 `running`인지 확인 | 기본 생존 확인 |
| `http` | HTTP GET 요청 후 200 응답 확인 | 웹 서버 |
| `tcp` | TCP 소켓 연결 시도 | DB, Redis 등 |

### 장애 판정 및 자동 복구 로직

```
체크 실패 → failure_count++
  ├─ failure_count < retries → 경고 로그만 출력
  └─ failure_count >= retries → 자동 복구 시작
       ├─ container_mgr.restart() 호출
       ├─ 성공 → failure_count 리셋, 10초 대기
       └─ 실패 → 에러 로그, DB에 restart_failed 이벤트 기록
```

---

## 3. Auto Scaler (`orchestrator/scaler.py`)

### 스케일링 판단 기준

```
평균 CPU > cpu_threshold OR 평균 Memory > memory_threshold
  → Scale Up (현재 + scale_up_step, max_replicas 이하)

평균 CPU < cpu_threshold × 0.5 AND 평균 Memory < memory_threshold × 0.5
  → Scale Down (현재 - scale_down_step, min_replicas 이상)
```

- **0.5 배수 기준**: 임계치의 절반 이하로 떨어져야 스케일 다운 → 빈번한 스케일링 방지
- **cooldown**: 마지막 스케일링 이후 지정 시간(초)이 지나야 다음 스케일링 수행

### 스케일 아웃 시 레플리카 이름 규칙
```
{service_name}-{index}
예: nginx-0, nginx-1, nginx-2
```

---

## 4. Metric Collector (`monitoring/collector.py`)

### 수집 주기 및 저장

- 기본 `interval=15`초마다 모든 running 컨테이너의 메트릭 수집
- Docker Stats API → CPU%, Memory%, Network RX/TX 계산
- `db.save_metric()`으로 SQLite에 저장
- 7일 이상 된 메트릭은 `cleanup_old_metrics()`로 자동 정리

### 임계치 체크 및 알림 발생

```python
thresholds = {
    "cpu_critical": 90.0,     # → critical 알림 + Slack + Email
    "cpu_warning": 80.0,      # → warning 알림 + Slack
    "memory_critical": 90.0,  # → critical 알림 + Slack + Email
    "memory_warning": 80.0,   # → warning 알림 + Slack
}
```

### 트렌드 분석

최근 10개 샘플을 3개씩 비교:
- 최근 3개 평균 > 이전 3개 평균 × 1.2 → `increasing`
- 최근 3개 평균 < 이전 3개 평균 × 0.8 → `decreasing`
- 그 외 → `stable`

---

## 5. Alert Manager (`monitoring/alerting/alert_manager.py`)

### 중복 알림 방지 (Dedup)

```python
dedup_key = f"{container_name}:{alert_type}"
# 같은 키로 dedup_interval(기본 300초) 내 재발생 시 무시
```

### 알림 채널 분기

| Severity | Slack | Email | DB 저장 |
|----------|:-----:|:-----:|:-------:|
| critical | O | O | O |
| warning | O | X | O |
| info | X | X | O |

---

## 6. DB Manager (`db/db_manager.py`)

### 주요 메서드

| 메서드 | 용도 |
|--------|------|
| `init()` | schema.sql로 테이블 생성 |
| `upsert_container()` | 컨테이너 상태 저장/갱신 (ON CONFLICT DO UPDATE) |
| `log_event()` | 이벤트 기록 (append-only) |
| `save_metric()` | 메트릭 저장 |
| `get_metric_avg()` | 최근 N분간 평균 메트릭 |
| `create_pipeline_run()` | 파이프라인 실행 기록 |
| `create_deployment()` | 배포 이력 생성 |
| `mark_rollback()` | 배포 롤백 처리 |
| `create_alert()` | 알림 생성 |
| `resolve_alert()` | 알림 해결 처리 |

### 연결 설정

```python
conn.execute("PRAGMA journal_mode=WAL")    # 동시 읽기/쓰기
conn.execute("PRAGMA foreign_keys=ON")     # 참조 무결성
conn.row_factory = sqlite3.Row             # dict-like 결과
```

---

## 7. Java API Server (`api/`)

### 계층 구조

```
Controller (HTTP 요청 처리)
    → Service (비즈니스 로직, JdbcTemplate으로 DB 조회)
        → SQLite DB (Python과 동일한 DB 파일 공유)
```

### Spring Boot 설정

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:sqlite:../db/platform.db  # Python과 같은 DB 파일
```

---

## 8. MCP Server (`mcp_server/`)

### 도구 목록 (10개)

| 도구 | 기능 |
|------|------|
| `list_containers` | 컨테이너 목록 조회 |
| `deploy_service` | YAML 기반 서비스 배포 |
| `scale_service` | 레플리카 수 조정 |
| `get_container_stats` | 리소스 사용량 조회 |
| `get_container_logs` | 로그 조회 |
| `health_check` | 전체 헬스 상태 확인 |
| `get_alerts` | 활성 알림 조회 |
| `get_platform_overview` | 전체 상태 요약 |
| `analyze_issue` | 장애 분석 (로그+메트릭+이벤트 종합) |
| `get_deployment_history` | 배포 이력 조회 |

### 도구 디스패치 패턴

```python
def execute(self, tool_name, arguments):
    handler = getattr(self, f"_tool_{tool_name}", None)
    return handler(arguments)
```

`_tool_{name}` 메서드를 추가하면 자동으로 새 도구가 등록되는 구조.
