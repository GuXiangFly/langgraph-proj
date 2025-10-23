from langchain_openai import ChatOpenAI
from env_utils import *

llm = ChatOpenAI(
    model='qwen3-8b',
    temperature=0.8,
    api_key='xx',
    base_url=LOCAL_BASE_URL,
    extra_body={'chat_template_kwargs': {'enable_thinking': False}},
)

# llm = ChatOpenAI(
#     model='qwen3-4b',
#     temperature=0.8,
#     api_key='xx',
#     base_url='http://172.25.129.72:6006/v1',
#     extra_body={'chat_template_kwargs': {'enable_thinking': False}},
# )

