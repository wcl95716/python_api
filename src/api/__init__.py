"""
API 模块的入口文件，负责创建和配置 FastAPI 应用。

主要功能：
1. 创建 FastAPI 应用实例
2. 配置中间件
3. 注册路由
4. 配置全局异常处理
5. 配置基础路由
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
    创建并配置 FastAPI 应用实例
    """
    app = FastAPI(
        title="AgileX API",
        description="AgileX 后端 API 服务",
        version="1.0.0"
    )
    
    # 配置 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由模块
    app.include_router(api_router, prefix="/api")
    
    # 全局异常处理
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseModel(
                code=exc.status_code,
                message=str(exc.detail),
                data=None
            ).dict()
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
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
    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:
        return RedirectResponse(url="/docs")
    
    @app.get("/docs", include_in_schema=False)
    async def custom_docs() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="AgileX API Docs"
        )
    
    return app

# 导出公共接口
__all__ = ["create_app", "api_router"]

