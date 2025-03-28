# 导入 FastAPI 实例
import uvicorn
from api import create_app
import sys
from pathlib import Path

def get_base_path():
    # 检查是否为打包后的环境
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # 检查 _MEIPASS 是否存在
        return Path(sys._MEIPASS)  # 获取 PyInstaller 的临时目录
    return Path(__file__).parent  # 开发环境下的路径

# 动态获取 api_router 的路径
base_path = get_base_path()
api_router_path = base_path / "api/api_router"

# 确保路径存在
if not api_router_path.exists():
    raise FileNotFoundError(f"Path not found: {api_router_path}")

# 创建 FastAPI 应用实例
app = create_app()

if __name__ == "__main__":
    # 开发模式配置
    uvicorn.run(
        app,  # 直接传递 app 对象，避免字符串路径问题
        host="0.0.0.0",
        port=8000,
        # reload=True,  # 开发模式下启用热重载
        workers=1,    # 单进程
        log_level="info"
    )
    
