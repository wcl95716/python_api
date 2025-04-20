# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

# 设置 pip 使用国内镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制依赖文件
COPY requirements.txt .

# # 安装系统依赖
# RUN apt-get update && apt-get install -y \
#     gcc \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# 分批安装依赖，先安装基础依赖
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv

# 安装其他依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ ./src/

# 暴露端口
EXPOSE 8066

# 运行应用
CMD ["python", "src/main.py"] 