# sql_detector.py
from models import MODEL
import os
import requests
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

input_search = "Best SEO in chirala"

def is_sql_requred(search_query: str) -> str:
    """
    Returns ONLY:
    YES -> if query requires SQL/database access
    NO  -> otherwise
    """

    system_prompt = (
        "You are a strict classifier.\n"
        "Reply with ONLY one word: YES or NO.\n\n"
        "Reply YES if the user query requires:\n"
        "- fetching data from a database\n"
        "- SQL queries\n"
        "- filtering/searching tables (restaurants, businesses, users, orders)\n\n"
        "Reply NO for:\n"
        "- general knowledge\n"
        "- explanations\n"
        "- greetings or casual chat\n"
        "- coding help without data lookup"
    )

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": search_query}
        ],
        "temperature": 0,
        "max_tokens": 3
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    answer = response.json()["choices"][0]["message"]["content"].strip().upper()

    return "YES" if answer.startswith("YES") else "NO"

if __name__ == "__main__":
    result = is_sql_requred(input_search)
    print(f"SQL Required: {result}")