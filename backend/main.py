from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from datetime import datetime
import shutil
import PyPDF2
from typing import List

import models
import schemas
from database import engine, get_db
from utils.ocr import process_receipt

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Receipt Processing API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload", response_model=schemas.ReceiptFile)
async def upload_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a receipt file."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create database entry
    db_file = models.ReceiptFile(
        file_name=file.filename,
        file_path=file_path,
        is_valid=False,
        is_processed=False
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file

@app.post("/validate/{file_id}", response_model=schemas.ValidationResponse)
async def validate_receipt(file_id: int, db: Session = Depends(get_db)):
    """Validate if the uploaded file is a valid PDF."""
    db_file = db.query(models.ReceiptFile).filter(models.ReceiptFile.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        # Try to open and read the PDF
        with open(db_file.file_path, 'rb') as file:
            PyPDF2.PdfReader(file)
        
        db_file.is_valid = True
        db_file.invalid_reason = None
        db.commit()
        
        return {"is_valid": True, "message": "Valid PDF file"}
    except Exception as e:
        db_file.is_valid = False
        db_file.invalid_reason = str(e)
        db.commit()
        
        return {"is_valid": False, "message": f"Invalid PDF file: {str(e)}"}

@app.post("/process/{file_id}", response_model=schemas.ProcessingResponse)
async def process_receipt_file(file_id: int, db: Session = Depends(get_db)):
    """Process a receipt file using OCR and store extracted information."""
    db_file = db.query(models.ReceiptFile).filter(models.ReceiptFile.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    if not db_file.is_valid:
        raise HTTPException(status_code=400, detail="File is not valid")

    try:
        # Process receipt using OCR
        receipt_data = process_receipt(db_file.file_path)

        # Create receipt record
        db_receipt = models.Receipt(
            purchased_at=receipt_data["purchased_at"],
            merchant_name=receipt_data["merchant_name"],
            total_amount=receipt_data["total_amount"],
            file_path=db_file.file_path,
            receipt_file_id=db_file.id
        )
        db.add(db_receipt)
        db.flush()

        # Create receipt items
        for item_data in receipt_data["items"]:
            db_item = models.ReceiptItem(
                receipt_id=db_receipt.id,
                **item_data
            )
            db.add(db_item)

        # Mark file as processed
        db_file.is_processed = True
        db.commit()

        return {
            "success": True,
            "message": "Receipt processed successfully",
            "receipt_id": db_receipt.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing receipt: {str(e)}")

@app.get("/receipts", response_model=List[schemas.Receipt])
async def list_receipts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all processed receipts."""
    receipts = db.query(models.Receipt).offset(skip).limit(limit).all()
    return receipts

@app.get("/receipts/{receipt_id}", response_model=schemas.Receipt)
async def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    """Get details of a specific receipt."""
    receipt = db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt 