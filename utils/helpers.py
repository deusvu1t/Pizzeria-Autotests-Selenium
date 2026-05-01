def normalize_text(text: str) -> str:
    return text.strip().replace("«", '"').replace("»", '"').upper()


def parse_price(price: str) -> int:
    cleaned = price.replace("₽", "").replace("\u00a0", "").strip()
    cleaned = cleaned.replace(" ", "")
    if "," in cleaned:
        cleaned = cleaned.split(",")[0]
    elif "." in cleaned:
        cleaned = cleaned.split(".")[0]
    return int(cleaned)
