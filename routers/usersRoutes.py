from fastapi import APIRouter, HTTPException, Path, Depends
from request_models.authVerificationRequestModel import AuthVerificationRequestModel, UpdateAuthPhoneNumberRequestModel
from starlette import status
from db.dbConfig import DB_Dependency
from .authRoutes import getCurrentAuthUser
from typing import Annotated
from models import Auths

# For password verify and change in passlib.context library to import CryptContext
from passlib.context import CryptContext

# from models.TodosModel import Todos
from models import Todos

router = APIRouter(
    prefix = "/users",
    tags = [ "User-Routes" ]
)

Auth_Dependency = Annotated [ dict, Depends ( getCurrentAuthUser )]

bcryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get ("/", status_code = status.HTTP_200_OK)
async def get_logged_user (auth: Auth_Dependency, db: DB_Dependency):
    if auth is None:
        raise HTTPException (status_code = 401, detail='Unauthorized!')
    return db.query(Auths).filter(Auths.id == auth.get('id')).first()


@router.put("/", status_code = status.HTTP_204_NO_CONTENT)
async def change_password (auth: Auth_Dependency, db: DB_Dependency, auth_verify: AuthVerificationRequestModel):
    if auth is None:
        raise HTTPException (status_code = 401, detail='Unauthorized!')

    auth_info = db.query(Auths).filter (Auths.id == auth.get('id')).first()

    if not bcryptContext.verify (auth_verify.password, auth_info.password):
        raise HTTPException (status_code = 401, detail='Error on Password Change!')
    auth_info.password = bcryptContext.hash(auth_verify.new_password)
    db.add(auth_info)
    db.commit()

@router.put("/{id}", status_code = status.HTTP_200_OK)
async def update_auth_phone_number (auth: Auth_Dependency, db: DB_Dependency, auth_req: UpdateAuthPhoneNumberRequestModel):
    if auth is None:
        raise HTTPException (status_code = 401, detail='Unauthorized!')
    auth_info = db.query(Auths).filter (Auths.id == auth.get('id')).first()
    auth_info.phone_number = auth_req.phone_number
    db.add(auth_info)
    db.commit()


