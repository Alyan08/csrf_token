import redis

from uuid import uuid4
from typing import Optional

from errors import RedisConnectionError, CSRFTokenError, CSRFParamsError


class CSRFAgent:
    def __init__(self):
        self._default_lifetime = 300
        self._max_reuse_count = 5
        self._redis_client = None

    def set_token_params(self,
                         default_lifetime: int,
                         max_reuse_count: int):
        if default_lifetime <= 0:
            raise CSRFParamsError("default_lifetime must be greater than 0")
        if max_reuse_count <= 0:
            raise CSRFParamsError("max_reuse_count must be greater than 0")

        self._default_lifetime = default_lifetime
        self._max_reuse_count = max_reuse_count

    def set_redis_params(self,
                         host: str,
                         port: int,
                         db: int,
                         password: Optional[str] = None,
                         socket_timeout: Optional[int] = None,
                         socket_connect_timeout: Optional[int] = None,
                         socket_keepalive: bool = False,
                         socket_keepalive_options: Optional[dict] = None,
                         max_connections: Optional[int] = None,
                         retry_on_timeout: bool = False,
                         connection_pool: Optional[redis.ConnectionPool] = None):

        self._redis_client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            db=db,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
            socket_keepalive=socket_keepalive,
            socket_keepalive_options=socket_keepalive_options,
            max_connections=max_connections,
            retry_on_timeout=retry_on_timeout,
            connection_pool=connection_pool
        )

        if not self._redis_client.ping():
            raise RedisConnectionError()

    """
    user_info - some details about user, e.g. user_info=example@gmil.com or user_info=123 (id)
    api_name  - protected method name for separation of tokens for a single user
    ex - life time (seconds)
    """
    def set(self,
            user: str,
            api_name: Optional[str] = "",
            ex: Optional[int] = None):

        if ex is None:
            ex = self._default_lifetime

        _token = str(uuid4())
        self._redis_client.set(f'{user}_{api_name}_csrf_t', _token, ex)
        return _token

    """
    reusable - not recommended in critical flows. 
    If True, the token can be reused; intended for one-time use only if False.
    """
    def verify(self,
                        user: str,
                        api_name: Optional[str] = "",
                        token: Optional[str] = None,
                        reusable: Optional[bool] = False
                        ):
        if token is None:
            raise CSRFTokenError(msg='missing token')
        _stored_t = self._redis_client.get(f'{user}_{api_name}_csrf_t')
        if _stored_t is None:
            raise CSRFTokenError(msg='expired or non-required token')
        if token != _stored_t:
            raise CSRFTokenError(msg='wrong token')

        if not reusable:
            self._redis_client.delete(f'{user}_{api_name}_csrf_t')
        return


csrf_agent = CSRFAgent()
