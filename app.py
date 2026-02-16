import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ExtractRequest, ExtractResponse
from extractor import extract_structured_data

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Structured Data Extraction API",
    version="1.0.0",
    description="Extract structured information from raw text."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Structured Data Extraction API",
        "version": "1.0.0",
        "endpoints": {
            "POST /extract": "Extract structured data",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/extract", response_model=ExtractResponse)
def extract(request: ExtractRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        result = extract_structured_data(
            text=request.text,
            fields=request.extract
        )
        return ExtractResponse(success=True, **result)

    except Exception as e:
        logging.exception("Extraction failed")
        raise HTTPException(status_code=500, detail=str(e))
