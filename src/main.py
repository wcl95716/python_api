# 导入 FastAPI 实例
import uvicorn
from api import create_app

import sys
sys.path.append("./src")

# 创建 FastAPI 应用实例
app = create_app()

if __name__ == "__main__":
    # 获取本机IP
    # uvicorn.run("main:fast_api", host=NetworkUtils.get_ipv6_address(), port=25432, reload=True)
    # uvicorn.run("main:fast_api", host=NetworkUtils.get_ipv4_address(), port=25432, reload=True)
    uvicorn.run(
        "main:app",  # 这里使用字符串路径，指向当前文件中的 app 变量
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式下启用热重载
        workers=1,    # 开发模式下使用单进程
        log_level="info"
    )
    
