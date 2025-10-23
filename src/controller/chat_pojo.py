from pydantic import BaseModel, Field
from typing import List, Optional, Union


class ChatRequest(BaseModel):
    user_input: str = Field(..., description="要输入的文本")
    work_flow_id:str = Field(...,description= "对话的id")



class ChatResponse(BaseModel):
    user_input: str = Field(..., description="要输入的文本")
    chat_response_content: str
    work_flow_id:str = Field(...,description= "对话的id")
