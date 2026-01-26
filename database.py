from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost/udemy_todo_app"

Engine = create_engine( SQLALCHEMY_DATABASE_URL )

SessionLocal = sessionmaker( autocommit = False, autoflush = False, bind = Engine )

Base = declarative_base()