from fastapi import FastAPI, Depends
import models
from database import engine
from Routers import auth,Todos
from Company import company_apis,dependencies
app=FastAPI(title="FastAPI: TodoApp")
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(Todos.router)
app.include_router(company_apis.router,dependencies=[Depends(dependencies.get_token_header)])
