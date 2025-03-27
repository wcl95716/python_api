"""
API 异常处理模块。

这个模块定义了 API 使用的自定义异常类，用于统一异常处理。
所有 API 相关的异常都应该继承自 APIException 类。
"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any

class APIException(HTTPException):
    """
    API 自定义异常基类。
    
    用于统一处理 API 相关的异常，继承自 FastAPI 的 HTTPException。
    所有 API 相关的异常都应该使用这个类来抛出。
    
    Attributes:
        status_code (int): HTTP 状态码
        detail (Optional[str]): 错误详情信息
        headers (Optional[Dict[str, Any]]): 可选的响应头信息
    
    Example:
        raise APIException(
            status_code=404,
            detail="Resource not found"
        )
    """
    def __init__(
        self,
        status_code: int,
        detail: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers) 