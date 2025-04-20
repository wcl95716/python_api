# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

# # 安装系统依赖
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     python3-dev \
#     xvfb \
#     x11-apps \
#     && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ ./src/

# 暴露端口（根据你的应用需要修改）
EXPOSE 8066

# 运行应用
CMD ["python", "src/main.py"] 