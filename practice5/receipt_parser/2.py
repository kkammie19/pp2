import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Product names
products = re.findall(r"\d+\.\n(.+)", text)

# Prices
prices = re.findall(r"\d{1,3}(?: \d{3})*,\d{2}", text)

# Date and time
date_time = re.search(
    r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
    text
)

# Payment method
payment = re.search(
    r"(Банковская карта|Наличные):\s*([\d ]+,\d{2})",
    text
)

# Total
total = re.search(
    r"ИТОГО:\s*([\d ]+,\d{2})",
    text
)

result = {
    "products": products,
    "prices": prices,
    "total": total.group(1) if total else None,
    "date": date_time.group(1) if date_time else None,
    "time": date_time.group(2) if date_time else None,
    "payment_method": payment.group(1) if payment else None,
    "payment_amount": payment.group(2) if payment else None
}

print(json.dumps(result, ensure_ascii=False, indent=4))