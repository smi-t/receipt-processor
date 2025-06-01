# Receipt Processing System

This project is a web application that processes scanned receipts using OCR technology and stores the extracted information in a structured database.

## Features

- Upload PDF receipts
- Validate PDF files
- Extract information using OCR
- Store data in SQLite database
- View and manage receipts through a modern web interface

## Prerequisites

- Python 3.8+
- Node.js 14+
- Tesseract OCR
- Poppler (for PDF processing)

### Installing Prerequisites

#### Windows
```bash
# Install Tesseract OCR
winget install UB-Mannheim.TesseractOCR

# Install Poppler
# Download from: http://blog.alivate.com.au/poppler-windows/
# Add the bin/ directory to your PATH
```

#### macOS
```bash
brew install tesseract
brew install poppler
```

#### Linux
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

## Project Structure

```
.
├── backend/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils/
│       └── ocr.py
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       │   ├── Navbar.js
│       │   ├── ReceiptDetails.js
│       │   ├── ReceiptList.js
│       │   └── UploadReceipt.js
│       ├── App.js
│       └── index.js
├── uploads/
├── requirements.txt
└── receipts.db
```

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd receipt-processing-system
```

2. Set up the backend:
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
cd backend
uvicorn main:app --reload
```

3. Set up the frontend:
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

### POST /upload
Upload a PDF receipt file.
- Request: `multipart/form-data` with file
- Response: Receipt file metadata

### POST /validate/{file_id}
Validate an uploaded PDF file.
- Response: Validation status and message

### POST /process/{file_id}
Process a receipt using OCR.
- Response: Processing status and extracted receipt ID

### GET /receipts
List all processed receipts.
- Response: Array of receipt objects

### GET /receipts/{id}
Get details of a specific receipt.
- Response: Receipt object with items

## Database Schema

### Receipt File Table
- id: Primary key
- file_name: Name of the uploaded file
- file_path: Storage path
- is_valid: PDF validation status
- invalid_reason: Reason for invalid status
- is_processed: Processing status
- created_at: Creation timestamp
- updated_at: Last update timestamp

### Receipt Table
- id: Primary key
- purchased_at: Purchase date/time
- merchant_name: Merchant name
- total_amount: Total amount
- file_path: Path to receipt file
- created_at: Creation timestamp
- updated_at: Last update timestamp

### Receipt Item Table
- id: Primary key
- receipt_id: Foreign key to Receipt
- item_name: Product name
- quantity: Quantity purchased
- unit_price: Price per unit
- total_price: Total item price
- created_at: Creation timestamp

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- OCR processing errors
- Database operations
- API request validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
