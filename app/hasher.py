from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_the_password(password_to_hash:str):
    hashed_password=pwd_context.hash(password_to_hash)
    return hashed_password

def hashed_verify(hashed_password:str,user_password:str):
    return pwd_context.verify(user_password,hashed_password)
