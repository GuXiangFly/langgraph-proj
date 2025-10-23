from fastmcp import FastMCP
from zhipuai import ZhipuAI
from agent.env_utils import ZHIPU_API_KEY

zhipuai_client = ZhipuAI(api_key=ZHIPU_API_KEY)
mcp_server = FastMCP(name='老肖的MCP', instructions='老肖的Python代码实现MCP服务器')

@mcp_server.tool()
def my_search(query: str) -> str:
    """搜索互联网上的内容，包括实时天气等"""
    try:
        print("执行我的Python中的工具，输入的参数为:", query)
        response = zhipuai_client.web_search.web_search(
            search_engine="search_pro",
            search_query=query
        )
        # print(response)
        if response.search_result:
            return "\n\n".join([d.content for d in response.search_result])
        return '没有搜索到任何内容！'
    except Exception as e:
        print(e)
        return '没有搜索到任何内容！'