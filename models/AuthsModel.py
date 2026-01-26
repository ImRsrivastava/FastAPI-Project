from database import Base 
from sqlalchemy import Column, Integer, String, Boolean


class Auths (Base):
    __tablename__ = "auths"

    id      =   Column ( Integer, primary_key = True, index = True )
    first_name  =   Column ( String (100), unique = True )
    last_name   =   Column ( String (100) )
    username    =   Column ( String (200), unique = True )
    email       =   Column ( String (150) )
    password    =   Column ( String (255) )
    role        =   Column ( String (100) )
    is_active   =   Column ( Boolean, default = True )