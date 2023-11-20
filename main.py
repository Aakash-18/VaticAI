from fastapi import FastAPI, HTTPException, Depends, status, Form, Request
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username: str
    password: str


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def create_user(request: Request):
   return templates.TemplateResponse('index.html', context={'request': request})


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, username: str = Form(...), password: str = Form(...)):
   user = UserBase(username=username, password=password)
   db_user = models.User(**user.dict())
   db.add(db_user)
   db.commit()
   return {"username":username, "password": password}

   

