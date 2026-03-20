"""컨테이너 라이프사이클 관리 모듈"""

import docker
from docker.errors import NotFound, APIError
from dataclasses import dataclass
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)


@dataclass
class ContainerConfig:
    name: str
    image: str
    ports: Optional[dict] = None
    environment: Optional[dict] = None
    volumes: Optional[dict] = None
    network: Optional[str] = None
    restart_policy: Optional[dict] = None
    labels: Optional[dict] = None
    cpu_limit: Optional[float] = None
    memory_limit: Optional[str] = None


class ContainerManager:
    """Docker 컨테이너 라이프사이클 관리"""

    def __init__(self):
        self.client = docker.from_env()
        self.label_prefix = "orchestrator"

    def create(self, config: ContainerConfig) -> docker.models.containers.Container:
        """컨테이너 생성 및 시작"""
        labels = config.labels or {}
        labels[f"{self.label_prefix}.managed"] = "true"
        labels[f"{self.label_prefix}.service"] = config.name

        kwargs = {
            "image": config.image,
            "name": config.name,
            "detach": True,
            "labels": labels,
        }

        if config.ports:
            kwargs["ports"] = config.ports
        if config.environment:
            kwargs["environment"] = config.environment
        if config.volumes:
            kwargs["volumes"] = config.volumes
        if config.network:
            kwargs["network"] = config.network
        if config.restart_policy:
            kwargs["restart_policy"] = config.restart_policy
        if config.cpu_limit:
            kwargs["nano_cpus"] = int(config.cpu_limit * 1e9)
        if config.memory_limit:
            kwargs["mem_limit"] = config.memory_limit

        try:
            self.client.images.pull(config.image)
            logger.info(f"Image pulled: {config.image}")
        except APIError as e:
            logger.warning(f"Failed to pull image {config.image}: {e}")

        container = self.client.containers.run(**kwargs)
        logger.info(f"Container created: {config.name} ({container.short_id})")
        return container

    def stop(self, name: str, timeout: int = 10) -> bool:
        """컨테이너 중지"""
        try:
            container = self.client.containers.get(name)
            container.stop(timeout=timeout)
            logger.info(f"Container stopped: {name}")
            return True
        except NotFound:
            logger.warning(f"Container not found: {name}")
            return False

    def remove(self, name: str, force: bool = False) -> bool:
        """컨테이너 삭제"""
        try:
            container = self.client.containers.get(name)
            container.remove(force=force)
            logger.info(f"Container removed: {name}")
            return True
        except NotFound:
            logger.warning(f"Container not found: {name}")
            return False

    def restart(self, name: str, timeout: int = 10) -> bool:
        """컨테이너 재시작"""
        try:
            container = self.client.containers.get(name)
            container.restart(timeout=timeout)
            logger.info(f"Container restarted: {name}")
            return True
        except NotFound:
            logger.warning(f"Container not found: {name}")
            return False

    def get_status(self, name: str) -> Optional[dict]:
        """컨테이너 상태 조회"""
        try:
            container = self.client.containers.get(name)
            return {
                "id": container.short_id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "created": container.attrs["Created"],
                "ports": container.ports,
            }
        except NotFound:
            return None

    def list_managed(self) -> list[dict]:
        """관리 중인 컨테이너 목록 조회"""
        containers = self.client.containers.list(
            all=True,
            filters={"label": f"{self.label_prefix}.managed=true"},
        )
        return [
            {
                "id": c.short_id,
                "name": c.name,
                "status": c.status,
                "image": c.image.tags[0] if c.image.tags else "unknown",
                "service": c.labels.get(f"{self.label_prefix}.service", "unknown"),
            }
            for c in containers
        ]

    def get_logs(self, name: str, tail: int = 100) -> Optional[str]:
        """컨테이너 로그 조회"""
        try:
            container = self.client.containers.get(name)
            return container.logs(tail=tail).decode("utf-8")
        except NotFound:
            return None

    def get_stats(self, name: str) -> Optional[dict]:
        """컨테이너 리소스 사용량 조회"""
        try:
            container = self.client.containers.get(name)
            stats = container.stats(stream=False)

            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                        stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                          stats["precpu_stats"]["system_cpu_usage"]
            num_cpus = stats["cpu_stats"]["online_cpus"]
            cpu_percent = (cpu_delta / system_delta) * num_cpus * 100.0 if system_delta > 0 else 0.0

            memory_usage = stats["memory_stats"].get("usage", 0)
            memory_limit = stats["memory_stats"].get("limit", 1)
            memory_percent = (memory_usage / memory_limit) * 100.0

            return {
                "cpu_percent": round(cpu_percent, 2),
                "memory_usage_mb": round(memory_usage / (1024 * 1024), 2),
                "memory_limit_mb": round(memory_limit / (1024 * 1024), 2),
                "memory_percent": round(memory_percent, 2),
                "network_rx_bytes": stats.get("networks", {}).get("eth0", {}).get("rx_bytes", 0),
                "network_tx_bytes": stats.get("networks", {}).get("eth0", {}).get("tx_bytes", 0),
            }
        except (NotFound, KeyError):
            return None

    def rolling_update(self, service_name: str, new_image: str, replicas: list[str]) -> bool:
        """롤링 업데이트 수행"""
        logger.info(f"Starting rolling update for {service_name} to {new_image}")

        for replica_name in replicas:
            try:
                old_container = self.client.containers.get(replica_name)
                old_labels = old_container.labels.copy()
                old_env = old_container.attrs["Config"].get("Env", [])

                # 새 컨테이너 시작
                temp_name = f"{replica_name}_new"
                new_container = self.client.containers.run(
                    image=new_image,
                    name=temp_name,
                    detach=True,
                    labels=old_labels,
                    environment=old_env,
                )

                # 헬스체크 대기
                time.sleep(5)
                new_container.reload()
                if new_container.status != "running":
                    logger.error(f"New container {temp_name} failed to start, rolling back")
                    new_container.remove(force=True)
                    return False

                # 기존 컨테이너 제거 후 이름 변경
                old_container.stop(timeout=10)
                old_container.remove()
                new_container.rename(replica_name)

                logger.info(f"Updated replica: {replica_name}")

            except Exception as e:
                logger.error(f"Rolling update failed at {replica_name}: {e}")
                return False

        logger.info(f"Rolling update completed for {service_name}")
        return True
