from sqlalchemy import Column, String, Integer, Numeric, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# ---------------- Clients ----------------
class Client(Base):
    __tablename__ = "clients"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    address = Column(Text)

    invoices = relationship("Invoice", back_populates="client")


# ---------------- Products ----------------
class Product(Base):
    __tablename__ = "products"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(12,2), nullable=False)
    quantite = Column(Integer)


# ---------------- Invoices ----------------
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String(50), primary_key=True, index=True)
    client_id = Column(String(50), ForeignKey("clients.id"), nullable=False)
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255), nullable=False)
    client_phone = Column(String(50))
    client_address = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Numeric(12,2), nullable=False)
    notes = Column(Text)

    client = relationship("Client", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("PaymentTranche", back_populates="invoice", cascade="all, delete-orphan")


# ---------------- Invoice Items ----------------
class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_id = Column(String(50), ForeignKey("invoices.id"), nullable=False)
    product_id = Column(String(50), nullable=False)
    product_name = Column(String(255), nullable=False)
    product_price = Column(Numeric(12,2), nullable=False)
    product_quantite = Column(Integer, nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12,2), nullable=False, default=0)
    discount_percent = Column(Numeric(5,2), nullable=False, default=0)

    invoice = relationship("Invoice", back_populates="items")


# ---------------- Payment Tranches ----------------
class PaymentTranche(Base):
    __tablename__ = "payment_tranches"
    id = Column(String(50), primary_key=True, index=True)
    invoice_id = Column(String(50), ForeignKey("invoices.id"), nullable=False)
    amount = Column(Numeric(12,2), nullable=False)
    date = Column(DateTime, nullable=False)
    method = Column(String(50))
    note = Column(Text)
    is_confirmed = Column(Boolean, default=False)

    invoice = relationship("Invoice", back_populates="payments")