# Light‑API‑Gateway
轻量个人API网关，基于FastAPI实现，适合学习与小型项目使用。

功能：
‑ HTTP请求代理转发
‑ JWT鉴权 + Token黑名单
‑ Redis IP计数器限流
‑ IP黑名单拦截
‑ YAML配置驱动，无需修改代码
‑ 请求访问日志
‑ Docker支持

### 快速启动
1. 复制配置：`cp config.example.yaml config.yaml`，修改配置
2. 启动redis
3. 安装依赖：`pip install -r requirements.txt`
4. 运行：`python -m app.main`

### 测试
1. 启动一个被代理的后端服务，修改`config.yaml`中的`target_backend_url`
2. 访问健康检查：`GET http://127.0.0.1:8000/gateway/health`
