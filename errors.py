from typing import Optional


class RedisConnectionError(Exception):
    def __init__(self, msg: Optional[str] = "unknown"):
        super().__init__(f"Redis connection error: {msg}")


class CSRFTokenError(Exception):
    def __init__(self, msg: Optional[str] = "invalid token"):
        super().__init__(f"csrf token error: {msg}")


class CSRFParamsError(Exception):
    def __init__(self, msg: Optional[str] = "unknown"):
        super().__init__(f"wrong csrf token configuration: {msg}")
