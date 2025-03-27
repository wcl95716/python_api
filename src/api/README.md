# AgileX API 模块

## 简介
AgileX API 模块是一个基于 FastAPI 构建的现代化 API 框架，提供了统一的响应格式、异常处理、路由管理等核心功能。

## 目录结构
```
src/api/
├── __init__.py          # API 入口文件，应用配置
├── core/                # 核心功能模块
│   ├── __init__.py     # 核心模块导出
│   ├── schemas.py      # 数据模型定义
│   └── exceptions.py   # 异常处理
├── api_router/         # 系统核心路由
└── custom_api/         # 自定义业务路由
```

## 核心功能

### 1. 应用入口
- 工厂模式创建 FastAPI 应用
- CORS 中间件配置
- 路由模块注册
- 全局异常处理
- API 文档配置

### 2. 统一响应格式
```python
{
    "code": 200,          # HTTP 状态码
    "message": "success", # 响应消息
    "data": {...}         # 响应数据
}
```

### 3. 异常处理
- 统一的异常基类 `APIException`
- 全局异常处理器
- 详细的错误日志记录

## 快速开始

### 1. 创建路由
```python
from fastapi import APIRouter
from api.core.schemas import ResponseModel
from api.core.exceptions import APIException

router = APIRouter()

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        item = await get_item_from_db(item_id)
        if not item:
            raise APIException(
                status_code=404,
                detail=f"Item {item_id} not found"
            )
        return ResponseModel(data=item)
    except Exception as e:
        raise APIException(
            status_code=500,
            detail=str(e)
        )
```

### 2. 启动应用
```python
from api import create_app

app = create_app()
```

## 最佳实践

### 1. 路由组织
- 系统核心路由放在 `api_router/`
- 业务相关路由放在 `custom_api/`
- 每个路由模块使用独立的文件

### 2. 异常处理
- 使用 `APIException` 抛出异常
- 在全局异常处理器中统一处理
- 生产环境隐藏具体错误信息

### 3. 响应格式
- 使用 `ResponseModel` 包装响应
- 保持响应格式统一
- 使用类型注解确保类型安全

## 配置说明

### CORS 配置
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 异常处理配置
```python
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
```

## 注意事项

### 1. 安全性
- 生产环境配置具体的 CORS 来源
- 隐藏敏感错误信息
- 使用环境变量管理配置

### 2. 性能
- 合理使用异步操作
- 避免不必要的数据库查询
- 使用缓存优化性能

### 3. 可维护性
- 遵循模块化设计
- 保持代码结构清晰
- 编写完整的文档

## 开发指南

### 1. 添加新路由
1. 在 `custom_api/` 或 `api_router/` 中创建新的路由文件
2. 定义路由处理函数
3. 在相应的 `main.py` 中注册路由

### 2. 添加新异常
1. 在 `core/exceptions.py` 中定义新的异常类
2. 继承 `APIException` 基类
3. 在全局异常处理器中处理

### 3. 添加新数据模型
1. 在 `core/schemas.py` 中定义新的模型类
2. 继承 `BaseModel`
3. 使用类型注解确保类型安全

## 常见问题

### 1. 跨域问题
- 检查 CORS 配置
- 确保请求头正确设置
- 验证允许的来源列表

### 2. 异常处理
- 使用 `APIException` 抛出异常
- 检查异常处理器是否正确注册
- 查看错误日志获取详细信息

### 3. 响应格式
- 使用 `ResponseModel` 包装响应
- 确保状态码正确设置
- 检查数据类型匹配

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT License 