import redis
import jwt
from datetime import datetime, timedelta
from app.config import cfg

# redis连接，增加 protocol=2，兼容Windows旧版Redis
redis_client = redis.Redis(
    host=cfg.redis.host,
    port=cfg.redis.port,
    db=cfg.redis.db,
    password=cfg.redis.password,
    decode_responses=True,
    protocol=2   # 新增这一行！强制RESP2协议，关闭HELLO握手
)

def create_jwt_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, cfg.jwt.secret_key, algorithm=cfg.jwt.algorithm)
    return token

def verify_jwt(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, cfg.jwt.secret_key, algorithms=[cfg.jwt.algorithm])
        return payload
    except jwt.PyJWTError:
        return None

def add_token_blacklist(token: str, ttl: int):
    redis_client.setex(f"jwt:black:{token}", ttl, "1")

def is_token_in_blacklist(token: str) -> bool:
    return redis_client.exists(f"jwt:black:{token}") > 0
