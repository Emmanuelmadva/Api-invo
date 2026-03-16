from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import models
import database
import schemas

router = APIRouter()

# tester la connection a la bd
@router.get("/test-db")
def test_db_connection(db: Session = Depends(database.get_db)):
    try:
        result = db.execute(text("SELECT NOW()"))
        current_time = result.scalar()
        return {"message": "Connexion réussie à PostgreSQL !", "server_time": str(current_time)}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erreur connexion DB: {e}")


# Clients

# enregistrer un client
@router.post("/clients", response_model=schemas.ClientResponse)
def create_client(client: schemas.ClientCreate, db: Session = Depends(database.get_db)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
# recupérer les clients
@router.get("/clients", response_model=List[schemas.ClientResponse])
def get_clients(db: Session = Depends(database.get_db)):
    return db.query(models.Client).all()
#Récupérer un client par ID
@router.get("/clients/{client_id}", response_model=schemas.ClientResponse)
def get_client(client_id: int, db: Session = Depends(database.get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client
#Modifier un client
@router.put("/clients/{client_id}", response_model=schemas.ClientResponse)
def update_client(client_id: int, client: schemas.ClientCreate, db: Session = Depends(database.get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()

    if not db_client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    for key, value in client.dict().items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client
#Supprimer un client
@router.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(database.get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    db.delete(client)
    db.commit()
    return {"message": "Client supprimé"}

# Produits

# Enregistrer un produit
@router.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
# recupérer les produits
@router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()
#Produit par ID
@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    return product
#Modifier produit
@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product
#Supprimer produit
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    db.delete(product)
    db.commit()

    return {"message": "Produit supprimé"}
# facture d'un client
@router.get("/clients/{client_id}/invoices")
def get_client_invoices(client_id: int, db: Session = Depends(database.get_db)):
    invoices = db.query(models.Invoice).filter(models.Invoice.client_id == client_id).all()
    return invoices

# Factures
# Enregistrer une facture
@router.post("/invoices", response_model=schemas.InvoiceResponse)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(database.get_db)):
    db_invoice = models.Invoice(
        id=invoice.id,
        client_id=invoice.client_id,
        client_name=invoice.client_name,
        client_email=invoice.client_email,
        client_phone=invoice.client_phone,
        client_address=invoice.client_address,
        date=invoice.date,
        total_amount=invoice.total_amount,
        notes=invoice.notes
    )
    db.add(db_invoice)
    db.commit()
    # Items
    for item in invoice.items:
        db_item = models.InvoiceItem(invoice_id=db_invoice.id, **item.dict())
        db.add(db_item)
    # Payments
    for payment in invoice.payments:
        db_payment = models.PaymentTranche(invoice_id=db_invoice.id, **payment.dict())
        db.add(db_payment)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice
# recupérer toutes les factures
@router.get("/invoices", response_model=List[schemas.InvoiceResponse])
def get_invoices(db: Session = Depends(database.get_db)):
    return db.query(models.Invoice).all()
# supprimer une facture
@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: str, db: Session = Depends(database.get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Facture non trouvée")

    db.delete(invoice)
    db.commit()

    return {"message": "Facture supprimée"}
