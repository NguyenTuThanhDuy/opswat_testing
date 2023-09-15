from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db_connect import engine
from models.base import Base
from routes.user import router as user_router
from routes.article import router as article_router


app = FastAPI()

# Allow these methods to be used
methods = ["GET", "POST", "PUT", "DELETE"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=methods
)

app.include_router(user_router)
app.include_router(article_router)

try:
    Base.metadata.create_all(bind=engine)
    print("Successful")
except:
    print("Failed to create")