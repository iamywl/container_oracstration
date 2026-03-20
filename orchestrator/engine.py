"""오케스트레이션 코어 엔진"""

import yaml
import logging
from pathlib import Path
from orchestrator.container import ContainerManager, ContainerConfig
from orchestrator.health_checker import HealthChecker, HealthCheck
from orchestrator.scaler import AutoScaler, ScalingPolicy

logger = logging.getLogger(__name__)


class OrchestrationEngine:
    """컨테이너 오케스트레이션 코어 엔진

    서비스 정의(YAML)를 기반으로 컨테이너 배포, 헬스체크, 오토 스케일링을 통합 관리
    """

    def __init__(self, db_manager=None):
        self.container_mgr = ContainerManager()
        self.health_checker = HealthChecker(self.container_mgr, db_manager)
        self.auto_scaler = AutoScaler(self.container_mgr, db_manager)
        self.db = db_manager
        self.services: dict[str, dict] = {}

    def load_service_definition(self, yaml_path: str) -> dict:
        """YAML 서비스 정의 파일 로드"""
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"Service definition not found: {yaml_path}")

        with open(path) as f:
            definition = yaml.safe_load(f)

        logger.info(f"Loaded service definition: {yaml_path}")
        return definition

    def deploy(self, yaml_path: str) -> list[str]:
        """서비스 정의를 기반으로 컨테이너 배포"""
        definition = self.load_service_definition(yaml_path)
        deployed = []

        services = definition.get("services", {})
        for svc_name, svc_config in services.items():
            replicas = svc_config.get("replicas", 1)
            logger.info(f"Deploying service: {svc_name} (replicas={replicas})")

            container_config = ContainerConfig(
                name=svc_name,
                image=svc_config["image"],
                ports=svc_config.get("ports"),
                environment=svc_config.get("environment"),
                volumes=svc_config.get("volumes"),
                network=svc_config.get("network"),
                cpu_limit=svc_config.get("cpu_limit"),
                memory_limit=svc_config.get("memory_limit"),
                labels=svc_config.get("labels", {}),
            )

            # 멀티 레플리카 배포
            for i in range(replicas):
                replica_name = f"{svc_name}-{i}" if replicas > 1 else svc_name
                replica_config = ContainerConfig(
                    name=replica_name,
                    image=container_config.image,
                    ports=container_config.ports,
                    environment=container_config.environment,
                    volumes=container_config.volumes,
                    network=container_config.network,
                    cpu_limit=container_config.cpu_limit,
                    memory_limit=container_config.memory_limit,
                    labels={
                        **(container_config.labels or {}),
                        "orchestrator.replica": str(i),
                    },
                )
                try:
                    self.container_mgr.create(replica_config)
                    deployed.append(replica_name)
                except Exception as e:
                    logger.error(f"Failed to deploy {replica_name}: {e}")

            # 헬스체크 등록
            health_config = svc_config.get("health_check", {})
            if health_config:
                for replica_name in deployed:
                    if replica_name.startswith(svc_name):
                        hc = HealthCheck(
                            container_name=replica_name,
                            check_type=health_config.get("type", "status"),
                            endpoint=health_config.get("endpoint"),
                            interval=health_config.get("interval", 30),
                            timeout=health_config.get("timeout", 5),
                            retries=health_config.get("retries", 3),
                        )
                        self.health_checker.register(hc)

            # 오토 스케일링 정책 등록
            scaling_config = svc_config.get("scaling", {})
            if scaling_config:
                policy = ScalingPolicy(
                    service_name=svc_name,
                    min_replicas=scaling_config.get("min_replicas", 1),
                    max_replicas=scaling_config.get("max_replicas", 10),
                    cpu_threshold=scaling_config.get("cpu_threshold", 80.0),
                    memory_threshold=scaling_config.get("memory_threshold", 80.0),
                    cooldown=scaling_config.get("cooldown", 60),
                )
                self.auto_scaler.register_policy(policy, container_config)

            self.services[svc_name] = svc_config

            if self.db:
                self.db.log_event(
                    container_name=svc_name,
                    event_type="deploy",
                    details=f"replicas={replicas}, image={svc_config['image']}"
                )

        return deployed

    def undeploy(self, service_name: str) -> bool:
        """서비스 제거"""
        containers = self.container_mgr.list_managed()
        removed = False

        for c in containers:
            if c["service"] == service_name:
                self.health_checker.unregister(c["name"])
                self.container_mgr.stop(c["name"])
                self.container_mgr.remove(c["name"])
                removed = True

        if removed:
            self.services.pop(service_name, None)
            logger.info(f"Service undeployed: {service_name}")

            if self.db:
                self.db.log_event(
                    container_name=service_name,
                    event_type="undeploy",
                    details="Service removed"
                )

        return removed

    def scale(self, service_name: str, replicas: int) -> bool:
        """서비스 수동 스케일링"""
        config = self.services.get(service_name)
        if not config:
            logger.error(f"Service not found: {service_name}")
            return False

        container_config = ContainerConfig(
            name=service_name,
            image=config["image"],
            ports=config.get("ports"),
            environment=config.get("environment"),
            network=config.get("network"),
            cpu_limit=config.get("cpu_limit"),
            memory_limit=config.get("memory_limit"),
        )

        if service_name not in self.auto_scaler.policies:
            policy = ScalingPolicy(service_name=service_name)
            self.auto_scaler.register_policy(policy, container_config)

        return self.auto_scaler.scale_to(service_name, replicas)

    def get_status(self) -> dict:
        """전체 플랫폼 상태 조회"""
        containers = self.container_mgr.list_managed()
        health_results = self.health_checker.run_checks()

        return {
            "total_containers": len(containers),
            "running": sum(1 for c in containers if c["status"] == "running"),
            "stopped": sum(1 for c in containers if c["status"] != "running"),
            "containers": containers,
            "health": health_results,
            "services": list(self.services.keys()),
        }

    def start_daemons(self):
        """헬스체크 및 오토 스케일러 데몬 시작"""
        self.health_checker.start()
        self.auto_scaler.start()
        logger.info("All daemons started")

    def stop_daemons(self):
        """데몬 중지"""
        self.health_checker.stop()
        self.auto_scaler.stop()
        logger.info("All daemons stopped")
