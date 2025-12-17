# fast_result.py

from llm_client import call_llm
from models import MODEL


SYSTEM_PROMPT = """
You are a helpful, concise assistant.

Rules:
- Answer clearly and directly
- Keep responses short unless explanation is required
- Do NOT mention databases or SQL
- Do NOT hallucinate unknown facts
"""


def fast_answer(user_query: str) -> str:
    """
    Handles NON-SQL user queries.
    Uses LLM API directly for fast responses.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    response = call_llm(
        messages=messages,
        model=MODEL
    )

    answer = response.get("content", "").strip()

    if not answer:
        return "Sorry, I couldn't generate a response."

    return answer


if __name__ == "__main__":
    while True:
        q = input("Ask something (non-SQL): ")
        print("\nANSWER:\n", fast_answer(q))
