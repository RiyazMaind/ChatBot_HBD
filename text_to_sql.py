# text_to_sql.py
from models import MODEL
from llm_client import call_llm


def generate_sql(query: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You generate SQLite SQL ONLY.\n\n"

                "Use ONLY this table:\n"
                "google_maps_listings\n\n"

                "Valid columns:\n"
                "id, name, address, website, phone_number,\n"
                "reviews_count, reviews_average,\n"
                "category, subcategory, city, state, area\n\n"

                "RULES:\n"
                "- Always SELECT DISTINCT * FROM google_maps_listings\n"
                "- Use LOWER(column) LIKE '%value%' for text matching\n"
                "- If city is mentioned, filter by city\n"
                "- If category/service is mentioned, filter category OR subcategory OR name\n"
                "- Exclude permanently closed businesses\n"
                "- EXCLUDE businesses with reviews_average < 3.5\n"
                "- Apply Amazon-style ranking:\n"
                "  ranking_score = reviews_average * 0.75 + reviews_count * 0.002\n"
                "- ORDER BY ranking_score DESC\n"
                "- LIMIT 5\n"
                "- Output ONLY SQL\n\n"

                "IMPORTANT:\n"
                "- High review count must NOT override poor ratings\n"
                "- A 2-star business must rank below a 4-star business\n"
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
    user_query = input("Enter your query: ")
    try:
        sql_query = generate_sql(user_query)
        print("Generated SQL Query:")
        print(sql_query)
    except Exception as e:
        print("Error generating SQL:", str(e))
