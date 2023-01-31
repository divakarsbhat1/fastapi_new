# Import statements

from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi import HTTPException,Depends,status
from . import schemas
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from.config_env import settings

#oAuth2 is a security protocol,to instanciate the object of this,
#first we need the method OAuth2PasswordBearer(), we need to pass the service where the token was generated
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login_user")

# Function to create access token

def create_access_token(data:dict()):
    data_to_encode=data
    expire=datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp":expire})
    created_token=jwt.encode(data_to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return created_token

# Function to verify access token ***   

def verify_access_token(token:str,token_exception):
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        id:int=payload.get("id")
        if id is None:
            raise token_exception
        id_sch=schemas.Token(id=id)
    except JWTError:
        raise token_exception
    return id_sch

def get_current_user(token:str=Depends(oauth2_scheme)):
    token_exception=HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"could not validate credentials",headers={"www-Autenticate":"bearer"})
    return verify_access_token(token,token_exception)