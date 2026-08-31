from fastapi import Request, Response
from app.config import cfg
from app.utils import verify_jwt, is_token_in_blacklist

async def auth_middleware(request: Request, call_next):
    path = request.url.path
    if path in cfg.jwt.no_auth_paths:
        return await call_next(request)

    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(content="unauthorized", status_code=401)
    token = auth_header.split(" ",1)[1]

    if is_token_in_blacklist(token):
        return Response(content="token invalid", status_code=401)

    payload = verify_jwt(token)
    if not payload:
        return Response(content="token verify failed", status_code=401)

    # 把解析后的用户信息放到request.state，后续可使用
    request.state.user = payload
    resp = await call_next(request)
    return resp
