"""MCP 도구 구현 - 컨테이너 플랫폼 운영 도구"""

import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from orchestrator.container import ContainerManager
from orchestrator.engine import OrchestrationEngine
from monitoring.alerting.alert_manager import AlertManager
from db.db_manager import DBManager

logger = logging.getLogger(__name__)


class ContainerTools:
    """MCP 도구 구현체

    각 도구는 컨테이너 플랫폼의 기능을 LLM 에이전트가 사용할 수 있도록 래핑한다.
    """

    def __init__(self):
        self.db = DBManager()
        self.db.init()
        self.engine = OrchestrationEngine(db_manager=self.db)
        self.alert_mgr = AlertManager(self.db)

    def execute(self, tool_name: str, arguments: dict) -> dict:
        """도구 실행 디스패처"""
        handler = getattr(self, f"_tool_{tool_name}", None)
        if handler is None:
            raise ValueError(f"Unknown tool: {tool_name}")
        return handler(arguments)

    def _tool_list_containers(self, args: dict) -> dict:
        """컨테이너 목록 조회"""
        containers = self.engine.container_mgr.list_managed()
        status_filter = args.get("status", "all")

        if status_filter != "all":
            containers = [c for c in containers if c["status"] == status_filter]

        return {
            "total": len(containers),
            "containers": containers,
        }

    def _tool_deploy_service(self, args: dict) -> dict:
        """서비스 배포"""
        yaml_path = args["yaml_path"]
        deployed = self.engine.deploy(yaml_path)
        return {
            "deployed_count": len(deployed),
            "containers": deployed,
            "status": "success",
        }

    def _tool_scale_service(self, args: dict) -> dict:
        """서비스 스케일링"""
        service_name = args["service_name"]
        replicas = args["replicas"]

        current = self.engine.auto_scaler.get_replicas(service_name)
        success = self.engine.scale(service_name, replicas)

        return {
            "service": service_name,
            "previous_replicas": len(current),
            "target_replicas": replicas,
            "success": success,
        }

    def _tool_get_container_stats(self, args: dict) -> dict:
        """컨테이너 리소스 사용량"""
        name = args["container_name"]
        stats = self.engine.container_mgr.get_stats(name)

        if stats is None:
            return {"error": f"Container not found or not running: {name}"}

        # DB에서 트렌드 정보도 가져옴
        avg = self.db.get_metric_avg(name, minutes=5)

        return {
            "container": name,
            "current": stats,
            "avg_5min": avg,
        }

    def _tool_get_container_logs(self, args: dict) -> dict:
        """컨테이너 로그"""
        name = args["container_name"]
        tail = args.get("tail", 50)
        logs = self.engine.container_mgr.get_logs(name, tail=tail)

        if logs is None:
            return {"error": f"Container not found: {name}"}

        return {
            "container": name,
            "log_lines": tail,
            "logs": logs,
        }

    def _tool_health_check(self, args: dict) -> dict:
        """전체 헬스체크"""
        status = self.engine.get_status()
        unhealthy = [
            c for c in status["containers"]
            if c["status"] != "running"
        ]

        return {
            "total": status["total_containers"],
            "running": status["running"],
            "stopped": status["stopped"],
            "unhealthy_containers": unhealthy,
            "all_healthy": len(unhealthy) == 0,
        }

    def _tool_get_alerts(self, args: dict) -> dict:
        """활성 알림 조회"""
        return self.alert_mgr.get_summary()

    def _tool_get_platform_overview(self, args: dict) -> dict:
        """플랫폼 전체 상태 요약"""
        status = self.engine.get_status()
        alerts = self.alert_mgr.get_summary()

        # 최근 이벤트
        events = self.db.get_events(limit=5)

        return {
            "containers": {
                "total": status["total_containers"],
                "running": status["running"],
                "stopped": status["stopped"],
            },
            "services": status["services"],
            "alerts": {
                "total_active": alerts["total_active"],
                "critical": alerts["critical"],
                "warning": alerts["warning"],
            },
            "recent_events": events,
        }

    def _tool_analyze_issue(self, args: dict) -> dict:
        """컨테이너 장애 분석"""
        name = args["container_name"]

        # 컨테이너 상태
        container_status = self.engine.container_mgr.get_status(name)

        # 최근 이벤트
        events = self.db.get_events(container_name=name, limit=10)

        # 로그
        logs = self.engine.container_mgr.get_logs(name, tail=30)

        # 리소스 사용량
        stats = self.engine.container_mgr.get_stats(name)
        avg_metrics = self.db.get_metric_avg(name, minutes=30)

        # 분석 결과 구성
        analysis = {
            "container": name,
            "status": container_status,
            "recent_events": events,
            "recent_logs": logs,
            "current_stats": stats,
            "avg_metrics_30min": avg_metrics,
            "possible_issues": [],
        }

        # 간단한 휴리스틱 분석
        if container_status and container_status["status"] != "running":
            analysis["possible_issues"].append({
                "type": "container_down",
                "description": f"Container is {container_status['status']}",
                "suggestion": "Check logs for error messages, consider restart",
            })

        if stats and stats.get("cpu_percent", 0) > 90:
            analysis["possible_issues"].append({
                "type": "high_cpu",
                "description": f"CPU usage is {stats['cpu_percent']}%",
                "suggestion": "Consider scaling out or optimizing the application",
            })

        if stats and stats.get("memory_percent", 0) > 90:
            analysis["possible_issues"].append({
                "type": "high_memory",
                "description": f"Memory usage is {stats['memory_percent']}%",
                "suggestion": "Check for memory leaks, consider increasing memory limit",
            })

        if logs and "OOMKilled" in logs:
            analysis["possible_issues"].append({
                "type": "oom_killed",
                "description": "Container was killed due to out-of-memory",
                "suggestion": "Increase memory limit or optimize memory usage",
            })

        return analysis

    def _tool_get_deployment_history(self, args: dict) -> dict:
        """배포 이력 조회"""
        service_name = args.get("service_name")
        history = self.db.get_pipeline_history(service_name, limit=10)
        return {
            "service": service_name or "all",
            "history": history,
        }
