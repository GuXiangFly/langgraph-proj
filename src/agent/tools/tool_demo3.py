from typing import Annotated

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from agent.common.log_utils import log

class CalculateArgs(BaseModel):
    a:float = Field(description = "第一个需要输入的数字")
    b:float = Field(description = "第二个需要输入的数字")
    operation:str = Field(description="运算类型，只能是 add subtract multiply divide 中的一个")

@tool('calculate',return_direct=False, args_schema=CalculateArgs)
def calculate(
        a:Annotated[float,'第一个需要输入的数字'],
        b:Annotated[float,'第二个需要输入的数字'],
        operation:Annotated[float,"运算类型，只能是 add subtract multiply divide 中的一个"],
      ) -> float:
    """计算两个数字的工具"""
    log.info(f"Calculating {operation} between {a} and {b}")
    if operation == "add" or operation == "+":
        return a + b
    elif operation == "subtract" or operation == "-":
        return a - b
    elif operation == "multiply" or operation == "*":
        return a * b
    elif operation == "divide" or operation == "/":
        if b == 0:
            return 0
        return a / b



log.info(f"calculate.name {calculate.name}")
log.info(f"calculate.description {calculate.description}")
log.info(f"calculate.args {calculate.args}")
log.info(f"calculate.args_schema.model_json_schema() {calculate.args_schema.model_json_schema()}")
log.info(f"calculate.return_direct {calculate.return_direct}")
