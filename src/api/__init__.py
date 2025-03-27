"""
API 模块的入口文件，负责创建和配置 FastAPI 应用。

主要功能：
1. 创建 FastAPI 应用实例
2. 配置中间件（如 CORS）
3. 注册路由
4. 配置全局异常处理
5. 配置基础路由（如文档页面）

使用方式：
    from api import create_app, api_router, custom_api_router
    app = create_app()
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from api.core.schemas import ResponseModel
from api.core.exceptions import APIException
import traceback

# 导出路由
from api.api_router import api_router

def create_app() -> FastAPI:
    """
    创建并配置 FastAPI 应用实例。
    
    这个工厂函数负责：
    1. 创建 FastAPI 实例并设置基本配置
    2. 配置 CORS 中间件以支持跨域请求
    3. 注册所有路由模块
    4. 配置全局异常处理
    5. 设置基础路由（如文档页面）
    
    Returns:
        FastAPI: 配置好的 FastAPI 应用实例
    """
    app = FastAPI(
        title="AgileX API",
        description="AgileX 后端 API 服务",
        version="1.0.0"
    )
    
    # 配置 CORS 中间件
    # 允许所有来源的跨域请求，用于开发环境
    # 生产环境建议配置具体的允许来源
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由模块
    app.include_router(api_router)
    
    # 全局异常处理
    # 处理自定义 API 异常
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        """
        处理自定义 API 异常。
        
        将 APIException 转换为统一的响应格式：
        {
            "code": status_code,
            "message": detail,
            "data": null
        }
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseModel(
                code=exc.status_code,
                message=str(exc.detail),
                data=None
            ).dict()
        )
    
    # 处理所有未捕获的异常
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        处理所有未捕获的异常。
        
        1. 记录详细的错误堆栈信息用于调试
        2. 返回统一的错误响应，隐藏具体错误信息
        3. 设置 500 状态码表示服务器内部错误
        """
        # 记录详细错误信息用于调试
        error_detail = traceback.format_exc()
        print(f"Global error: {error_detail}")
        
        return JSONResponse(
            status_code=500,
            content=ResponseModel(
                code=500,
                message="Internal server error",
                data=None
            ).dict()
        )
    
    # 基础路由配置
    # 重定向根路径到 API 文档
    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:
        return RedirectResponse(url="/docs")
    
    # 自定义 Swagger UI 文档页面
    @app.get("/docs", include_in_schema=False)
    async def custom_docs() -> HTMLResponse:
        return get_swagger_ui_html(openapi_url="/openapi.json", title="AgileX API Docs")
    
    return app

# 导出公共接口
__all__ = ["create_app", "api_router", "custom_api_router"]

