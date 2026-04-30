def normalize_text(text: str) -> str:
    """Приводит кавычки и пробелы к единому виду."""
    text = text.strip()
    text = text.replace("«", '"').replace("»", '"')
    text = text.upper()
    return text
