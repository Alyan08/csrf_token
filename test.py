from csrf_token import csrf_agent
csrf_agent.set_redis_params(host='localhost', port=6379, db=0)


_token = csrf_agent.set(user="login=user123", api_name="/password/change")
print(f"created CSRF token: {_token}")

try:
    csrf_agent.verify(user="login=user123", api_name="/password/change")
    print("valid CSRF token")
except Exception as e:
    print(e.__class__.__name__)
    print(e)

try:
    csrf_agent.verify(user="login=user123", token=_token)
    print("valid CSRF token")
except Exception as e:
    print(e.__class__.__name__)
    print(e)

try:
    csrf_agent.verify(user="login=user123", api_name="/password/change", token=_token)
    print("valid CSRF token")
except Exception as e:
    print(e.__class__.__name__)
    print(e)
