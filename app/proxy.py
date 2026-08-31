import requests
from fastapi import Request, Response
from starlette.background import BackgroundTask
from app.config import cfg

async def proxy_request(raw_req: Request) -> Response:
    """网关核心：接收客户端请求，转发到后端，返回后端响应"""
    target_url = cfg.gateway.target_backend_url.rstrip("/") + raw_req.url.path
    if raw_req.url.query:
        target_url += f"?{raw_req.url.query}"

    # 读取原始body
    body = await raw_req.body()

    # 过滤掉host，由requests自动生成
    headers = dict(raw_req.headers)
    headers.pop("host", None)

    try:
        resp = requests.request(
            method=raw_req.method,
            url=target_url,
            headers=headers,
            data=body,
            timeout=cfg.gateway.proxy_timeout,
        )
    except requests.exceptions.RequestException as e:
        return Response(
            content=f"backend service error: {str(e)}",
            status_code=503
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
        background=BackgroundTask(resp.close)
    )
