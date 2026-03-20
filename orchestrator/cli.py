"""CLI 인터페이스"""

import sys
import logging
import click
from rich.console import Console
from rich.table import Table

from orchestrator.engine import OrchestrationEngine
from db.db_manager import DBManager

console = Console()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def get_engine() -> OrchestrationEngine:
    db = DBManager()
    db.init()
    return OrchestrationEngine(db_manager=db)


@click.group()
def cli():
    """Container Orchestration Platform CLI"""
    pass


@cli.command()
@click.argument("yaml_path")
def deploy(yaml_path: str):
    """서비스 정의 YAML을 기반으로 컨테이너 배포"""
    engine = get_engine()
    try:
        deployed = engine.deploy(yaml_path)
        console.print(f"[green]Deployed {len(deployed)} container(s)[/green]")
        for name in deployed:
            console.print(f"  - {name}")
    except Exception as e:
        console.print(f"[red]Deploy failed: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("service_name")
def undeploy(service_name: str):
    """서비스 제거"""
    engine = get_engine()
    if engine.undeploy(service_name):
        console.print(f"[green]Service undeployed: {service_name}[/green]")
    else:
        console.print(f"[yellow]Service not found: {service_name}[/yellow]")


@cli.command(name="list")
def list_containers():
    """관리 중인 컨테이너 목록 조회"""
    engine = get_engine()
    containers = engine.container_mgr.list_managed()

    if not containers:
        console.print("[yellow]No managed containers found[/yellow]")
        return

    table = Table(title="Managed Containers")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Service", style="blue")
    table.add_column("Image")
    table.add_column("Status")

    for c in containers:
        status_style = "green" if c["status"] == "running" else "red"
        table.add_row(
            c["id"], c["name"], c["service"], c["image"],
            f"[{status_style}]{c['status']}[/{status_style}]"
        )

    console.print(table)


@cli.command()
def health():
    """전체 헬스체크 실행"""
    engine = get_engine()
    status = engine.get_status()

    table = Table(title="Platform Health Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value")

    table.add_row("Total Containers", str(status["total_containers"]))
    table.add_row("Running", f"[green]{status['running']}[/green]")
    table.add_row("Stopped", f"[red]{status['stopped']}[/red]")
    table.add_row("Services", ", ".join(status["services"]) or "none")

    console.print(table)

    if status["containers"]:
        console.print("\n[bold]Container Details:[/bold]")
        for c in status["containers"]:
            icon = "✓" if c["status"] == "running" else "✗"
            color = "green" if c["status"] == "running" else "red"
            console.print(f"  [{color}]{icon}[/{color}] {c['name']} ({c['image']}) - {c['status']}")


@cli.command()
@click.argument("service_name")
@click.option("--replicas", "-r", required=True, type=int, help="목표 레플리카 수")
def scale(service_name: str, replicas: int):
    """서비스 스케일링"""
    engine = get_engine()
    if engine.scale(service_name, replicas):
        console.print(f"[green]Scaled {service_name} to {replicas} replicas[/green]")
    else:
        console.print(f"[red]Failed to scale {service_name}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("container_name")
@click.option("--tail", "-t", default=100, help="출력할 로그 줄 수")
def logs(container_name: str, tail: int):
    """컨테이너 로그 조회"""
    engine = get_engine()
    log_output = engine.container_mgr.get_logs(container_name, tail=tail)
    if log_output:
        console.print(f"[bold]Logs for {container_name}:[/bold]")
        console.print(log_output)
    else:
        console.print(f"[yellow]No logs found for {container_name}[/yellow]")


@cli.command()
@click.argument("container_name")
def stats(container_name: str):
    """컨테이너 리소스 사용량 조회"""
    engine = get_engine()
    stat = engine.container_mgr.get_stats(container_name)
    if stat:
        table = Table(title=f"Stats: {container_name}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value")
        table.add_row("CPU Usage", f"{stat['cpu_percent']}%")
        table.add_row("Memory", f"{stat['memory_usage_mb']}MB / {stat['memory_limit_mb']}MB")
        table.add_row("Memory Usage", f"{stat['memory_percent']}%")
        table.add_row("Network RX", f"{stat['network_rx_bytes']} bytes")
        table.add_row("Network TX", f"{stat['network_tx_bytes']} bytes")
        console.print(table)
    else:
        console.print(f"[yellow]Stats not available for {container_name}[/yellow]")


@cli.command()
def daemon():
    """헬스체크 및 오토 스케일러 데몬 시작"""
    engine = get_engine()
    console.print("[green]Starting orchestration daemons...[/green]")
    engine.start_daemons()

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        engine.stop_daemons()
        console.print("\n[yellow]Daemons stopped[/yellow]")


if __name__ == "__main__":
    cli()
