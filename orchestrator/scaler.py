"""컨테이너 오토 스케일링 모듈"""

import logging
import time
import threading
from typing import Optional
from orchestrator.container import ContainerManager, ContainerConfig

logger = logging.getLogger(__name__)


class ScalingPolicy:
    """스케일링 정책 정의"""
    def __init__(self, service_name: str, min_replicas: int = 1,
                 max_replicas: int = 10, cpu_threshold: float = 80.0,
                 memory_threshold: float = 80.0, cooldown: int = 60,
                 scale_up_step: int = 1, scale_down_step: int = 1):
        self.service_name = service_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.cooldown = cooldown
        self.scale_up_step = scale_up_step
        self.scale_down_step = scale_down_step
        self.last_scale_time = 0


class AutoScaler:
    """CPU/메모리 기반 오토 스케일러"""

    def __init__(self, container_manager: ContainerManager, db_manager=None):
        self.manager = container_manager
        self.db = db_manager
        self.policies: dict[str, ScalingPolicy] = {}
        self.service_configs: dict[str, ContainerConfig] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def register_policy(self, policy: ScalingPolicy, config: ContainerConfig):
        """스케일링 정책 등록"""
        self.policies[policy.service_name] = policy
        self.service_configs[policy.service_name] = config
        logger.info(f"Scaling policy registered: {policy.service_name} "
                    f"(min={policy.min_replicas}, max={policy.max_replicas})")

    def get_replicas(self, service_name: str) -> list[str]:
        """서비스의 현재 레플리카 목록 조회"""
        containers = self.manager.list_managed()
        return [
            c["name"] for c in containers
            if c["service"] == service_name and c["status"] == "running"
        ]

    def get_avg_metrics(self, service_name: str) -> dict:
        """서비스의 평균 메트릭 조회"""
        replicas = self.get_replicas(service_name)
        if not replicas:
            return {"cpu_percent": 0, "memory_percent": 0}

        total_cpu = 0.0
        total_mem = 0.0
        count = 0

        for replica_name in replicas:
            stats = self.manager.get_stats(replica_name)
            if stats:
                total_cpu += stats["cpu_percent"]
                total_mem += stats["memory_percent"]
                count += 1

        if count == 0:
            return {"cpu_percent": 0, "memory_percent": 0}

        return {
            "cpu_percent": round(total_cpu / count, 2),
            "memory_percent": round(total_mem / count, 2),
        }

    def scale_to(self, service_name: str, target_replicas: int) -> bool:
        """지정된 수의 레플리카로 스케일링"""
        policy = self.policies.get(service_name)
        config = self.service_configs.get(service_name)

        if not policy or not config:
            logger.error(f"No policy or config for service: {service_name}")
            return False

        target_replicas = max(policy.min_replicas, min(policy.max_replicas, target_replicas))
        current_replicas = self.get_replicas(service_name)
        current_count = len(current_replicas)

        if target_replicas == current_count:
            logger.info(f"Already at target replicas: {service_name} ({current_count})")
            return True

        if target_replicas > current_count:
            return self._scale_up(service_name, config, current_count, target_replicas)
        else:
            return self._scale_down(service_name, current_replicas, current_count, target_replicas)

    def _scale_up(self, service_name: str, config: ContainerConfig,
                  current: int, target: int) -> bool:
        """스케일 아웃"""
        logger.info(f"Scaling up {service_name}: {current} -> {target}")

        for i in range(current, target):
            replica_config = ContainerConfig(
                name=f"{service_name}-{i}",
                image=config.image,
                ports=config.ports,
                environment=config.environment,
                volumes=config.volumes,
                network=config.network,
                labels={**(config.labels or {}), "orchestrator.replica": str(i)},
                cpu_limit=config.cpu_limit,
                memory_limit=config.memory_limit,
            )
            try:
                self.manager.create(replica_config)
            except Exception as e:
                logger.error(f"Failed to create replica {service_name}-{i}: {e}")
                return False

        if self.db:
            self.db.log_event(
                container_name=service_name,
                event_type="scale_up",
                details=f"{current} -> {target}"
            )
        return True

    def _scale_down(self, service_name: str, replicas: list[str],
                    current: int, target: int) -> bool:
        """스케일 인"""
        logger.info(f"Scaling down {service_name}: {current} -> {target}")

        to_remove = replicas[target:]
        for name in to_remove:
            try:
                self.manager.stop(name)
                self.manager.remove(name)
            except Exception as e:
                logger.error(f"Failed to remove replica {name}: {e}")
                return False

        if self.db:
            self.db.log_event(
                container_name=service_name,
                event_type="scale_down",
                details=f"{current} -> {target}"
            )
        return True

    def evaluate(self, service_name: str) -> Optional[str]:
        """스케일링 필요 여부 평가"""
        policy = self.policies.get(service_name)
        if not policy:
            return None

        now = time.time()
        if now - policy.last_scale_time < policy.cooldown:
            return None

        metrics = self.get_avg_metrics(service_name)
        current_count = len(self.get_replicas(service_name))

        if (metrics["cpu_percent"] > policy.cpu_threshold or
                metrics["memory_percent"] > policy.memory_threshold):
            target = min(current_count + policy.scale_up_step, policy.max_replicas)
            if target > current_count:
                self.scale_to(service_name, target)
                policy.last_scale_time = now
                return "scale_up"

        elif (metrics["cpu_percent"] < policy.cpu_threshold * 0.5 and
              metrics["memory_percent"] < policy.memory_threshold * 0.5):
            target = max(current_count - policy.scale_down_step, policy.min_replicas)
            if target < current_count:
                self.scale_to(service_name, target)
                policy.last_scale_time = now
                return "scale_down"

        return None

    def start(self, interval: int = 30):
        """오토 스케일러 데몬 시작"""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._loop, args=(interval,), daemon=True
        )
        self._thread.start()
        logger.info("Auto scaler started")

    def stop(self):
        """오토 스케일러 데몬 중지"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Auto scaler stopped")

    def _loop(self, interval: int):
        """스케일링 평가 루프"""
        while self._running:
            for service_name in list(self.policies.keys()):
                self.evaluate(service_name)
            time.sleep(interval)
