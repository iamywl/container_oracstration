# 환경 구성 및 실행 가이드

> 처음부터 끝까지 따라하면 플랫폼을 실행할 수 있는 가이드

---

## 1. 사전 요구사항

| 도구 | 버전 | 확인 방법 |
|------|------|-----------|
| Docker | 20.10+ | `docker --version` |
| Python | 3.10+ | `python3 --version` |
| Java | 17+ | `java --version` |
| SQLite | 3.x | `sqlite3 --version` |

---

## 2. 초기 설정

```bash
# 프로젝트 클론
git clone https://github.com/iamywl/container_oracstration.git
cd container_oracstration

# 자동 설정 (디렉토리 생성, 의존성 설치, DB 초기화)
./scripts/deploy/setup.sh
```

**setup.sh가 하는 일:**
1. Docker 데몬 상태 확인
2. `logs/`, `build/`, `data/` 디렉토리 생성
3. `pip install -r requirements.txt` 실행
4. `db/schema.sql`로 SQLite DB 초기화
5. `.gitignore` 설정

**수동 설정 (setup.sh 없이):**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 db/db_manager.py init
```

---

## 3. 서비스 배포

### YAML 서비스 정의 작성

`configs/examples/service.yaml` 참고:

```yaml
services:
  nginx:
    image: "nginx:1.25-alpine"
    replicas: 2
    ports:
      "80/tcp": 8080
    cpu_limit: 0.5
    memory_limit: "256m"
    health_check:
      type: "http"
      endpoint: "http://localhost:8080/"
      interval: 30
      timeout: 5
      retries: 3
    scaling:
      min_replicas: 1
      max_replicas: 5
      cpu_threshold: 70.0
```

### 배포 실행

```bash
# CLI로 배포
python -m orchestrator.cli deploy configs/examples/service.yaml

# 컨테이너 목록 확인
python -m orchestrator.cli list

# 특정 컨테이너 상태
python -m orchestrator.cli stats nginx-0

# 로그 확인
python -m orchestrator.cli logs nginx-0 --tail 50
```

---

## 4. 헬스체크 및 오토스케일링 데몬

```bash
# 데몬 시작 (헬스체크 + 오토스케일러 백그라운드 실행)
python -m orchestrator.cli daemon

# Ctrl+C로 중지
```

**데몬이 하는 일:**
- 등록된 모든 컨테이너에 대해 주기적 헬스체크
- 실패 횟수가 retries에 도달하면 자동 재시작
- CPU/메모리 사용률이 임계치를 초과하면 자동 스케일 아웃
- 사용률이 낮으면 자동 스케일 인

---

## 5. 수동 스케일링

```bash
# nginx를 3개 레플리카로 스케일 아웃
python -m orchestrator.cli scale nginx --replicas=3

# 1개로 스케일 인
python -m orchestrator.cli scale nginx --replicas=1
```

---

## 6. 모니터링 대시보드

```bash
python -m monitoring.dashboard
```

터미널에 실시간 대시보드가 표시됨:
- 컨테이너 상태 테이블 (이름, 서비스, 이미지, 상태)
- 리소스 사용량 (CPU%, 메모리, 네트워크)
- 활성 알림 패널
- 최근 이벤트 패널

---

## 7. CI/CD 파이프라인

```bash
# 빌드 (소스검증 → 테스트 → Docker 빌드 → 아티팩트 저장)
./scripts/cicd/build.sh myapp v1.0.0

# 배포
./scripts/cicd/deploy.sh myapp v1.0.0 dev

# 롤백 (문제 발생 시)
./scripts/cicd/rollback.sh myapp dev

# 테스트만 실행
./scripts/cicd/test.sh
```

---

## 8. Java API 서버

```bash
cd api
./gradlew bootRun
```

**API 엔드포인트:**

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/containers` | 컨테이너 목록 |
| GET | `/api/containers/overview` | 전체 현황 |
| GET | `/api/containers/events` | 이벤트 로그 |
| GET | `/api/monitoring/metrics/{name}` | 컨테이너 메트릭 |
| GET | `/api/monitoring/metrics/{name}/avg` | 평균 메트릭 |
| GET | `/api/monitoring/alerts` | 활성 알림 |
| GET | `/api/monitoring/dashboard` | 대시보드 데이터 |
| GET | `/api/pipelines/history` | 파이프라인 이력 |
| GET | `/api/pipelines/deployments` | 배포 이력 |

---

## 9. MCP 서버

```bash
python -m mcp_server.server
```

MCP 클라이언트(Claude Desktop 등)에서 연결하여 자연어로 컨테이너 관리:
- "현재 컨테이너 상태 보여줘"
- "nginx를 3개로 스케일 아웃해줘"
- "nginx-0 컨테이너 장애 분석해줘"

---

## 10. 운영 스크립트

```bash
# 데이터 백업
./scripts/ops/backup.sh

# 로그 로테이션 (30일 이상 로그 삭제)
./scripts/ops/log_rotate.sh

# 환경 정리 (컨테이너 중지, 빌드 삭제)
./scripts/deploy/teardown.sh

# 강제 정리 (DB 포함)
./scripts/deploy/teardown.sh --force
```

---

## 11. Makefile 단축 명령어

```bash
make help          # 사용 가능한 명령어 목록
make setup         # 초기 설정
make test          # 전체 테스트
make list          # 컨테이너 목록
make health        # 헬스체크
make dashboard     # 모니터링 대시보드
make daemon        # 데몬 시작
make build APP_NAME=myapp VERSION=v1.0  # 빌드
make deploy APP_NAME=myapp VERSION=v1.0 # 배포
make backup        # 백업
make clean         # 정리
```
