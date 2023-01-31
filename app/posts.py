# Import statements
from fastapi import APIRouter, FastAPI,Response,status,HTTPException,Depends
from . import schemas
from random import randint
from . import database
from . import tokenizer

# Router declaration

router=APIRouter(tags=["posts"],prefix="/posts")

# create a post

@router.post("/create_posts")
async def create_posts(post:schemas.Post,response:Response,get_curr_user:int=Depends(tokenizer.get_current_user)):
    abc=post.dict()
    if abc["title"]==None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="title is missing")
    elif abc["content"]==None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="content is missing")
    else:
        new_title=abc["title"]
        new_content=abc["content"]
        new_id=randint(1,1000000)
        aa=int(get_curr_user.id)
        database.cursor.execute("insert into posts(id,title,content,user_id) values(%s,%s,%s,%s);",(new_id,new_title,new_content,aa))
        database.cursor.fetchone()
        database.connection.commit()
        response.status_code=status.HTTP_201_CREATED
        return {"Message":"New Post Created"}

# Get all posts

@router.get("/get_all_posts")
async def get_all_posts(response:Response,response_model=schemas.Resp,get_curr_user:int=Depends(tokenizer.get_current_user)):
    database.cursor.execute("select * from posts where user_id=%s",(get_curr_user.id,))
    ihavedata=database.cursor.fetchall()
    print(ihavedata)
    x={}
    for i in ihavedata:
        x.update({"title":i[1]})
        x.update({"content":i[2]})
    return x

# Get all posts by id

@router.get("/get_post/{id}",response_model=schemas.Resp)
async def get_post(id:int,response:Response,get_curr_user:int=Depends(tokenizer.get_current_user)):
    database.cursor.execute("select * from posts where id=%s",(str(id),))
    mydata=database.cursor.fetchone()
    if mydata==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The Requested ID not found")
    else:
        x={}
        x.update({"title":mydata[1]})
        x.update({"content":mydata[2]})
        return x

# Delete all posts

@router.get("/delete_post/{id}",)
async def delete_post(id:int,response:Response,get_curr_user:int=Depends(tokenizer.get_current_user)):
    database.cursor.execute("select * from posts where id=%s",(str(id),))
    mydata=database.cursor.fetchone()
    if mydata==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The Requested ID not found")
    else:
        database.cursor.execute("delete from posts where id=%s",(str(id),))
        database.cursor.fetchone()
        database.connection.commit()
        response.status_code=status.HTTP_204_NO_CONTENT
        return {"Message":"SUccessfully Deleted"}

# update specific post

@router.put("/update_post/{id}")
async def update_post(id:int,post:schemas.Post,response:Response,get_curr_user:int=Depends(tokenizer.get_current_user)):
    database.cursor.execute("select * from posts where id=%s",(str(id),))
    mydata=database.cursor.fetchone()
    if mydata==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The Requested ID not found")
    else:
        abc=post.dict()
        new_title=abc["title"]
        database.cursor.execute("update posts set title=%s where id=%s",(new_title,str(id)))
        database.cursor.fetchone()
        database.connection.commit()
        response.status_code=status.HTTP_204_NO_CONTENT
        return {"Message":"successfully updated"}