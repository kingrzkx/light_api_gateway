FROM python:3.11-slim

WORKDIR /app

# 设置python环境
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 拷贝依赖文件
COPY requirements.txt .

# 安装python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝项目源码
COPY ./app /app/app
COPY config.example.yaml /app/config.example.yaml

# 注意：config.yaml 不打入镜像，运行时宿主机挂载覆盖
# EXPOSE声明端口，仅文档提示，不实际开启端口
EXPOSE 8000

# 启动命令，使用uvicorn，使用app.main:app，读取配置
CMD ["python","-m","app.main"]