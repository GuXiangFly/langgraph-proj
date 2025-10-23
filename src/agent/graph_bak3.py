"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from src.agent.agentstate.my_state import CustomState
from src.agent.common import env_utils
from src.agent.common.model_llm import llm,openai_llm
from src.agent.tools.tool_demo8 import get_user_name_by_talk,greet_user
import os

os.environ['NO_PROXY'] = env_utils.NO_PROXY_IP




# 提示词模板的函数：由用户传入内容，组成一个动态的系统提示词
def prompt(state:AgentState ,config:RunnableConfig) -> list[AnyMessage]:
    user_name = config['configurable'].get('user_name','zs')
    print(user_name)
    system_message = f'你是一个智能助手，当前用户名字是：{user_name}'
    return [{'role':'system', 'content':system_message}] + state['messages']
    pass

# Define the graph
graph = create_react_agent(
    openai_llm,
    tools=[get_user_name_by_talk,greet_user],
    prompt=prompt,
    state_schema=CustomState,
)