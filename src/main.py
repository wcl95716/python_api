# 导入 FastAPI 实例
import uvicorn
from api import create_app
import os
import sys
import argparse

# 创建 FastAPI 应用实例
app = create_app()

def main():
    """主函数"""
    try:
        # 创建命令行参数解析器
        parser = argparse.ArgumentParser(description='启动 FastAPI 服务器')
        parser.add_argument('--port', type=int, default=8001, help='服务器端口号 (默认: 8001)')
        args = parser.parse_args()
        
        print(f"服务器将在端口 {args.port} 上启动...")
        
        # 启动服务器
        uvicorn.run(
            app,  # 直接使用 app 实例
            host="0.0.0.0",
            port=args.port,
            log_level="info",
            reload=False  # 在生产环境中禁用重载
        )
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
