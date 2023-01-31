# Import statements

from fastapi import APIRouter, Depends, FastAPI,Response,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from . import schemas
from random import randint
from . import database
from . import hasher
from . import schemas
from . import tokenizer

# Router declaration
router=APIRouter(tags=["users"],prefix="/users")

# Router to create user

@router.post("/create_user",response_model=schemas.created_user)
async def create_user(mydata:OAuth2PasswordRequestForm=Depends()):
    user_id=randint(1,100000)
    hashed_pass=hasher.hash_the_password(mydata.password)
    database.cursor.execute("insert into user(id,username,password) values(%s,%s,%s)",(user_id,mydata.username,hashed_pass))
    database.cursor.fetchone()
    database.connection.commit()
    print(hashed_pass)
    return {"email":mydata.username,"userid":user_id}

# Router to login user

@router.post("/login_user",response_model=schemas.token_return)
async def login_user(mydata:OAuth2PasswordRequestForm=Depends()):
    database.cursor.execute("select id,password from user where username=%s",(mydata.username,))
    y=database.cursor.fetchone()
    verify=hasher.hashed_verify(y[1],mydata.password)
    token=tokenizer.create_access_token({"id":y[0]})
    return {"type":"bearer","token":token}


