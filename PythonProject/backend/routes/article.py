from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import or_, event

from database.db_connect import get_db, redis_client
from models.article import Article
from models.user import User
from routes.user import get_current_user

router = APIRouter()

class CreateUpdateArticleRequest(BaseModel):
    title: str = Field(..., max_length=250)
    body: str = Field(..., max_length=10000)

@event.listens_for(Article, 'before_update')
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()

@router.get("/api/articles")
async def get_articles(db=Depends(get_db)):
    articles = db.query(Article).all()
    return {
        'message': 'success',
        'articles': articles
    }

@router.post("/api/articles")
async def create_article(request: CreateUpdateArticleRequest, db=Depends(get_db)):
    title = request.title
    body = request.body
    exist_article = db.query(Article).filter(Article.title == title).first()
    if exist_article:
        return {'message': 'This title is exist'}
    
    article = Article(
        title=title,
        body=body
    )
    db.add(article)
    db.commit()
    print("Create article successfully")
    return {'message': 'success', 'data': request}

@router.put("/api/articles/{article_id}")
async def update_article(article_id: int, request: CreateUpdateArticleRequest, db=Depends(get_db)):
    exist_article = db.query(Article).get(article_id)
    if exist_article:
        exist_article.title = request.get('title', exist_article.title)
        exist_article.body = request.get('body', exist_article.body)

        db.commit()
        print("update successfully")
        return {'message': 'success', 'data': exist_article}
    
    return {'message': 'Article not found'}

@router.delete("/api/articles/{article_id}")
async def delete_article(article_id: int, db=Depends(get_db)):
    exist_article = db.query(Article).filter(Article.id == article_id).first()
    if exist_article:
        db.delete(exist_article)
        db.commit()
        return {
            'message': 'Delete article successfully'
        }
    return {
        'message': 'Article not found'
    }

@router.post("/api/articles/{article_id}/favorite")
async def favorite_article(article_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='Login first')
    
    exist_article = db.query(Article).filter(Article.id == article_id).first()
    if not exist_article:
        raise HTTPException(status_code=401, detail='Article not found')
    
    user = db.query(User).filter(User.id == current_user).first()
    exist_article.liked_users.append(user)
    db.commit()
    return {'message': 'Like article successfully'}

@router.delete("/api/articles/{article_id}/favorite")
async def unfavorite_article(article_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail='Login first')
    
    exist_article = db.query(Article).filter(Article.id == article_id).first()
    if not exist_article:
        raise HTTPException(status_code=401, detail='Article not found')
    
    user = db.query(User).filter(User.id == current_user).first()
    exist_article.liked_users.remove(user)
    db.commit()
    return {'message': 'Unlike article successfully'}