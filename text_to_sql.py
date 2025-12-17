# text_to_sql.py
from models import MODEL
from llm_client import call_llm


def generate_sql(query: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You generate SQLite SQL ONLY for a local business search engine.\n\n"

                "TABLE:\n"
                "google_maps_listings\n\n"

                "COLUMNS:\n"
                "id, name, address, website, phone_number,\n"
                "reviews_count, reviews_average,\n"
                "category, subcategory, city, state, area\n\n"

                "MANDATORY RULES:\n"
                "1. ALWAYS use SELECT DISTINCT * FROM google_maps_listings\n"
                "2. ALWAYS use AND between city and business intent filters\n"
                "3. Match business intent using PARTIAL ROOT WORDS\n"
                "   (example: ayurvedic -> ayurved, restaurant -> restaur)\n"
                "4. Match intent across name OR category OR subcategory\n"
                "5. Use LOWER(column) LIKE '%root%'\n"
                "6. EXCLUDE businesses with reviews_average < 3.0\n"
                "7. Ranking formula:\n"
                "   score = reviews_average * 0.75 + reviews_count * 0.002\n"
                "8. ORDER BY score DESC\n"
                "9. LIMIT 5\n"
                "10. Output ONLY valid SQL\n\n"

                "IMPORTANT SPELLING TOLERANCE:\n"
                "- Handle spelling mistakes (aayurvedic, ayurvedik)\n"
                "- Use root matching instead of full words\n"
                "- NEVER return unrelated categories\n"
            )
        },
        {"role": "user", "content": query}
    ]

    response = call_llm(messages, model=MODEL)
    sql = response["content"].strip()

    if not sql.upper().startswith("SELECT"):
        raise ValueError("Invalid SQL generated")

    return sql
if __name__ == "__main__":
    while True:
        q = input("Enter your business search query: ")
        print("\nGENERATED SQL:\n", generate_sql(q))