from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy import or_, event

from database.db_connect import get_db, redis_client
from models.user import User

router = APIRouter()
security = HTTPBasic()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(LoginRequest):
    fullname: str
    username: str

@event.listens_for(User, 'before_update')
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()

def get_current_user(db=Depends(get_db)):
    current_user = redis_client.get('current_user')
    if not current_user:
        return None
    current_user_id = int(current_user.decode('utf-8'))
    return current_user_id

@router.get("/api/users")
async def get_users(db=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user:
        users = db.query(User).filter(User.id != current_user).all()
        return {
            'message': 'success',
            'users': users
        }
    users = db.query(User).all()
    return {
        'message': 'success',
        'users': users
    }

@router.post("/api/login")
async def login(request: LoginRequest, db=Depends(get_db)):
    email = request.email
    password = request.password
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid username/password')
    
    stored_password = redis_client.get(email)
    if not stored_password or stored_password.decode() != password:
        raise HTTPException(status_code=401, detail='Invalid username/password')
    
    redis_client.set('current_user', user.id)
    return user

@router.post("/api/users")
async def register(request: RegisterRequest, db=Depends(get_db)):
    email = request.email
    username = request.username
    password = request.password
    exist_user = db.query(User).filter(or_(User.email == email, User.username == username)).first()
    if exist_user:
        raise HTTPException(status_code=401, detail='User exist')
    
    user = User(
        email=request.email,
        password=request.password,
        fullname=request.fullname,
        username=request.username
    )
    db.add(user)
    db.commit()
    redis_client.set(email, password)
    request.password = '********'
    return {
        'message': 'Create user successfully',
        'data': request
    }

@router.delete("/api/users/{email}")
async def delete_user(email: str, db=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user:
        user = db.query(User).filter(User.id == current_user).first()
        if user.email == email:
            raise HTTPException(status_code=401, detail='Cannot delete yourself')
        
    exist_user = db.query(User).filter(User.email == email).first()
    if exist_user:
        db.delete(exist_user)
        db.commit()
        return {
            'message': 'Delete user successfully'
        }
    raise HTTPException(status_code=401, detail='User not found')