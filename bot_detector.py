# bot_detector.py

import re

def is_bot(query: str) -> bool:
    if not query:
        return True

    q = query.strip()

    # Too short or too long
    if len(q) < 2 or len(q) > 300:
        return True

    # Excessive URLs
    if len(re.findall(r"http[s]?://", q)) > 2:
        return True

    # Repeated characters (spam)
    if re.search(r"(.)\1{6,}", q):
        return True

    # Too many special characters
    special_ratio = sum(not c.isalnum() and not c.isspace() for c in q) / len(q)
    if special_ratio > 0.4:
        return True

    return False


if __name__ == "__main__":
    while True:
        text = input("Enter text: ")
        print("BOT" if is_bot(text) else "HUMAN")
