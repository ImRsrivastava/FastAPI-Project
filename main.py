from fastapi import FastAPI
import models
from database import Engine
from routers import authRoutes, todoRoutes, usersRoutes


app = FastAPI()

models.Base.metadata.create_all ( bind = Engine )


app.include_router(authRoutes.router)
app.include_router(todoRoutes.router)
app.include_router(usersRoutes.router)


