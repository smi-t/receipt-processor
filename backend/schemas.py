from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ReceiptItemBase(BaseModel):
    item_name: str
    quantity: float
    unit_price: float
    total_price: float

class ReceiptItemCreate(ReceiptItemBase):
    pass

class ReceiptItem(ReceiptItemBase):
    id: int
    receipt_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ReceiptFileBase(BaseModel):
    file_name: str
    file_path: str

class ReceiptFileCreate(ReceiptFileBase):
    pass

class ReceiptFile(ReceiptFileBase):
    id: int
    is_valid: bool
    invalid_reason: Optional[str] = None
    is_processed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReceiptBase(BaseModel):
    purchased_at: datetime
    merchant_name: str
    total_amount: float
    file_path: str

class ReceiptCreate(ReceiptBase):
    receipt_file_id: int

class Receipt(ReceiptBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[ReceiptItem] = []

    class Config:
        from_attributes = True

class ValidationResponse(BaseModel):
    is_valid: bool
    message: str

class ProcessingResponse(BaseModel):
    success: bool
    message: str
    receipt_id: Optional[int] = None 