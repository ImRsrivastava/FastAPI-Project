from fastapi import APIRouter, Depends
from request_models.authRequestModel import AuthRequest, TokenRequest
from passlib.context import CryptContext
# from models.AuthsModel import Auths
from models import Auths
from starlette import status
from db.dbConfig import DB_Dependency
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from jose import jwt
from datetime import timedelta, datetime


router = APIRouter()

SECRET_KEY = "d1ed0c896e1a90d87a3d757c1063dc253241d7131a348337a9cb5dfa4d3ab42a"
ALGORITHM = "HS256"

bcryptContext = CryptContext( schemes = ['bcrypt'], deprecated = "auto" )


def authenticateAuth (username: str, password: str, db):
    auth = db.query(Auths).filter(Auths.username == username).first()
    if not auth:
        return False
    if not bcryptContext.verify(password, auth.password):
        return False
    return auth


def generateAccessToken (username: str, userId: int, expires_delta: timedelta):
    encode = { "sub": username, "id": userId }
    expires = datetime.utcnow() + expires_delta
    encode.update({ "exp": expires })
    return jwt.encode ( encode, SECRET_KEY, algorithm = ALGORITHM )



@router.post('/auth', status_code = status.HTTP_201_CREATED)
async def createAuthenticate (db: DB_Dependency, authRequest: AuthRequest):
    createAuth = Auths(
        first_name  =   authRequest.first_name,
        last_name   =   authRequest.last_name,
        username    =   authRequest.username,
        email       =   authRequest.email,
        password    =   bcryptContext.hash(authRequest.password),
        role        =   authRequest.role,
        is_active   =   True
    )

    db.add(createAuth)
    db.commit()


@router.post("/token", response_model = TokenRequest)
async def login_for_access_token (form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_Dependency):
    auth = authenticateAuth (form_data.username, form_data.password, db)

    if not auth:
        return "Authentication Failed"
    
    token = generateAccessToken ( auth.username, auth.id, timedelta(minutes = 20) )
    return { "access_token": token, "token_type": "bearer"}