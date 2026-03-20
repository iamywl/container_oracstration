"""오케스트레이션 엔진 테스트"""

import os
import sys
import tempfile
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from orchestrator.container import ContainerConfig
from orchestrator.health_checker import HealthCheck, HealthChecker
from orchestrator.scaler import ScalingPolicy, AutoScaler


class TestContainerConfig:
    def test_default_config(self):
        config = ContainerConfig(name="test", image="nginx:latest")
        assert config.name == "test"
        assert config.image == "nginx:latest"
        assert config.ports is None
        assert config.cpu_limit is None

    def test_full_config(self):
        config = ContainerConfig(
            name="web-0",
            image="nginx:latest",
            ports={"80/tcp": 8080},
            environment={"ENV": "prod"},
            cpu_limit=0.5,
            memory_limit="256m",
        )
        assert config.ports == {"80/tcp": 8080}
        assert config.cpu_limit == 0.5


class TestHealthCheck:
    def test_health_check_defaults(self):
        hc = HealthCheck(container_name="test")
        assert hc.check_type == "status"
        assert hc.interval == 30
        assert hc.retries == 3
        assert hc.healthy is True

    def test_http_health_check(self):
        hc = HealthCheck(
            container_name="web",
            check_type="http",
            endpoint="http://localhost:8080/health",
            interval=10,
        )
        assert hc.check_type == "http"
        assert hc.endpoint == "http://localhost:8080/health"


class TestHealthChecker:
    def test_register_and_unregister(self):
        mock_mgr = MagicMock()
        checker = HealthChecker(mock_mgr)

        hc = HealthCheck(container_name="nginx-0")
        checker.register(hc)
        assert "nginx-0" in checker.checks

        checker.unregister("nginx-0")
        assert "nginx-0" not in checker.checks

    def test_status_check_running(self):
        mock_mgr = MagicMock()
        mock_mgr.get_status.return_value = {"status": "running"}

        checker = HealthChecker(mock_mgr)
        hc = HealthCheck(container_name="nginx-0", check_type="status")
        result = checker.check_container(hc)
        assert result is True

    def test_status_check_stopped(self):
        mock_mgr = MagicMock()
        mock_mgr.get_status.return_value = {"status": "exited"}

        checker = HealthChecker(mock_mgr)
        hc = HealthCheck(container_name="nginx-0", check_type="status")
        result = checker.check_container(hc)
        assert result is False

    def test_status_check_not_found(self):
        mock_mgr = MagicMock()
        mock_mgr.get_status.return_value = None

        checker = HealthChecker(mock_mgr)
        hc = HealthCheck(container_name="nginx-0", check_type="status")
        result = checker.check_container(hc)
        assert result is False

    def test_failure_count_increments(self):
        mock_mgr = MagicMock()
        mock_mgr.get_status.return_value = None

        checker = HealthChecker(mock_mgr)
        hc = HealthCheck(container_name="nginx-0", retries=3)
        checker.register(hc)

        # 1차 실패
        checker.run_checks()
        assert hc.failure_count == 1
        assert hc.healthy is True  # 아직 retries 미도달

    def test_auto_restart_after_retries(self):
        mock_mgr = MagicMock()
        mock_mgr.get_status.return_value = None
        mock_mgr.restart.return_value = True

        checker = HealthChecker(mock_mgr)
        hc = HealthCheck(container_name="nginx-0", retries=2)
        checker.register(hc)

        # retries 횟수만큼 실패
        hc.failure_count = 1
        checker.run_checks()

        # 자동 재시작 호출 확인
        mock_mgr.restart.assert_called_once_with("nginx-0")


class TestScalingPolicy:
    def test_default_policy(self):
        policy = ScalingPolicy(service_name="nginx")
        assert policy.min_replicas == 1
        assert policy.max_replicas == 10
        assert policy.cpu_threshold == 80.0

    def test_custom_policy(self):
        policy = ScalingPolicy(
            service_name="web",
            min_replicas=2,
            max_replicas=20,
            cpu_threshold=70.0,
            cooldown=120,
        )
        assert policy.min_replicas == 2
        assert policy.max_replicas == 20


class TestAutoScaler:
    def test_register_policy(self):
        mock_mgr = MagicMock()
        scaler = AutoScaler(mock_mgr)

        policy = ScalingPolicy(service_name="nginx")
        config = ContainerConfig(name="nginx", image="nginx:latest")
        scaler.register_policy(policy, config)

        assert "nginx" in scaler.policies

    def test_get_replicas(self):
        mock_mgr = MagicMock()
        mock_mgr.list_managed.return_value = [
            {"name": "nginx-0", "service": "nginx", "status": "running"},
            {"name": "nginx-1", "service": "nginx", "status": "running"},
            {"name": "redis-0", "service": "redis", "status": "running"},
        ]

        scaler = AutoScaler(mock_mgr)
        replicas = scaler.get_replicas("nginx")
        assert len(replicas) == 2
