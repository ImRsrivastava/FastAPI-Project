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

# DOCKER_HUB_USERNAME="im_rsrivastava_7854"
# DOCKER_HUB_PERSONAL_ACCESS_TOKEN="dckr_pat_xBwcOFSIn6MLP_kRkTdh6P-u-7c--df"
