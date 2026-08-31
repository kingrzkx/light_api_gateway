from pydantic import BaseModel
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

class GatewayConfig(BaseModel):
    host: str
    port: int
    target_backend_url: str
    proxy_timeout: int

class RedisConfig(BaseModel):
    host: str
    port: int
    db: int
    password: str | None

class JwtConfig(BaseModel):
    secret_key: str
    algorithm: str
    no_auth_paths: list[str]

class RateLimitConfig(BaseModel):
    enable: bool
    per_ip_max: int
    expire_seconds: int

class IpFilterConfig(BaseModel):
    blacklist: list[str]
    whitelist: list[str]

class AppConfig(BaseModel):
    gateway: GatewayConfig
    redis: RedisConfig
    jwt: JwtConfig
    rate_limit: RateLimitConfig
    ip_filter: IpFilterConfig

def load_config() -> AppConfig:
    config_path = BASE_DIR / "config.yaml"
    example_path = BASE_DIR / "config.example.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"请复制 {example_path.name} 为 config.yaml 并修改配置")
    with open(config_path, "r", encoding="utf‑8") as f:
        raw = yaml.safe_load(f)
    return AppConfig(**raw)

cfg = load_config()
