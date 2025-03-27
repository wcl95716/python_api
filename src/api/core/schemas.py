"""
API 核心数据模型定义。

这个模块定义了 API 使用的核心数据模型，包括：
1. 通用响应模型
2. 分页参数模型
3. 分页响应模型

这些模型用于统一 API 的请求和响应格式，确保数据的一致性和类型安全。
"""

from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

# 定义泛型类型变量，用于响应数据的类型
T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    """
    通用 API 响应模型。
    
    用于统一所有 API 响应的格式：
    {
        "code": 200,          # HTTP 状态码
        "message": "success", # 响应消息
        "data": {...}         # 响应数据
    }
    
    Attributes:
        code (int): HTTP 状态码，默认 200
        message (str): 响应消息，默认 "success"
        data (Optional[T]): 响应数据，可以是任何类型
    """
    code: int = 200
    message: str = "success"
    data: Optional[T] = None 