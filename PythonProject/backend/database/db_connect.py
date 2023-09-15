from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

# Replace the database URL with your own PostgreSQL connection details
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5433/duynguyen'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@app-postgres-1:5432/duynguyen'

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#redis_client = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=5)
redis_client = redis.Redis(host='app-redis-1', port=6379, db=0, socket_timeout=5)