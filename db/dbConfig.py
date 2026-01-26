from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated


def DB_Connection ():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DB_Dependency =   Annotated[ Session, Depends(DB_Connection) ]
