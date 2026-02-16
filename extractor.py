import re
import spacy
import phonenumbers
from collections import Counter
from dateutil import parser
from typing import Dict, List
import string

# Load spaCy model once
nlp = spacy.load("en_core_web_md")

EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

STOPWORDS = set(spacy.lang.en.stop_words.STOP_WORDS)


def extract_emails(text: str) -> List[str]:
    return list(set(re.findall(EMAIL_REGEX, text)))


def extract_phones(text: str) -> List[str]:
    phones = set()
    for match in phonenumbers.PhoneNumberMatcher(text, None):
        number = phonenumbers.format_number(
            match.number,
            phonenumbers.PhoneNumberFormat.E164
        )
        phones.add(number)
    return list(phones)


def extract_companies(text: str) -> List[str]:
    doc = nlp(text)
    return list(set(ent.text.strip() for ent in doc.ents if ent.label_ == "ORG"))


def extract_addresses(text: str) -> List[str]:
    doc = nlp(text)
    return list(set(
        ent.text.strip()
        for ent in doc.ents
        if ent.label_ in ["GPE", "LOC"]
    ))


def extract_dates(text: str) -> List[str]:
    potential_dates = []
    words = text.split()

    for word in words:
        try:
            dt = parser.parse(word, fuzzy=False)
            potential_dates.append(dt.strftime("%Y-%m-%d"))
        except Exception:
            continue

    return list(set(potential_dates))


def extract_topics(text: str) -> List[str]:
    doc = nlp(text.lower())

    words = [
        token.text
        for token in doc
        if token.is_alpha
        and token.text not in STOPWORDS
        and token.text not in string.punctuation
    ]

    most_common = Counter(words).most_common(5)
    return [word for word, _ in most_common]


def extract_structured_data(text: str, fields: List[str]) -> Dict:
    result = {
        "emails": [],
        "phones": [],
        "companies": [],
        "dates": [],
        "addresses": [],
        "topics": []
    }

    if "emails" in fields:
        result["emails"] = extract_emails(text)

    if "phones" in fields:
        result["phones"] = extract_phones(text)

    if "companies" in fields:
        result["companies"] = extract_companies(text)

    if "addresses" in fields:
        result["addresses"] = extract_addresses(text)

    if "dates" in fields:
        result["dates"] = extract_dates(text)

    if "topics" in fields:
        result["topics"] = extract_topics(text)

    return result
