import re
from datetime import datetime

DEFAULT_YEAR = 2025

def extract_symbol_and_date(question):
    """
    Extracts symbol (like BTCUSDT) and date from a question.
    Handles:
      - 'on June 15 2025'
      - 'on June 15'
      - '2025-06-15'
    """

    question_upper = question.upper()
    question_clean = question.strip()


    symbol_match = re.search(r"\b([A-Z]{3,10}USDT)\b", question_upper)
    symbol = symbol_match.group(1) if symbol_match else None

   
    iso_date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", question_clean)
    if iso_date_match:
        try:
            date_obj = datetime.fromisoformat(iso_date_match.group(1))
            return symbol, date_obj.date()
        except ValueError:
            pass

    
    date_match = re.search(r"on ([A-Za-z]+ \d{1,2}(?: \d{4})?)", question_clean, flags=re.IGNORECASE)
    if date_match:
        date_str = date_match.group(1)
        try:
            if re.search(r"\d{4}", date_str):
                date_obj = datetime.strptime(date_str, "%B %d %Y")
            else:
                date_obj = datetime.strptime(f"{date_str} {DEFAULT_YEAR}", "%B %d %Y")
            return symbol, date_obj.date()
        except ValueError:
            pass

    
    return symbol, None
