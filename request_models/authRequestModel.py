from pydantic import BaseModel



class AuthRequest (BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: str
    is_active: bool


class TokenRequest (BaseModel):
    access_token: str
    token_type: str