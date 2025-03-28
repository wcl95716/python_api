"""
系统核心路由模块。

这个模块包含系统级别的路由，如：
- 系统状态检查
- 系统配置
- 系统日志
等核心功能的路由。
"""

from fastapi import APIRouter

# 创建主路由实例
api_router = APIRouter()

# 导入路由模块
from api.api_router.tianyi_tasks.api import router as tianyi_tasks_router
from api.api_router.port_manager.api import router as port_manager_router
from api.api_router.example.api import router as example_router
from api.api_router.example2.api import router as example2_router

# 注册路由
api_router.include_router(tianyi_tasks_router)
api_router.include_router(port_manager_router)
api_router.include_router(example_router)
api_router.include_router(example2_router)

# api_router.include_router(tianyi_tasks_router, prefix="/tianyi-tasks", tags=["天翼任务"])
# api_router.include_router(port_manager_router, prefix="/port-manager", tags=["端口管理"])
# api_router.include_router(example_router, prefix="/example", tags=["示例1"])
# api_router.include_router(example2_router, prefix="/example2", tags=["示例2"])

