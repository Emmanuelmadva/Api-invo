import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("La variable d'environnement DATABASE_URL n'est pas définie !")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# fonction get_db pour les dépendances FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()