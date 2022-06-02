
import sys
sys.path.append("..")
from fastapi import APIRouter, Depends,HTTPException,Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel, Field
from typing import Optional
from Routers.auth import get_current_user,get_user_exception
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router=APIRouter(prefix="/todos",tags=["Todos"],responses={404:{"description":"Not found"}})
models.Base.metadata.create_all(bind=engine)
templates= Jinja2Templates(directory="templates")

def getDB():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title:str
    description:Optional[str]
    priority:int=Field(gt=0,lt=6,description="Priority must be between 1-5")
    complete:bool

@router.post("/")
async def create_todo(todo:Todo, user:dict=Depends(get_current_user), db:Session = Depends(getDB)):
    if user is None:
        raise get_user_exception()
    todo_model=models.Todos()
    todo_model.title=todo.title
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete
    todo_model.owner_id=user.get("id")
    db.add(todo_model)
    db.commit()
    return successful_response(201)
        
@router.put("/{todo_id}")
async def update_todo(todo_id:int,todo:Todo,user:dict=Depends(get_current_user),db:Session=Depends(getDB)):
    if user is None:
        raise get_user_exception()
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if todo_model is None:
        raise HttpException()
    todo_model.title=todo.title
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete
    
    db.add(todo_model)
    db.commit()
    return successful_response(200)

@router.delete("/{todo_id}")
async def delete_todo(todo_id:int,user:dict=Depends(get_current_user),db:Session=Depends(getDB)):
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if todo_model is None:
        raise HTTPException()
    db.query(models.Todos).filter(models.Todos.id==todo_id).delete()
    db.commit()
    return successful_response(200) 

@router.get("/test")
async def test(req:Request):
    return templates.TemplateResponse("home.html",{"request":req})
  
@router.get("/")
async def read_all(db:Session=Depends(getDB)):
    return db.query(models.Todos).all()

@router.get("/todos/user")
async def read_all_by_user(user:dict=Depends(get_current_user), db:Session=Depends(getDB)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()

@router.get("/toto/{todo_id}")
async def read_todo(todo_id:int,user:dict=Depends(get_current_user),db:Session=Depends(getDB)):
    if user is None:
        raise get_user_exception()
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HttpException()
def HttpException():
    return HTTPException(status_code=404,detail="Todo not found") 
def successful_response(status_code:int):
    return {"Status":status_code,"Transaction":"Successful"}