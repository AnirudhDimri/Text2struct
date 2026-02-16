# Structured Data Extractor API

A high-performance FastAPI-based service that extracts structured information from raw text.

## Features

- Email extraction
- Phone number extraction
- Company name detection
- Date detection
- Address detection
- Topic extraction

## Tech Stack

- FastAPI
- spaCy
- Python 3.11

## Run Locally

1. Create virtual environment:
   py -3.11 -m venv ve

2. Activate:
   .\ve\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Download spaCy model:
   python -m spacy download en_core_web_md

5. Run:
   uvicorn app:app --reload

## Example Request

POST /extract

{
  "text": "Contact us at hello@example.com"
}


