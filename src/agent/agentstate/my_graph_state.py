from typing import TypedDict

class MyGraphState(TypedDict):
    joke: str  # 生成的冷笑话内容
    topic: str  # 用户指定的主题
    feedback: str  # 改进建议
    funny_or_not: str  # 幽默评级