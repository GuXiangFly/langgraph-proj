from langgraph.prebuilt.chat_agent_executor import AgentState


# 系统自定义的状态
class CustomState(AgentState):
    username: str  # 用户名
