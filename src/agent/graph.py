"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = ChatOpenAI(
    model='qwen3-4b',
    temperature=0.8,
    api_key='xx',
    base_url='http://172.25.129.72:6006/v1',
    extra_body={'chat_template_kwargs': {'enable_thinking': False}},
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    # 🔴 实际场景中，这里可替换为真实逻辑（如调用天气API）
    # 示例为模拟返回，仅作演示
    return f"It's always sunny in {city}!"

# Define the graph
graph = create_react_agent(
    llm,
    tools=[get_weather],
    prompt="You are a helpful assistant"
)