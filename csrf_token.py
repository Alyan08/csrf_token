
import json
import secrets
import redis

from uuid import uuid4
from typing import Optional


class CsrfTokenError(Exception):
    pass


class CsrfToken:
    host = 'localhost'
    port = 6379
    password = None
    redis_db_index=0

    token_default_lifetime = 300
    token_maximum_lifetime = 3600
    create_attempts = 10

    redis_client = redis.StrictRedis(host=host, port=port, db=redis_db_index)

    """
    user_info - some details about user, e.g. user_info=example@gmil.com or user_info=123 (id)
    api_name  - protected method name for separation of tokens for a single user
    ex - life time (seconds)
    strong - more secure cryptographic method of token generation if True
    """
    @classmethod
    def create(cls, user_info: Optional[str] = "",
               api_name: Optional[str] = "",
               ex: Optional[int] = None,
               strong: Optional[bool] = False):

        if ex is None or ex < 0:
            ex = cls.token_default_lifetime

        ex = min(ex, cls.token_maximum_lifetime)

        data = json.dumps({"user_info": user_info, "api_name": api_name})

        for i in range(cls.create_attempts):
            token = str(secrets.token_hex(32)) if strong else str(uuid4())
            try:
                if not cls.redis_client.get(token):
                    cls.redis_client.set(token, data, ex=ex)
                    return token
            except:
                pass

        return None

    """
    reusable - not recommended in critical flows. 
    If True, the token can be reused; intended for one-time use only if False.
    """
    @classmethod
    def is_valid(cls, token: Optional[str] = "",
                 user_info: Optional[str] = "",
                 api_name: Optional[str] = "",
                 reusable: Optional[bool] = False):

        response = {"status": False, "msg": ""}

        try:
            validation_result = cls.redis_client.get(token)
            if not validation_result:
                raise ValueError("Invalid token")

            token_data = json.loads(validation_result.decode())

            if token_data.get("user_info") != user_info or token_data.get("api_name") != api_name:
                raise ValueError("Token does not match the provided user_info and api_name.")

            if not reusable:
                cls.redis_client.delete(token)
            response = {"status": False, "msg": "valid csrf token"}

        except redis.RedisError:
            response["msg"] = "Reddis error"
        except ValueError as e:
            response["msg"] = f"{e}"
        except:
            response["msg"] = "unknown error"

        finally:
            return response

