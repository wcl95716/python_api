# API 路由开发规范

@src/api/api_router/example2/api.py
@src/api/api_router/example/api.py

## 目录结构
```
api_router/
├── __init__.py          # 主路由配置
├── module_name/         # 功能模块
│   ├── __init__.py     # 模块初始化
│   ├── api.py          # 路由定义
│   ├── models.py       # 数据模型
│   ├── schemas.py      # 请求/响应模型
│   └── utils.py        # 工具函数
```

## API 实现方式

### 1. 类方式实现（推荐）
```python
class ExampleAPI(APIRouter):
    def __init__(self):
        super().__init__(
            prefix="/module",
            tags=["模块标签"],
        )
        self.setup_routes()
    
    def setup_routes(self):
        @self.post("", summary="创建")
        async def create_record() -> Response:
            return Response(status_code=200)
```

### 2. 函数方式实现
```python
router = APIRouter(prefix="/module", tags=["模块标签"])

@router.post("", summary="创建")
async def create_record() -> Response:
    return Response(status_code=200)
```

## 开发规则

### 1. 文件规范
- 模块目录：小写字母，下划线分隔
- 类名：PascalCase
- 函数名：小写字母，下划线分隔

### 2. 代码规范
```python
# 导入顺序：标准库 -> 第三方库 -> 本地模块
from fastapi import APIRouter
from .models import Model

# 路由定义
router = APIRouter(prefix="/module", tags=["模块标签"])

@router.get("/endpoint")
async def handler():
    """函数文档字符串"""
    pass
```

### 3. 注释要求
- 文件顶部：模块说明
- 函数：文档字符串
- 复杂逻辑：行内注释

### 4. 错误处理
```python
from fastapi import HTTPException

try:
    # 业务逻辑
except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
```

### 5. 测试要求
- 每个模块必须有测试文件
- 测试文件命名：test_module_name.py
- 测试覆盖率 > 80%

## 开发流程
1. 新增模块：创建目录 -> 添加文件 -> 注册路由
2. 修改模块：保持风格 -> 更新文档 -> 确保兼容
3. 删除模块：移除注册 -> 删除目录 -> 更新文档

## 文档要求
- API 文档：使用 FastAPI 自动生成
- 代码文档：保持同步，提供示例
- 使用限制：明确说明 