from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from agent.common.env_utils import *

qwen3_embedding_model = OpenAIEmbeddings(
    model=QWEN_EMBEDDING_MODEL_NAME,
    base_url= QWEN_EMBEDDING_BASE_URL,
    dimensions=2560,
    api_key="test",
    check_embedding_ctx_length=False,  # 禁用上下文长度检查，避免tokenization
    skip_empty=True,
    chunk_size=1,  # 减小块大小
    embedding_ctx_length=8191,  # 设置最大长度
)


llm = ChatOpenAI(
    model='qwen3-8b',
    temperature=0.8,
    api_key='xx',
    base_url=LOCAL_BASE_URL,
    extra_body={'chat_template_kwargs': {'enable_thinking': False}},
)



openai_llm = ChatOpenAI(
    temperature=1.0,
    base_url="https://xiaoai.plus/v1",
    api_key='sk-bY9TMxgcsEiW0IyMF3PbF3nvyy36mLLSYZ3O8tjJtoNpKeS9',
    model='gpt-4o'
)

