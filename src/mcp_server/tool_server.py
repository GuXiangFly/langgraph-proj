from fastmcp import FastMCP
from fastmcp.prompts.prompt import Prompt,PromptMessage,TextContent

server_gx = FastMCP(name='MCP_guxiang', instructions='guxiang的Python代码实现MCP服务器')

@server_gx.tool()
def my_search(query: str) -> str:
    """搜索互联网上的内容，包括实时天气等"""
    try:
        print("执行我的Python中的工具，输入的参数为:", query)

        # print(response)
        return 'SUCCESS！'
    except Exception as e:
        print(e)
        return '没有搜索到任何内容！'



@server_gx.tool()
def say_hello(username: str) -> str:
    """给用户打个招呼"""
    return f'Hello, {username}!'


@server_gx.prompt
def ask_about_topic(topic: str) -> str:
    """生成请求解释特定主题的用户消息模板"""
    return f"能否请您解释一下'{topic}',这个概念？"

# 高级提示模板：返回结构化消息对象
@server_gx.prompt
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """生成代码编写请求的用户消息模板"""
    content = f"请用{language}编写一个实现以下功能的函数：{task_description}"
    return PromptMessage(
        role="user",
        content=TextContent(type="text", text=content)
    )


# 结构化资源：自动序列化字典为JSON
@server_gx.resource("resource://config")
def get_config() -> dict:
    """以JSON格式返回应用配置"""
    return {
        "theme": "dark",        # 界面主题配置
        "version": "1.2.0",     # 当前版本号
        "features": ["tools", "resources"],  # 已启用的功能模块
    }