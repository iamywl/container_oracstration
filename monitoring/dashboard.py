"""터미널 기반 실시간 모니터링 대시보드"""

import time
import logging
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

from orchestrator.container import ContainerManager
from monitoring.collector import MetricCollector
from monitoring.alerting.alert_manager import AlertManager
from db.db_manager import DBManager

logger = logging.getLogger(__name__)
console = Console()


class MonitoringDashboard:
    """터미널 기반 실시간 대시보드

    Rich 라이브러리를 사용하여 컨테이너 상태, 메트릭, 알림을 실시간 표시.
    """

    def __init__(self):
        self.db = DBManager()
        self.db.init()
        self.container_mgr = ContainerManager()
        self.alert_mgr = AlertManager(self.db)
        self.collector = MetricCollector(
            self.container_mgr, self.db, self.alert_mgr, interval=10
        )

    def _build_container_table(self) -> Table:
        """컨테이너 상태 테이블"""
        table = Table(title="Containers", expand=True)
        table.add_column("Name", style="cyan", ratio=2)
        table.add_column("Service", style="blue")
        table.add_column("Image", ratio=2)
        table.add_column("Status", justify="center")

        containers = self.container_mgr.list_managed()
        for c in containers:
            status = c["status"]
            if status == "running":
                status_display = "[green]● running[/green]"
            elif status == "exited":
                status_display = "[red]● exited[/red]"
            else:
                status_display = f"[yellow]● {status}[/yellow]"

            table.add_row(c["name"], c["service"], c["image"], status_display)

        if not containers:
            table.add_row("[dim]No managed containers[/dim]", "", "", "")

        return table

    def _build_metrics_table(self) -> Table:
        """메트릭 테이블"""
        table = Table(title="Resource Usage", expand=True)
        table.add_column("Container", style="cyan")
        table.add_column("CPU %", justify="right")
        table.add_column("Memory", justify="right")
        table.add_column("Mem %", justify="right")
        table.add_column("Net RX", justify="right")
        table.add_column("Net TX", justify="right")

        containers = self.container_mgr.list_managed()
        for c in containers:
            if c["status"] != "running":
                continue

            stats = self.container_mgr.get_stats(c["name"])
            if not stats:
                continue

            cpu_color = "red" if stats["cpu_percent"] > 80 else \
                       "yellow" if stats["cpu_percent"] > 60 else "green"
            mem_color = "red" if stats["memory_percent"] > 80 else \
                       "yellow" if stats["memory_percent"] > 60 else "green"

            table.add_row(
                c["name"],
                f"[{cpu_color}]{stats['cpu_percent']:.1f}%[/{cpu_color}]",
                f"{stats['memory_usage_mb']:.0f}MB",
                f"[{mem_color}]{stats['memory_percent']:.1f}%[/{mem_color}]",
                self._format_bytes(stats["network_rx_bytes"]),
                self._format_bytes(stats["network_tx_bytes"]),
            )

        return table

    def _build_alerts_panel(self) -> Panel:
        """알림 패널"""
        summary = self.alert_mgr.get_summary()
        text = Text()

        if summary["total_active"] == 0:
            text.append("No active alerts", style="green")
        else:
            text.append(
                f"Active: {summary['total_active']} "
                f"(Critical: {summary['critical']}, Warning: {summary['warning']})\n\n",
                style="bold"
            )
            for alert in summary["alerts"][:5]:
                severity_style = "red" if alert["severity"] == "critical" else "yellow"
                text.append(
                    f"[{alert['severity'].upper()}] {alert['container_name']}: "
                    f"{alert['message']}\n",
                    style=severity_style,
                )

        return Panel(text, title="Alerts", border_style="red" if summary.get("critical") else "green")

    def _build_events_panel(self) -> Panel:
        """최근 이벤트 패널"""
        events = self.db.get_events(limit=8)
        text = Text()

        for event in events:
            text.append(f"{event['created_at'][:19]} ", style="dim")
            text.append(f"[{event['event_type']}] ", style="cyan")
            text.append(f"{event['container_name']}")
            if event.get("details"):
                text.append(f" - {event['details']}", style="dim")
            text.append("\n")

        if not events:
            text.append("No events", style="dim")

        return Panel(text, title="Recent Events")

    @staticmethod
    def _format_bytes(b: int) -> str:
        """바이트를 읽기 좋은 형식으로 변환"""
        for unit in ["B", "KB", "MB", "GB"]:
            if b < 1024:
                return f"{b:.1f}{unit}"
            b /= 1024
        return f"{b:.1f}TB"

    def run(self, refresh_interval: int = 5):
        """대시보드 실행"""
        self.collector.start()

        console.print("[bold green]Container Orchestration Platform - Monitoring Dashboard[/bold green]")
        console.print("[dim]Press Ctrl+C to exit[/dim]\n")

        try:
            with Live(console=console, refresh_per_second=1) as live:
                while True:
                    layout = Layout()
                    layout.split_column(
                        Layout(self._build_container_table(), name="containers", ratio=2),
                        Layout(self._build_metrics_table(), name="metrics", ratio=2),
                        Layout(name="bottom", ratio=2),
                    )
                    layout["bottom"].split_row(
                        Layout(self._build_alerts_panel(), name="alerts"),
                        Layout(self._build_events_panel(), name="events"),
                    )

                    live.update(layout)
                    time.sleep(refresh_interval)

        except KeyboardInterrupt:
            self.collector.stop()
            console.print("\n[yellow]Dashboard stopped[/yellow]")


if __name__ == "__main__":
    dashboard = MonitoringDashboard()
    dashboard.run()
