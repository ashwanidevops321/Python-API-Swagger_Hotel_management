import secrets
import time

users = {"admin": "password123"}
token_store = {}

TOKEN_EXPIRATION_TIME = 3600

def authenticate_user(username, password):
    if username in users and users[username] == password:
        generated_token = secrets.token_hex(16)
        expires_at = time.time() + TOKEN_EXPIRATION_TIME
        token_store[generated_token] = {"username": username, "expires_at": expires_at}
        return generated_token
    return None

def verify_token(token):
    token_data = token_store.get(token)
    if token_data and token_data["expires_at"] > time.time():
        return token_data["username"] 
    return None

def remove_expired_tokens():
    current_time = time.time()
    expired_tokens = [token for token, data in token_store.items() 
    if data["expires_at"] < current_time]
    for token in expired_tokens:
        del token_store[token]
