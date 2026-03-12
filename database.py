import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Récupération de l'URL de la base de données depuis la variable d'environnement
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable d'environnement DATABASE_URL n'est pas définie")

# Création de l'engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # optionnel : affiche les requêtes SQL dans la console
)

# Création d'une session locale pour les requêtes
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

# Fonction get_db pour FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()