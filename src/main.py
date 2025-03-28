# 导入 FastAPI 实例
import uvicorn
from api import create_app
import os
import sys

def main():
    """主函数"""
    try:
        # 创建 FastAPI 应用实例
        app = create_app()
        
        # 启动服务器
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            workers=1,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
