from fastapi import FastAPI, Request
import models
from database import Engine
from routers import authRoutes, todoRoutes, usersRoutes
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

models.Base.metadata.create_all ( bind = Engine )

templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/")
def test (request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(authRoutes.router)
app.include_router(todoRoutes.router)
app.include_router(usersRoutes.router)


