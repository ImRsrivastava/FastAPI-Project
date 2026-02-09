from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Root%40123@db/todo_app"

Engine = create_engine( SQLALCHEMY_DATABASE_URL )

SessionLocal = sessionmaker( autocommit = False, autoflush = False, bind = Engine )

Base = declarative_base()


# .env content
# DOCKER_MYSQL_ROOT_PASSWORD="Root@123"
# DOCKER_MYSQL_DATABASE="todo_app"
# DOCKER_DATABASE_URL="mysql+pymysql://root:Root%40123@db/todo_app"
# DOCKER_APP_HOST_PORT=9080
# DOCKER_MY_SQL_HOST_PORT=3307
# DOCKER_VOLUME="./docker/mysql/data/"