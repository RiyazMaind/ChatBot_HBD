# llm_client.py

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Load multiple API keys (comma-separated)
raw_keys = os.getenv("OPEN_ROUTER_API_KEYS", "")
API_KEYS = [k.strip() for k in raw_keys.split(",") if k.strip()]

if not API_KEYS:
    raise RuntimeError("No OpenRouter API keys found in .env")

# Simple round-robin index
_key_index = 0


def _get_next_key():
    global _key_index
    key = API_KEYS[_key_index]
    _key_index = (_key_index + 1) % len(API_KEYS)
    return key


def call_llm(messages, model, max_retries=2):
    last_error = None

    for attempt in range(max_retries):
        for _ in range(len(API_KEYS)):
            api_key = _get_next_key()

            try:
                response = requests.post(
                    OPENROUTER_URL,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "http://localhost",
                        "X-Title": "HBD-Local-Business-AI"
                    },
                    json={
                        "model": model,
                        "messages": messages
                    },
                    timeout=30
                )

                # ----- Rate limit -----
                if response.status_code == 429:
                    print("⚠️ Rate limit hit, switching API key...")
                    time.sleep(0.5)
                    continue

                # ----- Invalid / exhausted key -----
                if response.status_code in (401, 403):
                    print("❌ Invalid or exhausted API key, switching...")
                    continue

                # ----- Other errors -----
                if response.status_code != 200:
                    print("OpenRouter error:", response.status_code, response.text)
                    last_error = response.text
                    continue

                return response.json()["choices"][0]["message"]

            except requests.exceptions.RequestException as e:
                last_error = e
                continue

    raise RuntimeError(f"LLM call failed after retries: {last_error}")