# sql_detector.py

from llm_client import call_llm
from models import MODEL


def needs_sql(query: str) -> bool:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a STRICT intent classifier.\n\n"
                "Your task is to decide whether the user's query requires "
                "querying a business database.\n\n"
                "Reply with ONLY ONE WORD:\n"
                "YES  -> if the query is about finding businesses, services, "
                "shops, companies, restaurants, or locations\n"
                "NO   -> if the query is general knowledge, explanation, or chit-chat\n\n"
                "IMPORTANT RULES:\n"
                "- DO NOT generate SQL\n"
                "- DO NOT explain your answer\n"
                "- DO NOT add formatting, markdown, or code blocks\n"
                "- Output must be EXACTLY either YES or NO"
            )
        },
        {
            "role": "user",
            "content": query
        }
    ]

    res = call_llm(messages, model=MODEL)
    decision = res["content"].strip().upper()

    print("SQL ROUTER:", decision)
    return decision == "YES"


if __name__ == "__main__":
    test_query = input("Enter your query to check for SQL need: ")

    if needs_sql(test_query):
        print("YES SQL is required")
    else:
        print("NO SQL is not required")
