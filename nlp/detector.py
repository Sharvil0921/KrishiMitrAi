import re
from nlp.patterns import PATTERNS
from data.crop_db import CROP_DB
from data.disease_db import DISEASE_DB


def detect_intent(text: str) -> str:
    """Return the detected intent category for the given text."""
    tl = text.lower()
    for intent, pats in PATTERNS.items():
        if any(re.search(p, tl) for p in pats):
            return intent
    return 'general'


def detect_crop(text: str):
    """Return the matched crop name or None. Uses word boundaries to avoid 'price' matching 'rice'."""
    tl = text.lower()
    for crop, d in CROP_DB.items():
        # English: match whole word only using regex boundaries
        if re.search(rf'\b{crop}\b', tl):
            return crop
        # Hindi/Marathi: substring match is usually okay for these scripts
        if d['hi'] in text or d['mr'] in text:
            return crop
    return None


def detect_symptom(text: str):
    """Return the matched disease symptom key or None."""
    tl = text.lower()
    for sym in DISEASE_DB:
        if sym in tl or any(w in tl for w in sym.split()):
            return sym
    return None
