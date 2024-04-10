from pydantic import BaseModel
from typing import List

class InvoiceNumber(BaseModel):
    invoice_number: str

class InvoiceDate(BaseModel):
    invoice_date: str

class ClientAddress(BaseModel):
    client_address: str

class ClientTaxID(BaseModel):
    client_tax_id: str

class SellerName(BaseModel):
    seller_name: str

class SellerAddress(BaseModel):
    seller_address: str

class NamesOfInvoiceItems(BaseModel):
    names_of_invoice_items: List[str]

class GrossWorthOfInvoiceItems(BaseModel):
    gross_worth_of_invoice_items: List[float]

class TotalGrossWorth(BaseModel):
    total_gross_worth: str

class SellerTaxID(BaseModel):
    seller_tax_id: str

class ClientName(BaseModel):
    client_name: str
class_names = [
    InvoiceNumber,
    InvoiceDate,
    ClientAddress,
    ClientTaxID,
    SellerName,
    SellerAddress,
    NamesOfInvoiceItems,
    GrossWorthOfInvoiceItems,
    TotalGrossWorth,
    SellerTaxID,
    ClientName
]