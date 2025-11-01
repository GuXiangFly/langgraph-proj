import asyncio
import json
from pyexpat.errors import messages
from typing import Dict, Any, List

from langchain_core.messages import AIMessage, ToolMessage, ToolCall


class BasicToolsNode:
    """
    异步工具节点，用于并发执行AIMessage中请求的工具调用
    AIMessage 里面可能会有两个tool calls  这时候我们可以并发执行

    功能：
    1. 接收工具列表并建立名称索引
    2. 并发执行消息中的工具调用请求
    3. 自动处理同步/异步工具适配
    """

    def __init__(self, tools: list):
        self.tools = tools
        self.tools_by_name:Dict[str, Any] = { tool.name : tool for tool in tools}

    async def _execute_tool_calls(self, tool_calls: list[ToolCall]) -> List[ToolMessage]:
        """执行实际工具调用
        Args:
            tool_calls: 工具调用请求列表
        Returns:
            ToolMessage结果列表
        """

        tool_coroutines = []
        for tool_call in tool_calls:
            coroutine = self._invoke_tool_call(tool_call)
            tool_coroutines.append(coroutine)

        tool_results = await asyncio.gather(*tool_coroutines)

        return tool_results


    async def _invoke_tool_call(self, tool_call: ToolCall) -> ToolMessage:
        try:
            tool_call_name = tool_call['name']
            tool = self.tools_by_name.get(tool_call_name)
            if hasattr(tool, 'ainvoke'):
                tool_result =  await tool.ainvoke(tool_call["args"])
            else:
                loop = asyncio.get_event_loop()
                tool_result = await loop.run_in_executor(
                    None,
                    tool.invoke,
                    tool_call["args"]
                )
            return ToolMessage(
                content=json.dumps(tool_result, ensure_ascii=False),
                name = tool_call["name"],
                tool_call_id = tool_call["id"],
            )
        except KeyError:
            raise KeyError('tool_call_name')


    async def __call__(self, state: Dict[str, Any]) -> Dict[str, List[ToolMessage]]:
        """异步调用入口
        Args:
            state: 输入字典，需包含"messages"字段
        Returns:
            包含ToolMessage列表的字典
        Raises:
            ValueError: 当输入无效时抛出
        """
        tool_msgs = []
        messages = state.get('messages')
        if not (messages is None):
            raise ValueError("输入数据中找到消息内容")
        # 消息的最后一条 必然是
        latest_ai_message: AIMessage = messages[-1]
        outputs = await self._execute_tool_calls(latest_ai_message.tool_calls)
        return {"messages": outputs}
