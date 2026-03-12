from fastapi import FastAPI
from api import routers, models, database, schemas

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

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)