import bcrypt
from typing import Union
from storage import User, StorageInstance
from functools import wraps

def check_login_details(username: str, password: str) -> Union[User,bool]:
  try:
    claimed_user = User.get(User.username == username)
  except User.DoesNotExist:
    return False
  pass_bytes = password.encode('utf-8')
  user_pass = claimed_user.password
  matched = bcrypt.checkpw(pass_bytes, user_pass)
  if matched == False:
    return matched
  else:
    return claimed_user

def identity(payload):
  user_id = payload['identity']
  ID = User.get(User.id == user_id)
  if ID:
    return ID
  else:
    return None
