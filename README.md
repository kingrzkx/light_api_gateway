
# Light‑API‑Gateway
轻量级 API 网关，基于 FastAPI 实现，用于学习、小型内部服务代理。

> ⚠️ 本项目适合学习与内网小规模使用，不建议未经修改直接公网生产部署。

## ✨ 功能特性
- 全HTTP方法请求代理转发到后端服务
- JWT Token鉴权，支持配置无需鉴权路径
- JWT Token黑名单，支持登出作废Token（Redis存储）
- Redis 基于IP固定窗口限流
- IP黑名单拦截
- YAML配置驱动，无需修改代码
- 请求访问日志，记录IP、路径、方法、状态码、耗时
- Docker 容器化部署支持

## 🧩 技术栈
- Python 3.11+
- FastAPI / Uvicorn
- Pydantic v2 配置校验
- Redis：限流、token黑名单存储
- PyYAML 配置解析

## 📁 项目结构
```

.
├── app
│   ├── **init**.py
│   ├── config.py              # 配置加载与模型定义
│   ├── proxy.py               # 请求代理转发核心
│   ├── utils.py               # jwt、redis 工具函数
│   ├── main.py                # FastAPI 入口、中间件、路由
│   └── middleware
│       ├── log_middleware.py
│       ├── blacklist_middleware.py
│       ├── limit_middleware.py
│       └── auth_middleware.py
├── config.example.yaml        # 配置模板
├── config.yaml                # 本地配置（git 忽略）
├── gen_token.py               # JWT token 生成工具
├── mock_backend.py            # 模拟被代理后端，用于本地调试
├── test_api.py                # http 调用测试脚本
├── requirements.txt
├── Dockerfile
└── README.md

```

## 🚀 本地快速启动

### 1. 准备环境
1. 启动本地 Redis 服务
2. python >=3.11
```bash
# 安装依赖
pip install -r requirements.txt

# 复制配置模板
cp config.example.yaml config.yaml
```

修改 `config.yaml`：

- 修改 `target_backend_url` 设置你的后端服务地址
- 修改 `jwt.secret_key` 使用强密钥
- 修改 redis 连接信息

### 2. 启动模拟后端（仅测试用）

```
python mock_backend.py
# 后端监听 127.0.0.1:8080
```

### 3. 启动网关服务

```
python -m app.main
# 默认监听 0.0.0.0:8000
```

### 4. 生成 JWT 测试 token

```
python gen_token.py
```

复制输出的 token，用于接口请求 Authorization Header。

### 5. 测试访问

健康检查接口（无需鉴权）

```
curl http://127.0.0.1:8000/gateway/health
```

代理接口（需要 Bearer Token）

```
curl -H "Authorization: Bearer 你的token" http://127.0.0.1:8000/api/demo
```

也可以运行测试脚本：

```
python test_api.py
```

## 🐳 Docker 部署

### 构建镜像

```
docker build -t light-api-gateway:latest .
```

### 运行容器

> 
> 需要外部提供 Redis 服务；把本地 config.yaml 挂载进容器

```
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  --name gateway \
  light-api-gateway:latest
```

> 
> 注意：容器内访问 Redis，如果 Redis 宿主机部署，配置 redis.host 不要写 127.0.0.1，使用宿主机局域网 IP。

### docker-compose 参考（可选）

```
version: "3.8"
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  gateway:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./config.yaml:/app/config.yaml
    depends_on:
      - redis
```

## ⚙️ 配置说明 config.yaml

表格

| 分组 | 配置项 | 说明 |
| --- | --- | --- |
| gateway.host | 网关监听地址 | 0.0.0.0 容器部署必填 |
| gateway.port | 网关端口 | 默认 8000 |
| gateway.target_backend_url | 被代理后端服务地址 | 代理转发目标 |
| gateway.proxy_timeout | 代理请求超时，秒 |  |
| redis | redis 连接配置 | 用于限流、token 黑名单 |
| jwt.secret_key | jwt 签名密钥，生产务必修改 |  |
| jwt.algorithm | 签名算法 HS256 |  |
| jwt.no_auth_paths | 免鉴权路径列表 | 例如健康检查 |
| rate_limit.enable | 是否开启 IP 限流 | true/false |
| rate_limit.per_ip_max | 窗口内单 IP 最大请求数 |  |
| rate_limit.expire_seconds | 限流时间窗口 |  |
| ip_filter.blacklist | IP 黑名单列表，匹配直接 403 拒绝 |  |

> 
> ip_filter.whitelist 当前版本代码未实现该逻辑。

## 🛡️ 中间件执行顺序（请求流入顺序）

1. log_middleware：记录访问日志
2. ip_blacklist_middleware：IP 黑名单拦截
3. rate_limit_middleware：IP 限流校验
4. auth_middleware：JWT 鉴权、token 黑名单校验

鉴权通过后，请求进入代理逻辑转发至后端服务。

## ⚠️ 已知局限 & 生产改进建议

1. **代理使用同步 requests**：async 环境会阻塞事件循环；建议替换为 `httpx.AsyncClient` 异步 http 客户端。
2. 限流为**固定窗口限流**，存在临界流量突刺风险；生产建议实现滑动窗口。
3. 没有解析 X‑Forwarded‑For，网关部署在 Nginx 后获取不到真实客户端 IP，需要改造中间件。
4. ip_filter.whitelist 配置字段未实现业务逻辑。
5. 缺少登出 HTTP 接口，只能内部调用工具函数将 token 加入黑名单。
6. 缺少熔断、重试、metrics 监控、单元测试。

## License

MIT