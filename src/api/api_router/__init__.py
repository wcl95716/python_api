"""
系统核心路由模块。

这个模块包含系统级别的路由，如：
- 系统状态检查
- 系统配置
- 系统日志
等核心功能的路由。
"""

from fastapi import APIRouter
from api.core.schemas import ResponseModel
import importlib
from pathlib import Path

# 创建主路由实例
api_router = APIRouter(
    prefix="/api",
    # tags=["system"]
)

# 自动导入所有子路由
current_dir = Path(__file__).parent
for item in current_dir.iterdir():
    if item.is_dir() and not item.name.startswith('__'):
        try:
            # 动态导入每个子目录中的 api 模块
            module = importlib.import_module(f"api.api_router.{item.name}.api")
            if hasattr(module, 'router'):
                api_router.include_router(module.router)
        except ImportError as e:
            print(f"Warning: Could not import router from {item.name}: {e}")
        except Exception as e:
            print(f"Warning: Error processing {item.name}: {e}")

