import re


def parse_price(price: str) -> float:
    cleaned = re.sub(r"[^\d,\.]", "", price)
    if "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")
    return float(cleaned)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("«", '"').replace("»", '"')
    text = re.sub(r"\s+", " ", text).strip()
    return text
