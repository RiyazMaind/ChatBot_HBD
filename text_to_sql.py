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
                "Rules:\n"
                "- Always SELECT * FROM google_maps_listings\n"
                "- Use LIKE with % for text matching\n"
                "- If city is mentioned, filter city\n"
                "- If category/service is mentioned, filter category\n"
                "- Exclude permanently closed businesses\n"
                "- ORDER BY reviews_average DESC\n"
                "- LIMIT 5\n"
                "- Output ONLY SQL"
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