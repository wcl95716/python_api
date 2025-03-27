"""
API 核心模块的初始化文件。

这个模块作为 core 包的入口点，主要功能是：
1. 导出核心组件，使它们可以直接从 api.core 导入
2. 简化导入路径，提供更清晰的 API
3. 控制模块的公共接口

使用示例：
    # 不推荐：直接导入具体模块
    from api.core.schemas import ResponseModel
    from api.core.exceptions import APIException
    
    # 推荐：从 core 包直接导入
    from api.core import ResponseModel, APIException

这样可以：
1. 提供更简洁的导入语法
2. 隐藏内部实现细节
3. 方便未来重构（如果改变文件结构，只需要修改这个文件）
4. 统一管理公共接口
"""

from .schemas import ResponseModel
from .exceptions import APIException

# 定义模块的公共接口
# 只有在这里列出的名称才会被 from api.core import * 导入
__all__ = ["ResponseModel", "APIException"] 