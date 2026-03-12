from fastapi import FastAPI
import routers, models, database

app = FastAPI(
    title="Facturation API",
    description="API pour la synchronisation des clients, produits et factures",
    version="1.0.0"
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(
    routers.router,
    prefix="/api",
    tags=["Facturation"]
)