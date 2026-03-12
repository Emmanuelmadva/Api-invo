from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import models
import database
import schemas

router = APIRouter()

# ---------------- Test DB ----------------
@router.get("/test-db")
def test_db_connection(db: Session = Depends(database.get_db)):
    try:
        result = db.execute(text("SELECT NOW()"))
        current_time = result.scalar()
        return {"message": "Connexion réussie à PostgreSQL !", "server_time": str(current_time)}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erreur connexion DB: {e}")


# ---------------- Clients ----------------
@router.post("/clients", response_model=schemas.ClientResponse)
def create_client(client: schemas.ClientCreate, db: Session = Depends(database.get_db)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/clients", response_model=List[schemas.ClientResponse])
def get_clients(db: Session = Depends(database.get_db)):
    return db.query(models.Client).all()


# ---------------- Products ----------------
@router.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()


# ---------------- Invoices ----------------
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

@router.get("/invoices", response_model=List[schemas.InvoiceResponse])
def get_invoices(db: Session = Depends(database.get_db)):
    return db.query(models.Invoice).all()