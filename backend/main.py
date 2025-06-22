# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pdf_utils import extract_text_from_pdf
from dotenv import load_dotenv
import os
import uuid

# Load Gemini API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()

# CORS (so React can talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temp in-memory store (key: session_id, value: PDF text)
pdf_store = {}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed.")

    try:
        contents = await file.read()
        with open("temp.pdf", "wb") as f:
            f.write(contents)

        extracted_text = extract_text_from_pdf("temp.pdf")

        # Generate unique session ID
        session_id = str(uuid.uuid4())
        pdf_store[session_id] = extracted_text

        return {
            "message": "PDF uploaded and parsed successfully.",
            "session_id": session_id,
            "page_count": extracted_text.count("\n\n") + 1
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing PDF: {e}")
