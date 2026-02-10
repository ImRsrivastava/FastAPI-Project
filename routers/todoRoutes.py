from fastapi import APIRouter, HTTPException, Path, Depends
from request_models.todoRequestModel import TodoRequest
from starlette import status
from db.dbConfig import DB_Dependency
from .authRoutes import getCurrentAuthUser
from typing import Annotated

# from models.TodosModel import Todos
from models import Todos

router = APIRouter(
    prefix = "/todo",
    tags = [ "Todo-Routes" ]
)

Auth_Dependency = Annotated [ dict, Depends ( getCurrentAuthUser )]

################### APIs Routes ###################
###### Get Method 
@router.get("/", status_code = status.HTTP_200_OK)
async def read_all (auth: Auth_Dependency, db: DB_Dependency):
    if auth is None:
        raise HTTPException ( status_code = 401, detail = "Authentication Failed.")
    
    return db.query(Todos).filter( Todos.user_id == auth.get("id") ).all()


###### Get Method with ID
@router.get("/{todo_id}", status_code = status.HTTP_200_OK)
async def read_todo_by_id (auth: Auth_Dependency, db: DB_Dependency, todo_id: int = Path (gt = 0)):
    if auth is None:
        raise HTTPException ( status_code = 401, detail = "Authentication Failed.")
    
    todoArr = db.query(Todos).filter(Todos.id == todo_id and Todos.user_id == auth.get("id")).first()
    if todoArr is not None:
        return todoArr
    raise HTTPException (status_code = 404, detail = "Todo associated with provided ID, NOT FOUND!")


###### Post Method
@router.post("/", status_code = status.HTTP_201_CREATED)
async def create_todo (auth: Auth_Dependency, db: DB_Dependency, todo_req: TodoRequest):
    if auth is None:
        raise HTTPException ( status_code = 401, detail = "Authentication Failed" )

    todoData = Todos( **todo_req.dict(), user_id = auth.get("id") )
    db.add(todoData)
    db.commit()


###### Put Method
@router.put("/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def update_todo (auth: Auth_Dependency, db:DB_Dependency, todo_req: TodoRequest, todo_id: int = Path (gt = 0)):
    if auth is None:
        raise HTTPException ( status_code = 401, detail = "Authentication Failed" )
    
    todoData = db.query(Todos).filter(Todos.id == todo_id).first()
    if todoData is None:
        raise HTTPException (status_code = 404, detail = "Todo associated with provided ID, NOT FOUND!")
    
    todoData.title          =   todo_req.title
    todoData.description    =   todo_req.description
    todoData.priority       =   todo_req.priority
    todoData.complete       =   todo_req.complete

    db.add(todoData)
    db.commit()


###### Delete Method
@router.delete("/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo (auth: Auth_Dependency, db: DB_Dependency, todo_id: int = Path (gt = 0)):
    if auth is None:
        raise HTTPException ( status_code = 401, detail = "Authentication Failed" )

    todoData = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.user_id == auth.get('id'))
    todoExist = todoData.first()

    if todoExist is None:
        raise HTTPException (status_code = 404, detail = "Todo associated with provided ID, NOT FOUND!")
    todoData.delete()
    db.commit()


