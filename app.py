# app.py

import streamlit as st
import sqlite3

from bot_detector import is_bot
from sql_detector import needs_sql
from text_to_sql import generate_sql
from fast_result import fast_answer

st.set_page_config(
    page_title="HBD Local Business AI",
    layout="wide"
)

st.title("HBD Local Business AI")
st.caption("Search local businesses or ask general questions")

# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CHAT HISTORY ---------------- #

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ---------------- #

user_input = st.chat_input("Ask about businesses or general questions...")

if user_input:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # ---------------- BOT DETECTION ---------------- #
    if is_bot(user_input):
        with st.chat_message("assistant"):
            st.error("Suspicious or invalid query detected. Please rephrase.")
        st.stop()

    try:
        # ---------------- SQL ROUTER ---------------- #
        if needs_sql(user_input):

            # ---------- SQL FLOW ----------
            sql_query = generate_sql(user_input)

            conn = sqlite3.connect("businesses.db")
            cursor = conn.cursor()

            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            conn.close()

            if not rows:
                answer = "No matching businesses found."
            else:
                cards = []
                for row in rows:
                    record = dict(zip(columns, row))
                    cards.append(f"""
### {record.get('name')}
- 📍 **Address:** {record.get('address')}
- 📞 **Phone:** {record.get('phone_number') or 'N/A'}
- ⭐ **Rating:** {record.get('reviews_average')} ({record.get('reviews_count')} reviews)
- 🏷️ **Category:** {record.get('category')}
- 🌐 **Website:** {record.get('website') or 'N/A'}
""")
                answer = "\n---\n".join(cards)

        else:
            # ---------- NON-SQL FLOW ----------
            answer = fast_answer(user_input)

        # ---------------- RESPONSE ---------------- #
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"Something went wrong: {str(e)}")
