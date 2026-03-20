"""메트릭 수집기 - 컨테이너 리소스 모니터링"""

import threading
import time
import logging
from typing import Optional
from orchestrator.container import ContainerManager
from db.db_manager import DBManager

logger = logging.getLogger(__name__)


class MetricCollector:
    """컨테이너 메트릭 수집기

    Docker 컨테이너의 CPU, 메모리, 네트워크 메트릭을 주기적으로 수집하여
    SQLite에 저장한다. 임계치 초과 시 알림 매니저에 전달.
    """

    def __init__(self, container_manager: ContainerManager, db_manager: DBManager,
                 alert_manager=None, interval: int = 15):
        self.container_mgr = container_manager
        self.db = db_manager
        self.alert_mgr = alert_manager
        self.interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None

        # 알림 임계치
        self.thresholds = {
            "cpu_critical": 90.0,
            "cpu_warning": 80.0,
            "memory_critical": 90.0,
            "memory_warning": 80.0,
        }

    def set_thresholds(self, **kwargs):
        """임계치 설정"""
        self.thresholds.update(kwargs)

    def collect_once(self) -> list[dict]:
        """모든 관리 대상 컨테이너 메트릭 1회 수집"""
        containers = self.container_mgr.list_managed()
        results = []

        for c in containers:
            if c["status"] != "running":
                continue

            stats = self.container_mgr.get_stats(c["name"])
            if not stats:
                continue

            # DB 저장
            self.db.save_metric(
                container_name=c["name"],
                cpu_percent=stats["cpu_percent"],
                memory_usage_mb=stats["memory_usage_mb"],
                memory_percent=stats["memory_percent"],
                network_rx=stats["network_rx_bytes"],
                network_tx=stats["network_tx_bytes"],
            )

            # 임계치 체크
            self._check_thresholds(c["name"], stats)

            results.append({
                "name": c["name"],
                "service": c["service"],
                **stats,
            })

        return results

    def _check_thresholds(self, container_name: str, stats: dict):
        """임계치 초과 여부 체크 및 알림 생성"""
        if not self.alert_mgr:
            return

        # CPU 임계치
        if stats["cpu_percent"] >= self.thresholds["cpu_critical"]:
            self.alert_mgr.fire(
                container_name=container_name,
                alert_type="cpu_critical",
                severity="critical",
                message=f"CPU usage {stats['cpu_percent']}% >= {self.thresholds['cpu_critical']}%"
            )
        elif stats["cpu_percent"] >= self.thresholds["cpu_warning"]:
            self.alert_mgr.fire(
                container_name=container_name,
                alert_type="cpu_warning",
                severity="warning",
                message=f"CPU usage {stats['cpu_percent']}% >= {self.thresholds['cpu_warning']}%"
            )

        # 메모리 임계치
        if stats["memory_percent"] >= self.thresholds["memory_critical"]:
            self.alert_mgr.fire(
                container_name=container_name,
                alert_type="memory_critical",
                severity="critical",
                message=f"Memory usage {stats['memory_percent']}% >= {self.thresholds['memory_critical']}%"
            )
        elif stats["memory_percent"] >= self.thresholds["memory_warning"]:
            self.alert_mgr.fire(
                container_name=container_name,
                alert_type="memory_warning",
                severity="warning",
                message=f"Memory usage {stats['memory_percent']}% >= {self.thresholds['memory_warning']}%"
            )

    def get_trend(self, container_name: str, minutes: int = 30) -> dict:
        """메트릭 트렌드 분석"""
        avg = self.db.get_metric_avg(container_name, minutes)
        recent = self.db.get_metrics(container_name, limit=10)

        if not recent:
            return {"trend": "unknown", "avg": avg}

        # 최근 추이 판단 (상승/하락/안정)
        cpu_values = [m["cpu_percent"] for m in recent]
        if len(cpu_values) >= 3:
            recent_avg = sum(cpu_values[:3]) / 3
            older_avg = sum(cpu_values[-3:]) / 3

            if recent_avg > older_avg * 1.2:
                trend = "increasing"
            elif recent_avg < older_avg * 0.8:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "trend": trend,
            "avg": avg,
            "recent_samples": len(recent),
        }

    def start(self):
        """수집기 데몬 시작"""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info(f"Metric collector started (interval={self.interval}s)")

    def stop(self):
        """수집기 데몬 중지"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Metric collector stopped")

    def _loop(self):
        """수집 루프"""
        while self._running:
            try:
                results = self.collect_once()
                logger.debug(f"Collected metrics for {len(results)} containers")
            except Exception as e:
                logger.error(f"Metric collection error: {e}")
            time.sleep(self.interval)
