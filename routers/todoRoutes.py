from fastapi import APIRouter, HTTPException, Path
from request_models.todoRequestModel import TodoRequest
from starlette import status
from db.dbConfig import DB_Dependency
# from models.TodosModel import Todos
from models import Todos

router = APIRouter()


################### APIs Routes ###################
###### Get Method 
@router.get("/", status_code = status.HTTP_200_OK)
async def read_all (db: DB_Dependency):
    return db.query(Todos).all()


###### Get Method with ID
@router.get("/todo/{todo_id}", status_code = status.HTTP_200_OK)
async def read_todo_by_id (db: DB_Dependency, todo_id: int = Path (gt = 0)):
    todoArr = db.query(Todos).filter(Todos.id == todo_id).first()
    if todoArr is not None:
        return todoArr
    raise HTTPException (status_code = 404, detail = "Todo associated with provided ID, NOT FOUND!")


###### Post Method
@router.post("/todo", status_code = status.HTTP_201_CREATED)
async def create_todo (db: DB_Dependency, todo_req: TodoRequest):
    todoData = Todos( **todo_req.dict() )
    db.add(todoData)
    db.commit()


###### Put Method
@router.put("/todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def update_todo (db:DB_Dependency, todo_req: TodoRequest, todo_id: int = Path (gt = 0)):
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
@router.delete("/todo/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo (db: DB_Dependency, todo_id: int = Path (gt = 0)):
    todoData = db.query(Todos).filter (Todos.id == todo_id)
    todoExist = todoData.first()

    if todoExist is None:
        raise HTTPException (status_code = 404, detail = "Todo associated with provided ID, NOT FOUND!")
    todoData.delete()
    db.commit()


