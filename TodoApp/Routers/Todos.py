
import sys

from markupsafe import HasHTML
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

#Routes
@router.get("/",response_class=HTMLResponse)
async def read_all_by_user(req:Request):
    return templates.TemplateResponse("home.html",{"request":req})
@router.get("/add-todo",response_class=HTMLResponse)
async def add_new_todo(req:Request):
    return templates.TemplateResponse("add-todo.html",{"request":req})
@router.get("/edit-todo/{todo_id}",response_class=HTMLResponse)
async def edit_todo(req:Request):
    return templates.TemplateResponse("edit-todo.html",{"request":req})
