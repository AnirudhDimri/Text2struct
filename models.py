from pydantic import BaseModel, Field
from typing import List


class ExtractRequest(BaseModel):
    text: str = Field(..., description="Raw input text")
    extract: List[str] = Field(
        default=["emails", "phones", "companies", "dates", "addresses", "topics"],
        description="Fields to extract"
    )


class ExtractResponse(BaseModel):
    success: bool
    emails: List[str] = []
    phones: List[str] = []
    companies: List[str] = []
    dates: List[str] = []
    addresses: List[str] = []
    topics: List[str] = []
