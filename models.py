from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey



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



class Todos (Base):
    __tablename__ = "todos"

    id      =   Column ( Integer, primary_key = True, index = True)
    user_id =   Column ( Integer, ForeignKey ("auths.id"))
    title   =   Column ( String (150) )
    description =   Column ( String (255) )
    priority    =   Column ( Integer, index = True )
    complete    =   Column ( Boolean, default = False )