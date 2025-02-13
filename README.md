# csrf_token

##Lightweight class for csrf_tokens generating and checking

How to run:
  1) add csrf_token.py + errors.py into your project and import csrf_agent object
  2) install redis client ``pip install redis==5.1.1``

How to use:
  1) set token params `csrf_token.set_token_params`
  2) set redis connections params `csrf_token.set_redis_params`
  3) generating csrf-token example :  `csrf_token = csrf_agent.set()`
  4) checking csrf_token example :     `csrf_t_check_res = csrf_agent.verify(reusable=True/False)`. Use `reusable` flag if you want to reuse created token.
  5) don't forget about exceptions  
