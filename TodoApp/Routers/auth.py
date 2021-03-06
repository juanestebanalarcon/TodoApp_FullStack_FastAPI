
import sys
sys.path.append("..")
from fastapi import Depends, HTTPException,status,APIRouter,Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import models
from passlib.context import CryptContext

SECRET_KEY="100610607JEAMJUANES234550905846"
ALGOTIHM="HS256"


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name:str
    last_name:str
    password:str
    
bcrypt_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="token")
templates= Jinja2Templates(directory="templates")

router = APIRouter(prefix="/auth",tags=["auth"],responses={401:{"user":"Not authorized"}})

def getDB():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password,hash_password):
    return bcrypt_context.verify(plain_password,hash_password)
def authenticate_user(username:str,password:str,db):
    user=db.query(models.Users).filter(models.Users.username==username).first()
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user
def create_access_token(username:str,user_id:int,expires_delta:Optional[timedelta]=None):
    encode={"sub":username,"id":user_id}
    if expires_delta:
        expire=datetime.utcnow() + expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGOTIHM)

async def get_current_user(token:str=Depends(oauth2_bearer)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGOTIHM)
        username: str = payload.get("sub")
        userid:int=payload.get("id")
        if username is None or userid is None:
            raise get_user_exception()
        return {"username":username,"user_id":userid}
    except JWTError:
        raise get_user_exception()

@router.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session= Depends(getDB)):
    create_user_model=models.Users()
    create_user_model.email=create_user.email
    create_user_model.username=create_user.username
    create_user_model.first_name=create_user.first_name
    create_user_model.last_name=create_user.last_name
    hash_password = get_password_hash(create_user.password)
    create_user_model.hashed_password=hash_password
    create_user_model.is_active=True
    #insert
    db.add(create_user_model)
    db.commit()
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(),db: Session=Depends(getDB)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token=create_access_token(user.username,user.id,expires_delta=token_expires)
    return {"token":token}

@router.get("/",response_class=HTMLResponse)
async def authPage(req:Request):
    return templates.TemplateResponse("login.html",{"request":req})
@router.get("/register",response_class=HTMLResponse)
async def register(req:Request):
    return templates.TemplateResponse("register.html",{"request":req})
    
#Exceptions
def get_user_exception():
    credentails_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not validate credentails",header={"WWW-Authenticate":"Bearer"})
    return credentails_exception
def token_exception():
    token_exception_response=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Incorrect username or password",headers={"WWW-Authenticate":"Bearer"})
    return token_exception_response
