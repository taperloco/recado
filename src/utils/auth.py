from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
import re

# For environmental variables
from dotenv import load_dotenv
import os


#Load secret keys from .env
load_dotenv() 
secret_key = os.getenv("CLAVE_SECRETA")

algorithm = "HS256"
#1440 one day
token_expiry_minutes = 1440 #one day

def check_token(token):
    #return "8d3a62eb-4962-4f44-b5c7-985c4d56e6ef", "nada"
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload.get("user_id"), "OK"
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

def refresh_token(token):
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": jwt.decode(token, secret_key, algorithms=[algorithm], options={"verify_exp": False}).get("user_id"),
        "exp": now + timedelta(minutes=token_expiry_minutes),
        "iat": now
    }
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token  
        
def create_token(user_id):
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "exp": now + timedelta(minutes=token_expiry_minutes),
        "iat": now
    }
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):      # at least one uppercase
        return False
    if not re.search(r"[a-z]", password):      # at least one lowercase
        return False
    if not re.search(r"\d", password):         # at least one digit
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # at least one symbol
        return False
    return True


if __name__ == '__main__':
    #print(hash_password("1234"))
    #Resultado:
    #$2b$12$jFb8Ntzcl4P.t4FVr6pfN.BnDCu3.MstzMr5rVQBQlIawM1swcQCS
    
    print(create_token("8d3a62eb-4962-4f44-b5c7-985c4d56e6ef"))
    #Resultado:
    #eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGQzYTYyZWItNDk2Mi00ZjQ0LWI1YzctOTg1YzRkNTZlNmVmIiwiZXhwIjoxNzQ1MDg0NzYyLCJpYXQiOjE3NDQ5OTgzNjJ9.BkRr14tR3kLkDw7gRM0JLBdA5GFBwp-fyDZhvTIGwtE
