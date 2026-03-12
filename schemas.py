from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ---------------- Clients ----------------
class ClientBase(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    class Config:
        orm_mode = True


# ---------------- Products ----------------
class ProductBase(BaseModel):
    id: str
    name: str
    price: float
    quantite: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    class Config:
        orm_mode = True


# ---------------- Invoice Items ----------------
class InvoiceItemBase(BaseModel):
    product_id: str
    product_name: str
    product_price: float
    product_quantite: int
    quantity: int
    unit_price: float
    discount_percent: float

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemResponse(InvoiceItemBase):
    class Config:
        orm_mode = True


# ---------------- Payment Tranches ----------------
class PaymentTrancheBase(BaseModel):
    id: str
    amount: float
    date: datetime
    method: Optional[str] = None
    note: Optional[str] = None
    is_confirmed: bool = False

class PaymentTrancheCreate(PaymentTrancheBase):
    pass

class PaymentTrancheResponse(PaymentTrancheBase):
    class Config:
        orm_mode = True


# ---------------- Invoices ----------------
class InvoiceBase(BaseModel):
    id: str
    client_id: str
    client_name: str
    client_email: str
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    date: datetime
    total_amount: float
    notes: Optional[str] = None
    items: List[InvoiceItemCreate] = []
    payments: List[PaymentTrancheCreate] = []

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    class Config:
        orm_mode = True