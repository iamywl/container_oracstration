"""알림 매니저 - Slack/Email 연동 알림 시스템"""

import json
import logging
import smtplib
from email.mime.text import MIMEText
from typing import Optional
from db.db_manager import DBManager

logger = logging.getLogger(__name__)


class AlertManager:
    """알림 매니저

    컨테이너 이상 탐지 시 Slack webhook, Email 등으로 알림을 발송하고
    알림 이력을 DB에 저장한다. 중복 알림 방지(dedup) 기능 포함.
    """

    def __init__(self, db_manager: DBManager, config: dict = None):
        self.db = db_manager
        self.config = config or {}
        self.slack_webhook = self.config.get("slack_webhook")
        self.email_config = self.config.get("email")

        # 중복 알림 방지: {container_name:alert_type -> last_fired_time}
        self._dedup_cache: dict[str, float] = {}
        self.dedup_interval = self.config.get("dedup_interval", 300)  # 5분

    def fire(self, container_name: str, alert_type: str,
             severity: str, message: str):
        """알림 발생"""
        import time

        # 중복 체크
        dedup_key = f"{container_name}:{alert_type}"
        now = time.time()
        last_fired = self._dedup_cache.get(dedup_key, 0)

        if now - last_fired < self.dedup_interval:
            logger.debug(f"Dedup: skipping alert {dedup_key}")
            return

        self._dedup_cache[dedup_key] = now

        # DB 저장
        alert_id = self.db.create_alert(
            container_name=container_name,
            alert_type=alert_type,
            severity=severity,
            message=message,
        )

        logger.warning(f"ALERT [{severity}] {container_name}: {message}")

        # 채널별 발송
        if severity == "critical":
            self._send_slack(container_name, alert_type, severity, message)
            self._send_email(container_name, alert_type, severity, message)
        elif severity == "warning":
            self._send_slack(container_name, alert_type, severity, message)

    def _send_slack(self, container_name: str, alert_type: str,
                    severity: str, message: str):
        """Slack webhook 알림 발송"""
        if not self.slack_webhook:
            return

        try:
            import requests

            severity_emoji = {
                "critical": ":rotating_light:",
                "warning": ":warning:",
                "info": ":information_source:",
            }

            payload = {
                "text": (
                    f"{severity_emoji.get(severity, ':bell:')} "
                    f"*[{severity.upper()}]* `{container_name}`\n"
                    f"Type: {alert_type}\n"
                    f"Message: {message}"
                )
            }

            resp = requests.post(
                self.slack_webhook,
                json=payload,
                timeout=5,
            )
            if resp.status_code == 200:
                logger.info(f"Slack alert sent: {container_name}")
            else:
                logger.error(f"Slack alert failed: {resp.status_code}")

        except Exception as e:
            logger.error(f"Slack notification error: {e}")

    def _send_email(self, container_name: str, alert_type: str,
                    severity: str, message: str):
        """Email 알림 발송"""
        if not self.email_config:
            return

        try:
            subject = f"[{severity.upper()}] Container Alert: {container_name}"
            body = (
                f"Container: {container_name}\n"
                f"Alert Type: {alert_type}\n"
                f"Severity: {severity}\n"
                f"Message: {message}\n"
            )

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.email_config["from"]
            msg["To"] = self.email_config["to"]

            with smtplib.SMTP(
                self.email_config["smtp_host"],
                self.email_config.get("smtp_port", 587)
            ) as server:
                server.starttls()
                server.login(
                    self.email_config["username"],
                    self.email_config["password"],
                )
                server.send_message(msg)

            logger.info(f"Email alert sent: {container_name}")

        except Exception as e:
            logger.error(f"Email notification error: {e}")

    def resolve(self, container_name: str, alert_type: str):
        """알림 해결 처리"""
        active = self.db.get_active_alerts()
        for alert in active:
            if (alert["container_name"] == container_name and
                    alert["alert_type"] == alert_type):
                self.db.resolve_alert(alert["id"])
                logger.info(f"Alert resolved: {container_name} - {alert_type}")

        dedup_key = f"{container_name}:{alert_type}"
        self._dedup_cache.pop(dedup_key, None)

    def get_active_alerts(self) -> list[dict]:
        """활성 알림 목록"""
        return self.db.get_active_alerts()

    def get_summary(self) -> dict:
        """알림 요약"""
        active = self.db.get_active_alerts()
        return {
            "total_active": len(active),
            "critical": sum(1 for a in active if a["severity"] == "critical"),
            "warning": sum(1 for a in active if a["severity"] == "warning"),
            "alerts": active,
        }
