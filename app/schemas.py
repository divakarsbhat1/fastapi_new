from pydantic import BaseModel

# Input taking and output model 

class Post(BaseModel):
    title:str
    content:str

class Resp(BaseModel):
    title:str
    content:str

class created_user(BaseModel):
    userid:int
    email:str

class token_return(BaseModel):
    token:str
    type:str

class Token(BaseModel):
    id:int
    