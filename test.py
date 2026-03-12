from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title="Test PostgreSQL")

# Remplace par tes infos PostgreSQL
DB_USER = "postgres"
DB_PASSWORD = "theone"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "facturationdb"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crée l'engine SQLAlchemy
engine = create_engine(DATABASE_URL)

@app.get("/")
def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT NOW()"))
            current_time = result.scalar()
        return {"message": "Connexion réussie !", "server_time": str(current_time)}
    except SQLAlchemyError as e:
        return {"message": "Échec de la connexion à PostgreSQL", "error": str(e)}