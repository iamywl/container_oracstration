"""컨테이너 헬스체크 및 자동 복구 모듈"""

import threading
import time
import logging
import requests
from typing import Optional
from orchestrator.container import ContainerManager

logger = logging.getLogger(__name__)


class HealthCheck:
    """헬스체크 설정"""
    def __init__(self, container_name: str, check_type: str = "status",
                 endpoint: Optional[str] = None, interval: int = 30,
                 timeout: int = 5, retries: int = 3):
        self.container_name = container_name
        self.check_type = check_type  # "status", "http", "tcp"
        self.endpoint = endpoint
        self.interval = interval
        self.timeout = timeout
        self.retries = retries
        self.failure_count = 0
        self.last_check = None
        self.healthy = True


class HealthChecker:
    """컨테이너 헬스체크 및 자동 복구 엔진"""

    def __init__(self, container_manager: ContainerManager, db_manager=None):
        self.manager = container_manager
        self.db = db_manager
        self.checks: dict[str, HealthCheck] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def register(self, health_check: HealthCheck):
        """헬스체크 등록"""
        self.checks[health_check.container_name] = health_check
        logger.info(f"Health check registered: {health_check.container_name} "
                    f"(type={health_check.check_type}, interval={health_check.interval}s)")

    def unregister(self, container_name: str):
        """헬스체크 해제"""
        self.checks.pop(container_name, None)
        logger.info(f"Health check unregistered: {container_name}")

    def check_container(self, health_check: HealthCheck) -> bool:
        """단일 컨테이너 헬스체크 수행"""
        try:
            if health_check.check_type == "status":
                return self._check_status(health_check)
            elif health_check.check_type == "http":
                return self._check_http(health_check)
            elif health_check.check_type == "tcp":
                return self._check_tcp(health_check)
            else:
                logger.warning(f"Unknown check type: {health_check.check_type}")
                return False
        except Exception as e:
            logger.error(f"Health check error for {health_check.container_name}: {e}")
            return False

    def _check_status(self, hc: HealthCheck) -> bool:
        """Docker 상태 기반 헬스체크"""
        status = self.manager.get_status(hc.container_name)
        if status is None:
            return False
        return status["status"] == "running"

    def _check_http(self, hc: HealthCheck) -> bool:
        """HTTP 엔드포인트 기반 헬스체크"""
        if not hc.endpoint:
            logger.warning(f"No endpoint configured for HTTP health check: {hc.container_name}")
            return False
        try:
            resp = requests.get(hc.endpoint, timeout=hc.timeout)
            return resp.status_code == 200
        except requests.RequestException:
            return False

    def _check_tcp(self, hc: HealthCheck) -> bool:
        """TCP 포트 기반 헬스체크"""
        import socket
        if not hc.endpoint:
            return False
        try:
            host, port = hc.endpoint.rsplit(":", 1)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(hc.timeout)
            result = sock.connect_ex((host, int(port)))
            sock.close()
            return result == 0
        except (ValueError, socket.error):
            return False

    def _handle_failure(self, hc: HealthCheck):
        """장애 처리 - 자동 복구"""
        hc.failure_count += 1
        logger.warning(f"Health check failed for {hc.container_name} "
                      f"({hc.failure_count}/{hc.retries})")

        if hc.failure_count >= hc.retries:
            logger.error(f"Container unhealthy, attempting restart: {hc.container_name}")
            hc.healthy = False

            success = self.manager.restart(hc.container_name)
            if success:
                logger.info(f"Container restarted successfully: {hc.container_name}")
                hc.failure_count = 0
                time.sleep(10)
            else:
                logger.error(f"Failed to restart container: {hc.container_name}")

            if self.db:
                self.db.log_event(
                    container_name=hc.container_name,
                    event_type="auto_restart" if success else "restart_failed",
                    details=f"Failure count: {hc.failure_count}"
                )

    def _handle_recovery(self, hc: HealthCheck):
        """복구 확인"""
        if not hc.healthy:
            logger.info(f"Container recovered: {hc.container_name}")
            hc.healthy = True
        hc.failure_count = 0

    def run_checks(self):
        """모든 등록된 헬스체크 1회 실행"""
        results = {}
        for name, hc in self.checks.items():
            healthy = self.check_container(hc)
            hc.last_check = time.time()

            if healthy:
                self._handle_recovery(hc)
            else:
                self._handle_failure(hc)

            results[name] = {
                "healthy": healthy,
                "failure_count": hc.failure_count,
                "last_check": hc.last_check,
            }
        return results

    def start(self):
        """헬스체크 데몬 시작"""
        if self._running:
            logger.warning("Health checker already running")
            return

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("Health checker started")

    def stop(self):
        """헬스체크 데몬 중지"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Health checker stopped")

    def _loop(self):
        """헬스체크 루프"""
        while self._running:
            self.run_checks()
            min_interval = min(
                (hc.interval for hc in self.checks.values()),
                default=30
            )
            time.sleep(min_interval)
