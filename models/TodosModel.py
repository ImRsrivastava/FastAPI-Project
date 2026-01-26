from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Todos (Base):
    __tablename__ = "todos"

    id      =   Column ( Integer, primary_key = True, index = True)
    user_id =   Column ( Integer, ForeignKey ("auths.id"))
    title   =   Column ( String (150) )
    description =   Column ( String (255) )
    priority    =   Column ( Integer, index = True )
    complete    =   Column ( Boolean, default = False )