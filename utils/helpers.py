def normalize_text(text: str) -> str:
    """Приводит кавычки и пробелы к единому виду."""
    text = text.strip()
    text = text.replace("«", '"').replace("»", '"')
    text = text.upper()
    return text


def parse_price(price: str) -> int:
    return int("".join(filter(str.isdigit, price)))
