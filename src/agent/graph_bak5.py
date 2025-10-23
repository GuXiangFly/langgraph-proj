"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations



from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from pydantic import BaseModel
from typing_extensions import TypedDict


from src.agent.common import env_utils
from src.agent.common.model_llm import llm,openai_llm
from src.agent.tools.tool_demo8 import get_user_name_by_talk,greet_user
import os


os.environ['NO_PROXY'] = env_utils.NO_PROXY_IP


class MyGraphState(TypedDict):
    joke: str  # 生成的冷笑话内容
    topic: str  # 用户指定的主题
    feedback: str  # 改进建议
    funny_or_not: str  # 幽默评级


from pydantic import BaseModel, Field
from typing import Literal

class Feedback(BaseModel):
    """使用此工具来结构化你的响应"""
    grade: Literal["funny", "not funny"] = Field(
        description="判断笑话是否幽默",
        examples=["funny", "not funny"]
    )
    feedback: str = Field(
        description="若不幽默，提供改进建议",
        example="可以加入双关语或意外结局"
    )




def generator_func(state: MyGraphState):
    """由大模型生成一个冷笑话的节点"""
    prompt = (
        f"根据反馈改进笑话：{state['feedback']}\n主题：{state['topic']}"
        if state.get("feedback")
        else f"创作一个关于{state['topic']}的笑话"
    )
    # resp 是AImessage
    resp = openai_llm.invoke(prompt)
    joke = resp.content
    return {
        'joke': joke
    }

def evaluate_func(state: MyGraphState):
    prompt = (

    )

builder =  StateGraph(MyGraphState)
builder.add_node("generator", generator_func)
builder.add_node("evaluate", evaluate_func)



# Define the graph
graph = create_react_agent(
    openai_llm,
    tools=[get_user_name_by_talk,greet_user],

)