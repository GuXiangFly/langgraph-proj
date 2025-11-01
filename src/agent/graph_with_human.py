"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.constants import START,END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from pydantic import BaseModel
from typing_extensions import TypedDict

from src.agent.common import env_utils
from src.agent.common.model_llm import  openai_llm
from src.agent.tools.tool_demo8 import get_user_name_by_talk, greet_user
import os
import json

os.environ['NO_PROXY'] = env_utils.NO_PROXY_IP


class MyGraphState(TypedDict):
    joke: Optional[str]  # 生成的冷笑话内容
    topic: Optional[str]   # 用户指定的主题
    feedback: Optional[str]   # 改进建议
    funny_or_not: Optional[str]   # 幽默评级


from pydantic import BaseModel, Field
from typing import Literal, Optional


class Feedback(BaseModel):
    """使用此工具来结构化你的响应"""
    funny_or_not: Literal["funny", "not funny"] = Field(
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
    print(f"generator_func joke response: {joke}")
    return {
        'joke': joke
    }


def evaluator_func(state: MyGraphState):
    """评估状态中的冷笑话"""
    print(f"evaluator_func joke: {state['joke']}")
    chain = openai_llm.with_structured_output(Feedback)
    resp = chain.invoke(
        f"评估此笑话的幽默程度：\n{state['joke']}\n"
        "注意：幽默应包含意外性或巧妙措辞"
    )
    return {
        'feedback': resp.feedback,
        'funny_or_not': resp.funny_or_not
    }

# 条件边的路由函数
def route_func(state: MyGraphState) ->str:
    if state.get("funny_or_not") == "funny":
        return 'go_to_end'
    else:
        return 'go_to_generator'


def before_end_process(state: MyGraphState):
    json_state = json.dumps(state, ensure_ascii=False)
    print(f"before_end_process result json like this: {json_state}")


builder = StateGraph(MyGraphState)
builder.add_node("generator", generator_func)
builder.add_node("evaluator", evaluator_func)
builder.add_node("before_end_process", before_end_process)

builder.add_edge(START, "generator")
builder.add_edge("generator", "evaluator")
builder.add_edge("before_end_process",END)

builder.add_conditional_edges('evaluator', route_func , {
    'go_to_generator': "generator",
    "go_to_end": "before_end_process"
})

# Define the graph
graph = builder.compile(interrupt_before=["before_end_process"])
