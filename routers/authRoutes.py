from fastapi import APIRouter, Depends, HTTPException, Request
from request_models.authRequestModel import AuthRequest, TokenRequest
from passlib.context import CryptContext
# from models.AuthsModel import Auths
from models import Auths
from starlette import status
from db.dbConfig import DB_Dependency
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix = "/auth",
    tags = [ "Auth-Routes" ]
)

SECRET_KEY = "d1ed0c896e1a90d87a3d757c1063dc253241d7131a348337a9cb5dfa4d3ab42a"
ALGORITHM = "HS256"

bcryptContext = CryptContext( schemes = ['bcrypt'], deprecated = "auto" )
oauth2Bearer = OAuth2PasswordBearer(tokenUrl = "auth/login")
templates = Jinja2Templates(directory = "templates")

##### HTML Page Loading #####
@router.get("/login")
def render_login_page (request: Request):
    return templates.TemplateResponse('login.html', {"request": request})


##### HTML Page Loading End #####






def authenticateAuth (username: str, password: str, db):
    auth = db.query(Auths).filter(Auths.username == username).first()
    if not auth:
        return False
    if not bcryptContext.verify(password, auth.password):
        return False
    return auth


def generateAccessToken (username: str, userId: int, role: str, expires_delta: timedelta):
    encode = { "sub": username, "id": userId, "role": role }
    expires = datetime.utcnow() + expires_delta
    encode.update({ "exp": expires })
    return jwt.encode ( encode, SECRET_KEY, algorithm = ALGORITHM )


async def getCurrentAuthUser (token: Annotated[str, Depends(oauth2Bearer)]):
    try:
        payload = jwt.decode( token, SECRET_KEY, algorithms=[ALGORITHM] )
        userName: str = payload.get("sub")
        userId: int = payload.get("id")
        role: str = payload.get("role")

        if userName is None or userId is None:
            raise HTTPException ( status_code = status.HTTP_401_UNAUTHORIZED, detail = "Not able to validate the user.")
        return { "username": userName, "id": userId, "auth_role": role }
    except JWTError:
        raise HTTPException ( status_code = status.HTTP_401_UNAUTHORIZED, detail = "Not able to validate the user.")


@router.post('/', status_code = status.HTTP_201_CREATED)
async def create_authenticate (db: DB_Dependency, authRequest: AuthRequest):
    createAuth = Auths(
        first_name  =   authRequest.first_name,
        last_name   =   authRequest.last_name,
        username    =   authRequest.username,
        email       =   authRequest.email,
        password    =   bcryptContext.hash(authRequest.password),
        role        =   authRequest.role,
        phone_number=   authRequest.phone_number,
        is_active   =   True
    )

    db.add(createAuth)
    db.commit()


@router.post("/login", response_model = TokenRequest)
async def login_for_access_token (form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_Dependency):
    auth = authenticateAuth (form_data.username, form_data.password, db)

    if not auth:
        raise HTTPException ( status_code = status.HTTP_401_UNAUTHORIZED, detail = "Not able to validate the user.")
    
    token = generateAccessToken ( auth.username, auth.id, auth.role, timedelta(minutes = 20) )
    return { "access_token": token, "token_type": "bearer"}