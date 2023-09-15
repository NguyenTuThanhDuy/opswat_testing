from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, select
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func

from .user_article import user_article_association
from .base import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    body = Column(String(1000))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    # Relationship with Users
    liked_users = relationship('User', secondary=user_article_association, backref='liked_by')

    favourite_count = column_property(
        select(func.count(user_article_association.c.user_id))
        .where(user_article_association.c.article_id == id)
        .correlate_except(user_article_association)
        .as_scalar()
        .label('favourite_count')
    )