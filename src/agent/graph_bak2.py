"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from src.agent.common import env_utils
from src.agent.common.model_llm import llm
from src.agent.tools.tool_demo3 import calculate
import os
import tools.tool_demo8 as tool

os.environ['NO_PROXY'] = env_utils.NO_PROXY_IP




# 提示词模板的函数：由用户传入内容，组成一个动态的系统提示词
from typing import Any

# 假设相关类型/工具已导入（如 AgentState、RunnableConfig、AnyMessage、create_react_agent、llm 等）
# 以及工具函数 calculate4、runnable_tool、search_tool、get_user_name、greet_user 已定义

def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    user_name = config['configurable'].get('user_name', 'zs')
    print(user_name)
    system_message = f'你是一个智能助手，尽可能的调用工具回答用户的问题，当前用户的名字是：{user_name}'
    return [{'role': 'system', 'content': system_message}] + state['messages']

graph = create_react_agent(
    llm,
    # tools=[calculate4, runnable_tool, search_tool, get_user_info_by_name],
    tools=[tool.get_user_name, tool.greet_user],
    # prompt="你是一个智能助手，尽可能的调用工具回答用户的问题"
    prompt=prompt,
)