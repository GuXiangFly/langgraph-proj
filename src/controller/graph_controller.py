
from fastapi import FastAPI, HTTPException
from src.controller.chat_pojo import ChatRequest, ChatResponse

import logging

app = FastAPI(title="Chat API")

logger = logging.getLogger(__name__)

# 定义API端点
@app.post("/chat/message", response_model=ChatResponse)
def create_embedding(request: ChatRequest):
    """创建嵌入向量（符合OpenAI API规范）"""

    # result =
    #
    # request_json = request.model_dump_json()
    # result_response = ChatResponse(**result)
    # vector_example = embedding_service.get_vector_example(result_response)
    # logger.info(f"embeddings request is:{request_json} vector_example is: {vector_example}")

    # return result_response
