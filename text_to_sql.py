# text_to_sql.py

from models import MODEL
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

if not API_KEY:
    raise RuntimeError("OPEN_ROUTER_API_KEY not set")

TABLE_NAME = "google_maps_listings"

COLUMNS = [
    "id",
    "name",
    "address",
    "website",
    "phone_number",
    "reviews_count",
    "reviews_average",
    "category",
    "subcategory",
    "city",
    "state",
    "area",
    "created_at"
]


def generate_sql_query(user_text: str) -> str:
    system_prompt = f"""
You are a STRICT SQL generator for a business search system.

DATABASE RULES:
- Table name is ALWAYS: {TABLE_NAME}
- Allowed columns ONLY:
  {", ".join(COLUMNS)}

QUERY RULES:
1. Generate ONLY a SELECT query.
2. NEVER use = for category, city, area, state.
   ALWAYS use:
   LOWER(column) LIKE '%value%'
3. Make queries CASE-INSENSITIVE.
4. If user asks for "best", "top", or "highest rated":
   ORDER BY reviews_average DESC, reviews_count DESC
5. Always LIMIT results to 5 unless user specifies otherwise.
6. Do NOT invent columns.
7. Output ONLY raw SQL. No explanation. No markdown.

IMPORTANT:
- Be tolerant to spelling mistakes by using partial LIKE matching.
- City and category filters should be broad, not strict.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0,
        "max_tokens": 200
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
    data = response.json()

    sql_query = data["choices"][0]["message"]["content"].strip()

    return sql_query


# ---------------- TEST ----------------
if __name__ == "__main__":
    text = 'best seo businesses in chirala'

    print(generate_sql_query(text))
