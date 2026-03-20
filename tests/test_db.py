"""DB 매니저 테스트"""

import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.db_manager import DBManager


@pytest.fixture
def db():
    """테스트용 임시 DB 생성"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    manager = DBManager(db_path=db_path)
    manager.init()
    yield manager

    os.unlink(db_path)


class TestContainerState:
    def test_upsert_container(self, db):
        db.upsert_container("nginx-0", "nginx", "nginx:latest", "running")
        containers = db.get_containers()
        assert len(containers) == 1
        assert containers[0]["name"] == "nginx-0"
        assert containers[0]["status"] == "running"

    def test_upsert_updates_status(self, db):
        db.upsert_container("nginx-0", "nginx", "nginx:latest", "running")
        db.upsert_container("nginx-0", "nginx", "nginx:latest", "exited")
        containers = db.get_containers()
        assert len(containers) == 1
        assert containers[0]["status"] == "exited"

    def test_filter_by_service(self, db):
        db.upsert_container("nginx-0", "nginx", "nginx:latest", "running")
        db.upsert_container("redis-0", "redis", "redis:latest", "running")
        containers = db.get_containers(service="nginx")
        assert len(containers) == 1
        assert containers[0]["service"] == "nginx"

    def test_filter_by_status(self, db):
        db.upsert_container("nginx-0", "nginx", "nginx:latest", "running")
        db.upsert_container("redis-0", "redis", "redis:latest", "exited")
        containers = db.get_containers(status="running")
        assert len(containers) == 1


class TestEvents:
    def test_log_event(self, db):
        db.log_event("nginx-0", "deploy", "replicas=2")
        events = db.get_events()
        assert len(events) == 1
        assert events[0]["event_type"] == "deploy"

    def test_filter_events(self, db):
        db.log_event("nginx-0", "deploy", "v1")
        db.log_event("nginx-0", "scale_up", "1->2")
        db.log_event("redis-0", "deploy", "v1")

        nginx_events = db.get_events(container_name="nginx-0")
        assert len(nginx_events) == 2

        deploy_events = db.get_events(event_type="deploy")
        assert len(deploy_events) == 2


class TestMetrics:
    def test_save_and_get_metrics(self, db):
        db.save_metric("nginx-0", 25.5, 128.0, 50.0, 1024, 512)
        db.save_metric("nginx-0", 30.0, 140.0, 55.0, 2048, 1024)

        metrics = db.get_metrics("nginx-0")
        assert len(metrics) == 2

    def test_metric_avg(self, db):
        for i in range(5):
            db.save_metric("nginx-0", 20.0 + i, 100.0, 40.0 + i)

        avg = db.get_metric_avg("nginx-0", minutes=5)
        assert avg["sample_count"] == 5
        assert avg["avg_cpu"] is not None


class TestPipeline:
    def test_create_pipeline_run(self, db):
        run_id = db.create_pipeline_run("pipe-001", "myapp", "v1.0", "build")
        assert run_id is not None

        history = db.get_pipeline_history("myapp")
        assert len(history) == 1
        assert history[0]["status"] == "running"

    def test_update_pipeline_run(self, db):
        run_id = db.create_pipeline_run("pipe-001", "myapp", "v1.0", "build")
        db.update_pipeline_run(run_id, "success", "Build OK", 30)

        history = db.get_pipeline_history("myapp")
        assert history[0]["status"] == "success"
        assert history[0]["duration_s"] == 30


class TestDeployments:
    def test_create_deployment(self, db):
        dep_id = db.create_deployment("nginx", "nginx:1.25", "v1.25", 2, "dev")
        assert dep_id is not None

        last = db.get_last_deployment("nginx")
        assert last is not None
        assert last["version"] == "v1.25"

    def test_rollback_deployment(self, db):
        dep_id = db.create_deployment("nginx", "nginx:1.25", "v1.25", 2)
        db.mark_rollback(dep_id)

        last = db.get_last_deployment("nginx")
        assert last is None  # 롤백된 배포는 조회되지 않음


class TestAlerts:
    def test_create_and_resolve_alert(self, db):
        alert_id = db.create_alert("nginx-0", "cpu_critical", "critical", "CPU 95%")
        active = db.get_active_alerts()
        assert len(active) == 1

        db.resolve_alert(alert_id)
        active = db.get_active_alerts()
        assert len(active) == 0

    def test_multiple_alerts(self, db):
        db.create_alert("nginx-0", "cpu_warning", "warning", "CPU 82%")
        db.create_alert("redis-0", "memory_critical", "critical", "Memory 95%")

        active = db.get_active_alerts()
        assert len(active) == 2
