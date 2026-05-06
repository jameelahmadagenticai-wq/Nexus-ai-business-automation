from sqlalchemy import Column, Integer, String , DateTime
from connection import Base
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP
)

from sqlalchemy.sql import func
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)

class Memory(Base):

    __tablename__ = "memories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    memory_key = Column(
        String,
        nullable=True
    )

    content = Column(
        Text,
        nullable=False
    )

    embedding = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )