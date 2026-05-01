def normalize_text(text: str) -> str:
    """Приводит кавычки и пробелы к единому виду."""
    text = text.strip()
    text = text.replace("«", '"').replace("»", '"')
    text = text.upper()
    return text


def parse_price(price: str) -> int:
    price = price.replace("₽", "").strip()

    # убираем копейки
    if "," in price:
        price = price.split(",")[0]
    elif "." in price:
        price = price.split(".")[0]

    return int(price)
