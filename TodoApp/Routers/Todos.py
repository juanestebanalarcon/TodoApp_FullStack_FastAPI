
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
