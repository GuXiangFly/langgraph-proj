import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from src.agent.common.model_llm import openai_llm

python_mcp_server_config = {
    'url': 'http://127.0.0.1:8181/streamable',
    'transport': 'streamable_http'
}

java_mcp_server_config = {
    'url': 'http://127.0.0.1:8080/api/v1/sse',
    #'url': 'http://127.0.0.1:8098/api/v1/sse',
    'transport': 'sse'
}


## MCP的构造

mcp_client = MultiServerMCPClient(
    {
        'weather_mcp_server': java_mcp_server_config,
    }
)



async def create_agent():
    """必须是异步函数 因为 await只能在异步函数中加"""
    mcp_tools = await mcp_client.get_tools()
    print('mcp_tools', mcp_tools)

    return create_react_agent(
        openai_llm,
        tools=mcp_tools,
        prompt="你是一个智能助手，尽可能调用工具回答问题"
    )


graph = asyncio.run(create_agent())