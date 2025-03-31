# 导入 FastAPI 实例
import uvicorn
from api import create_app
import os
import sys

# 创建 FastAPI 应用实例
app = create_app()

def main():
    """主函数"""
    try:
        # 启动服务器
        uvicorn.run(
            app,  # 直接使用 app 实例
            host="0.0.0.0",
            port=8001,
            log_level="info",
            reload=False  # 在生产环境中禁用重载
        )
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
