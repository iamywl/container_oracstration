"""MCP Server - AI 기반 컨테이너 운영 자동화

Model Context Protocol을 활용하여 자연어 명령으로 컨테이너를 관리한다.
LLM 에이전트가 이 서버의 도구를 호출하여 컨테이너 배포, 스케일링,
모니터링, 장애 분석 등을 수행할 수 있다.
"""

import sys
import os
import json
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from mcp_server.tools import ContainerTools

logger = logging.getLogger(__name__)

app = Server("container-platform")
tools = ContainerTools()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록 반환"""
    return [
        Tool(
            name="list_containers",
            description="관리 중인 모든 컨테이너 목록을 조회합니다. 이름, 상태, 이미지, 서비스 정보를 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "필터링할 상태 (running, exited, all)",
                        "enum": ["running", "exited", "all"],
                    }
                },
            },
        ),
        Tool(
            name="deploy_service",
            description="YAML 서비스 정의 파일을 기반으로 컨테이너를 배포합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "yaml_path": {
                        "type": "string",
                        "description": "서비스 정의 YAML 파일 경로",
                    }
                },
                "required": ["yaml_path"],
            },
        ),
        Tool(
            name="scale_service",
            description="서비스의 레플리카 수를 조정합니다. 스케일 아웃/인 모두 지원합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "서비스 이름",
                    },
                    "replicas": {
                        "type": "integer",
                        "description": "목표 레플리카 수",
                        "minimum": 0,
                    },
                },
                "required": ["service_name", "replicas"],
            },
        ),
        Tool(
            name="get_container_stats",
            description="컨테이너의 CPU, 메모리, 네트워크 사용량을 실시간으로 조회합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {
                        "type": "string",
                        "description": "컨테이너 이름",
                    }
                },
                "required": ["container_name"],
            },
        ),
        Tool(
            name="get_container_logs",
            description="컨테이너의 로그를 조회합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {
                        "type": "string",
                        "description": "컨테이너 이름",
                    },
                    "tail": {
                        "type": "integer",
                        "description": "출력할 로그 줄 수",
                        "default": 50,
                    },
                },
                "required": ["container_name"],
            },
        ),
        Tool(
            name="health_check",
            description="모든 컨테이너의 헬스 상태를 확인하고 비정상 컨테이너를 보고합니다.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_alerts",
            description="활성 알림 목록을 조회합니다. 심각도별로 분류하여 표시합니다.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_platform_overview",
            description="플랫폼 전체 상태 요약을 반환합니다. 컨테이너 수, 리소스 현황, 알림 상태를 포함합니다.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="analyze_issue",
            description="컨테이너 장애를 분석하고 원인과 해결 방안을 제시합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_name": {
                        "type": "string",
                        "description": "분석할 컨테이너 이름",
                    }
                },
                "required": ["container_name"],
            },
        ),
        Tool(
            name="get_deployment_history",
            description="서비스의 배포 이력을 조회합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "서비스 이름 (없으면 전체 조회)",
                    }
                },
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """도구 호출 처리"""
    try:
        result = tools.execute(name, arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        error_msg = {"error": str(e), "tool": name}
        return [TextContent(type="text", text=json.dumps(error_msg, ensure_ascii=False))]


async def main():
    """MCP 서버 실행"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream)


if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
