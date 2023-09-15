from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship

from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    fullname = Column(String)
    password = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())