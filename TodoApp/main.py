from fastapi import FastAPI
import models
from database import engine
from Routers import auth,Todos
from starlette.staticfiles import StaticFiles

app=FastAPI(title="FastAPI: TodoApp")
models.Base.metadata.create_all(bind=engine)

app.mount("/static",StaticFiles(directory="static"),name="static")
app.include_router(auth.router)
app.include_router(Todos.router)