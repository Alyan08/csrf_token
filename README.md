# csrf_token

##Lightweight class for csrf_tokens generating and checking

How to run:
  1) add csrf_token.py into your project and import main class CsrfToken
  2) run command `pip install -r requirements.txt`
  3) install redis anywhere
  4) set redis-server configurations into main class CsrfToken variables

How to use:
  1) read comments in csrf_token.py
  2) generating csrf-tokken example :  `csrf_token = CsrfToken.create()`
  3) checking csrf_token example :     `csrf_t_check_res = CsrfToken.is_valid(token='token from request')`
                                       `if csrf_t_check_res["status"] : `
                                       `  print("user send valid token with http-request")` 
