from csrf_token import CsrfToken


csrf_token = CsrfToken.create(user_info="login=user123", api_name="/password/change", strong=True)
print(f"created CSRF token: {csrf_token}")


is_valid = CsrfToken.is_valid(csrf_token)
print(f"token is valid? : {is_valid}")

is_valid = CsrfToken.is_valid(user_info="login=user1234", api_name="/password/change")
print(f"token is valid? : {is_valid}")

is_valid = CsrfToken.is_valid(csrf_token, user_info="login=user1234", api_name="/password/change")
print(f"token is valid? : {is_valid}")

is_valid = CsrfToken.is_valid(csrf_token, user_info="login=user123", api_name="/password/delete")
print(f"token is valid? : {is_valid}")

is_valid = CsrfToken.is_valid("wrong token", user_info="login=user123", api_name="/password/change")
print(f"token is valid? : {is_valid}")

is_valid = CsrfToken.is_valid(csrf_token, user_info="login=user123", api_name="/password/change")
print(f"token is valid? : {is_valid}")

is_valid = CsrfToken.is_valid(csrf_token, user_info="login=user123", api_name="/password/change")
print(f"token is valid? : {is_valid}")