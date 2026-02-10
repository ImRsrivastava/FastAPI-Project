from fastapi import APIRouter, HTTPException, Path, Depends
from request_models.todoRequestModel import TodoRequest
from starlette import status
from db.dbConfig import DB_Dependency
from .authRoutes import getCurrentAuthUser
from typing import Annotated

# from models.TodosModel import Todos
from models import Todos

router = APIRouter(
    prefix = "/admin",
    tags = [ "Admin-Routes" ]
)

Auth_Dependency = Annotated [ dict, Depends ( getCurrentAuthUser )]
