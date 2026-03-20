"""모니터링 시스템 테스트"""

import os
import sys
import tempfile
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from monitoring.collector import MetricCollector
from monitoring.alerting.alert_manager import AlertManager
from db.db_manager import DBManager


@pytest.fixture
def db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    manager = DBManager(db_path=db_path)
    manager.init()
    yield manager
    os.unlink(db_path)


class TestMetricCollector:
    def test_threshold_defaults(self):
        mock_mgr = MagicMock()
        mock_db = MagicMock()
        collector = MetricCollector(mock_mgr, mock_db, interval=10)

        assert collector.thresholds["cpu_critical"] == 90.0
        assert collector.thresholds["cpu_warning"] == 80.0

    def test_set_thresholds(self):
        mock_mgr = MagicMock()
        mock_db = MagicMock()
        collector = MetricCollector(mock_mgr, mock_db)
        collector.set_thresholds(cpu_critical=95.0)

        assert collector.thresholds["cpu_critical"] == 95.0

    def test_collect_skips_non_running(self):
        mock_mgr = MagicMock()
        mock_mgr.list_managed.return_value = [
            {"name": "nginx-0", "service": "nginx", "status": "exited"},
        ]
        mock_db = MagicMock()

        collector = MetricCollector(mock_mgr, mock_db)
        results = collector.collect_once()

        assert len(results) == 0
        mock_mgr.get_stats.assert_not_called()

    def test_collect_saves_metrics(self):
        mock_mgr = MagicMock()
        mock_mgr.list_managed.return_value = [
            {"name": "nginx-0", "service": "nginx", "status": "running"},
        ]
        mock_mgr.get_stats.return_value = {
            "cpu_percent": 25.0,
            "memory_usage_mb": 128.0,
            "memory_percent": 50.0,
            "network_rx_bytes": 1024,
            "network_tx_bytes": 512,
        }
        mock_db = MagicMock()

        collector = MetricCollector(mock_mgr, mock_db)
        results = collector.collect_once()

        assert len(results) == 1
        mock_db.save_metric.assert_called_once()

    def test_collect_triggers_alert_on_high_cpu(self):
        mock_mgr = MagicMock()
        mock_mgr.list_managed.return_value = [
            {"name": "nginx-0", "service": "nginx", "status": "running"},
        ]
        mock_mgr.get_stats.return_value = {
            "cpu_percent": 95.0,
            "memory_usage_mb": 128.0,
            "memory_percent": 50.0,
            "network_rx_bytes": 0,
            "network_tx_bytes": 0,
        }
        mock_db = MagicMock()
        mock_alert = MagicMock()

        collector = MetricCollector(mock_mgr, mock_db, alert_manager=mock_alert)
        collector.collect_once()

        mock_alert.fire.assert_called_once()
        call_args = mock_alert.fire.call_args
        assert call_args[1]["severity"] == "critical"


class TestAlertManager:
    def test_fire_alert(self, db):
        alert_mgr = AlertManager(db)
        alert_mgr.fire("nginx-0", "cpu_critical", "critical", "CPU 95%")

        active = db.get_active_alerts()
        assert len(active) == 1
        assert active[0]["severity"] == "critical"

    def test_dedup_alerts(self, db):
        alert_mgr = AlertManager(db, config={"dedup_interval": 300})
        alert_mgr.fire("nginx-0", "cpu_warning", "warning", "CPU 82%")
        alert_mgr.fire("nginx-0", "cpu_warning", "warning", "CPU 85%")

        # 중복 억제로 1개만 저장
        active = db.get_active_alerts()
        assert len(active) == 1

    def test_resolve_alert(self, db):
        alert_mgr = AlertManager(db)
        alert_mgr.fire("nginx-0", "cpu_critical", "critical", "CPU 95%")

        assert len(db.get_active_alerts()) == 1

        alert_mgr.resolve("nginx-0", "cpu_critical")
        assert len(db.get_active_alerts()) == 0

    def test_alert_summary(self, db):
        alert_mgr = AlertManager(db)
        alert_mgr.fire("nginx-0", "cpu_critical", "critical", "CPU 95%")
        alert_mgr.fire("redis-0", "memory_warning", "warning", "Memory 82%")

        summary = alert_mgr.get_summary()
        assert summary["total_active"] == 2
        assert summary["critical"] == 1
        assert summary["warning"] == 1
