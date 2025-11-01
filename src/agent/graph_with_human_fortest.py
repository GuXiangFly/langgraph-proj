"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations


from langgraph.constants import START,END
from langgraph.graph import MessagesState, StateGraph
from typing_extensions import TypedDict
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from src.agent.common import env_utils
from src.agent.common.model_llm import  openai_llm
from src.agent.tools.tool_demo8 import get_user_name_by_talk, greet_user
import os
import json
from common.env_utils import ZHIPU_API_KEY

os.environ['NO_PROXY'] = env_utils.NO_PROXY_IP

# 外网上公开 MCP 服务端的连接配置
zhipuai_mcp_server_config = {
    'url': 'https://open.bigmodel.cn/api/mcp/web_search/sse?Authorization=' + ZHIPU_API_KEY,
    'transport': 'sse',
}

my_12306_mcp_config = {
    "url": "https://mcp.api-inference.modelscope.net/bcf5d02484eb4e/sse",
    "transport": "sse",
}

mcp_client = MultiServerMCPClient(
    {
        'my_12306_mcp': my_12306_mcp_config,
        'zhipu_mcp_server': zhipuai_mcp_server_config,
    }
)


async def create_agent():
    """必须是异步函数 因为 await只能在异步函数中加"""
    mcp_tools = await mcp_client.get_tools()
    for mcp_tool in mcp_tools:
        print("=====")
        print(mcp_tool)

    return create_react_agent(
        openai_llm,
        tools=mcp_tools,
        prompt="你是一个智能助手，尽可能调用工具回答问题"
    )


graph = asyncio.run(create_agent())