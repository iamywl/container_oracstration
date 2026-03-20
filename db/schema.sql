-- Container Orchestration Platform Database Schema
-- 컨테이너 상태, 배포 이력, 메트릭, CI/CD 파이프라인 이력 관리

-- 컨테이너 상태 테이블
CREATE TABLE IF NOT EXISTS containers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    service     TEXT NOT NULL,
    image       TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'created',
    replica_idx INTEGER DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_containers_service ON containers(service);
CREATE INDEX IF NOT EXISTS idx_containers_status ON containers(status);

-- 이벤트 로그 테이블 (배포, 스케일링, 복구 등)
CREATE TABLE IF NOT EXISTS events (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    container_name  TEXT NOT NULL,
    event_type      TEXT NOT NULL,
    details         TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_events_container ON events(container_name);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_time ON events(created_at);

-- 메트릭 테이블 (CPU, 메모리, 네트워크 등)
CREATE TABLE IF NOT EXISTS metrics (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    container_name  TEXT NOT NULL,
    cpu_percent     REAL DEFAULT 0,
    memory_usage_mb REAL DEFAULT 0,
    memory_percent  REAL DEFAULT 0,
    network_rx      INTEGER DEFAULT 0,
    network_tx      INTEGER DEFAULT 0,
    collected_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_metrics_container ON metrics(container_name);
CREATE INDEX IF NOT EXISTS idx_metrics_time ON metrics(collected_at);

-- CI/CD 파이프라인 실행 이력
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_id TEXT NOT NULL,
    app_name    TEXT NOT NULL,
    version     TEXT,
    stage       TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending',
    log_output  TEXT,
    started_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP,
    duration_s  INTEGER
);

CREATE INDEX IF NOT EXISTS idx_pipeline_app ON pipeline_runs(app_name);
CREATE INDEX IF NOT EXISTS idx_pipeline_status ON pipeline_runs(status);

-- 배포 이력 테이블
CREATE TABLE IF NOT EXISTS deployments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    service     TEXT NOT NULL,
    image       TEXT NOT NULL,
    version     TEXT,
    replicas    INTEGER DEFAULT 1,
    environment TEXT DEFAULT 'dev',
    status      TEXT NOT NULL DEFAULT 'pending',
    deployed_by TEXT,
    deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rolled_back INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_deployments_service ON deployments(service);
CREATE INDEX IF NOT EXISTS idx_deployments_env ON deployments(environment);

-- 알림 이력 테이블
CREATE TABLE IF NOT EXISTS alerts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    container_name  TEXT NOT NULL,
    alert_type      TEXT NOT NULL,
    severity        TEXT NOT NULL DEFAULT 'warning',
    message         TEXT NOT NULL,
    resolved        INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at     TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_alerts_container ON alerts(container_name);
CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON alerts(resolved);
