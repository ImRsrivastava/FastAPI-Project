from pydantic import BaseModel, Field


class AuthVerificationRequestModel (BaseModel):
    password: str
    new_password: str = Field (min_length=6)

class UpdateAuthPhoneNumberRequestModel (BaseModel):
    phone_number: str