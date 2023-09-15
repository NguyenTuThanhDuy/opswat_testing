from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base

# Intermediate table for the many-to-many relationship
user_article_association = Table(
    'user_article_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('article_id', Integer, ForeignKey('articles.id'))
)