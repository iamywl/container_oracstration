"""데이터베이스 매니저 - SQLite 기반 상태/이력 관리"""

import sqlite3
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "platform.db"
SCHEMA_PATH = DB_DIR / "schema.sql"


class DBManager:
    """SQLite 데이터베이스 매니저"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DB_PATH)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def init(self):
        """데이터베이스 초기화 - 스키마 적용"""
        schema_path = SCHEMA_PATH
        if not schema_path.exists():
            logger.error(f"Schema file not found: {schema_path}")
            return False

        with open(schema_path) as f:
            schema_sql = f.read()

        conn = self._connect()
        try:
            conn.executescript(schema_sql)
            conn.commit()
            logger.info(f"Database initialized: {self.db_path}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Database init failed: {e}")
            return False
        finally:
            conn.close()

    # --- 컨테이너 상태 관리 ---

    def upsert_container(self, name: str, service: str, image: str,
                         status: str, replica_idx: int = 0):
        """컨테이너 상태 저장/갱신"""
        conn = self._connect()
        try:
            conn.execute("""
                INSERT INTO containers (name, service, image, status, replica_idx, updated_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(name) DO UPDATE SET
                    status = excluded.status,
                    image = excluded.image,
                    updated_at = CURRENT_TIMESTAMP
            """, (name, service, image, status, replica_idx))
            conn.commit()
        finally:
            conn.close()

    def get_containers(self, service: str = None, status: str = None) -> list[dict]:
        """컨테이너 목록 조회"""
        conn = self._connect()
        try:
            query = "SELECT * FROM containers WHERE 1=1"
            params = []
            if service:
                query += " AND service = ?"
                params.append(service)
            if status:
                query += " AND status = ?"
                params.append(status)
            query += " ORDER BY created_at DESC"

            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    # --- 이벤트 로그 ---

    def log_event(self, container_name: str, event_type: str, details: str = None):
        """이벤트 기록"""
        conn = self._connect()
        try:
            conn.execute(
                "INSERT INTO events (container_name, event_type, details) VALUES (?, ?, ?)",
                (container_name, event_type, details)
            )
            conn.commit()
        finally:
            conn.close()

    def get_events(self, container_name: str = None, event_type: str = None,
                   limit: int = 50) -> list[dict]:
        """이벤트 조회"""
        conn = self._connect()
        try:
            query = "SELECT * FROM events WHERE 1=1"
            params = []
            if container_name:
                query += " AND container_name = ?"
                params.append(container_name)
            if event_type:
                query += " AND event_type = ?"
                params.append(event_type)
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    # --- 메트릭 ---

    def save_metric(self, container_name: str, cpu_percent: float,
                    memory_usage_mb: float, memory_percent: float,
                    network_rx: int = 0, network_tx: int = 0):
        """메트릭 저장"""
        conn = self._connect()
        try:
            conn.execute("""
                INSERT INTO metrics (container_name, cpu_percent, memory_usage_mb,
                                     memory_percent, network_rx, network_tx)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (container_name, cpu_percent, memory_usage_mb, memory_percent,
                  network_rx, network_tx))
            conn.commit()
        finally:
            conn.close()

    def get_metrics(self, container_name: str, limit: int = 100) -> list[dict]:
        """메트릭 조회"""
        conn = self._connect()
        try:
            rows = conn.execute("""
                SELECT * FROM metrics
                WHERE container_name = ?
                ORDER BY collected_at DESC LIMIT ?
            """, (container_name, limit)).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_metric_avg(self, container_name: str, minutes: int = 5) -> dict:
        """최근 N분간 평균 메트릭"""
        conn = self._connect()
        try:
            row = conn.execute("""
                SELECT
                    AVG(cpu_percent) as avg_cpu,
                    AVG(memory_percent) as avg_memory,
                    MAX(cpu_percent) as max_cpu,
                    MAX(memory_percent) as max_memory,
                    COUNT(*) as sample_count
                FROM metrics
                WHERE container_name = ?
                  AND collected_at >= datetime('now', ? || ' minutes')
            """, (container_name, f"-{minutes}")).fetchone()
            return dict(row) if row else {}
        finally:
            conn.close()

    # --- CI/CD 파이프라인 ---

    def create_pipeline_run(self, pipeline_id: str, app_name: str,
                            version: str, stage: str) -> int:
        """파이프라인 실행 기록 생성"""
        conn = self._connect()
        try:
            cursor = conn.execute("""
                INSERT INTO pipeline_runs (pipeline_id, app_name, version, stage, status)
                VALUES (?, ?, ?, ?, 'running')
            """, (pipeline_id, app_name, version, stage))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_pipeline_run(self, run_id: int, status: str,
                            log_output: str = None, duration_s: int = None):
        """파이프라인 실행 상태 갱신"""
        conn = self._connect()
        try:
            conn.execute("""
                UPDATE pipeline_runs
                SET status = ?, log_output = ?, duration_s = ?,
                    finished_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, log_output, duration_s, run_id))
            conn.commit()
        finally:
            conn.close()

    def get_pipeline_history(self, app_name: str = None, limit: int = 20) -> list[dict]:
        """파이프라인 실행 이력 조회"""
        conn = self._connect()
        try:
            query = "SELECT * FROM pipeline_runs WHERE 1=1"
            params = []
            if app_name:
                query += " AND app_name = ?"
                params.append(app_name)
            query += " ORDER BY started_at DESC LIMIT ?"
            params.append(limit)

            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    # --- 배포 이력 ---

    def create_deployment(self, service: str, image: str, version: str,
                          replicas: int, environment: str = "dev") -> int:
        """배포 이력 생성"""
        conn = self._connect()
        try:
            cursor = conn.execute("""
                INSERT INTO deployments (service, image, version, replicas, environment, status)
                VALUES (?, ?, ?, ?, ?, 'deployed')
            """, (service, image, version, replicas, environment))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_last_deployment(self, service: str, environment: str = "dev") -> Optional[dict]:
        """최근 배포 이력 조회"""
        conn = self._connect()
        try:
            row = conn.execute("""
                SELECT * FROM deployments
                WHERE service = ? AND environment = ? AND rolled_back = 0
                ORDER BY deployed_at DESC LIMIT 1
            """, (service, environment)).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def mark_rollback(self, deployment_id: int):
        """배포 롤백 처리"""
        conn = self._connect()
        try:
            conn.execute(
                "UPDATE deployments SET rolled_back = 1 WHERE id = ?",
                (deployment_id,)
            )
            conn.commit()
        finally:
            conn.close()

    # --- 알림 ---

    def create_alert(self, container_name: str, alert_type: str,
                     severity: str, message: str) -> int:
        """알림 생성"""
        conn = self._connect()
        try:
            cursor = conn.execute("""
                INSERT INTO alerts (container_name, alert_type, severity, message)
                VALUES (?, ?, ?, ?)
            """, (container_name, alert_type, severity, message))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def resolve_alert(self, alert_id: int):
        """알림 해결 처리"""
        conn = self._connect()
        try:
            conn.execute("""
                UPDATE alerts SET resolved = 1, resolved_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (alert_id,))
            conn.commit()
        finally:
            conn.close()

    def get_active_alerts(self) -> list[dict]:
        """미해결 알림 조회"""
        conn = self._connect()
        try:
            rows = conn.execute("""
                SELECT * FROM alerts WHERE resolved = 0
                ORDER BY created_at DESC
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    # --- 유틸리티 ---

    def cleanup_old_metrics(self, days: int = 7):
        """오래된 메트릭 정리"""
        conn = self._connect()
        try:
            conn.execute("""
                DELETE FROM metrics
                WHERE collected_at < datetime('now', ? || ' days')
            """, (f"-{days}",))
            conn.commit()
            logger.info(f"Cleaned up metrics older than {days} days")
        finally:
            conn.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        db = DBManager()
        if db.init():
            print("Database initialized successfully")
        else:
            print("Database initialization failed")
            sys.exit(1)
