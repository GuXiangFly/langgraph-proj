from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
import json
from mypy.state import state

from agent.agentstate.my_state import CustomState


# tool_call_id:Annotated[str,InjectedToolCallId],  这个代表通过python的依赖注入，得到的这个tool_call_id
# 这个 tool_call_id 是从上一条的  AI message 中获取得到的。
# messages  Agentstate 里面有一个messages的方法， 调用了这个会自动对messages 在原有的 agentstate里面进行追加

@tool
def get_user_name(
        tool_call_id: Annotated[str, InjectedToolCallId],
        config: RunnableConfig) -> Command:
    """获取用户的所有信息，包括：性别，年龄等"""
    user_name = config['configurable'].get('user_name', 'zs')
    print(f"调用工具， 传入的用户名是：{user_name}")
    # 模拟
    return Command(update={

        # 这个是赋值，直接进行update
        "username": user_name,

        # Agentstate 里面有一个messages的方法， 调用了这个会自动对messages 在原有的 agentstate里面进行追加
        "messages": [
            ToolMessage(
                content="成功得到当前用户的username",
                tool_call_id=tool_call_id,
            )
        ],
    })



@tool
def greet_user(
        tool_call_id: Annotated[str, InjectedToolCallId],
        custom_state: Annotated[CustomState, InjectedState],
        config: RunnableConfig
) -> str:
    """等待用户说出 节日快乐 后执行"""
    print(f"custom_state: ")
    print(f"username {custom_state.get('username')}")
    username:str = custom_state.get('username')  #从状态中获取用户名
    print(f"greet_user 获取的username {username}")
    return f"祝贺你：{username} 节日快乐！"



@tool
def get_user_name_by_talk(
        tool_call_id: Annotated[str, InjectedToolCallId],
        user_name: Annotated[str, '用户对话中告诉我的名字'],
        config: RunnableConfig) -> Command:
    """通过用户的humanMessage对话，获取用户的名字"""
    print(f"调用工具， 用户对话中告诉我的用户名是：{user_name}")
    # 模拟
    return Command(update={

        # 这个是赋值，直接进行update
        "username": user_name,


        # Agentstate 里面有一个messages的方法， 调用了这个会自动对messages 在原有的 agentstate里面进行追加
        "messages": [
            ToolMessage(
                content=f"成功得到当前用户的username: {user_name}",
                tool_call_id=tool_call_id,
            )
        ],
    })
