from pydantic import BaseSettings

# Schema for environmental variables

class Settings(BaseSettings):
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES :int
    host:str
    user:str
    password:str
    database:str
    class Config:
        env_file=".env"
    
settings=Settings()
