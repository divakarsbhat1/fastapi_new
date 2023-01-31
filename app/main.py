from fastapi import FastAPI,Response,status,HTTPException,Depends
from . import tokenizer
from . import schemas
from random import randint
from . import database
from . import posts
from . import users
from fastapi.middleware.cors import CORSMiddleware

from .config_env import settings
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root

@app.get("/")
async def root(response:Response,get_curr_user:int=Depends(tokenizer.get_current_user)):
    response.status_code=status.HTTP_200_OK
    return {"Message":get_curr_user.id}

app.include_router(posts.router)
app.include_router(users.router)