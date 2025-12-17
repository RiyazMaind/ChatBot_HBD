# app.py

import streamlit as st
import sqlite3

from bot_detector import is_bot
from sql_detector import needs_sql
from text_to_sql import generate_sql
from fast_result import fast_answer
from business_by_phone import get_businesses_by_phone
from business_health import get_update_suggestions
from business_update import update_business

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="HBD Local Business AI",
    layout="wide"
)

st.title("HBD Local Business AI")
st.caption("Search local businesses, manage and update your business profile")

# ---------------- SESSION STATE ---------------- #

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "phone" not in st.session_state:
    st.session_state.phone = None

if "businesses" not in st.session_state:
    st.session_state.businesses = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_update" not in st.session_state:
    st.session_state.show_update = False

# ---------------- PHONE LOGIN ---------------- #

if not st.session_state.authenticated:
    st.subheader("📞 Enter your phone number to continue")

    phone = st.text_input(
        "Phone Number",
        placeholder="e.g. 093466 93525"
    )

    if st.button("Continue"):
        phone = phone.strip()

        if len(phone) < 6:
            st.error("Please enter a valid phone number")
        else:
            businesses = get_businesses_by_phone(phone)

            if not businesses:
                st.error("No businesses found for this phone number")
            else:
                st.session_state.authenticated = True
                st.session_state.phone = phone
                st.session_state.businesses = businesses
                st.success("Phone number verified")
                st.rerun()

    st.stop()

# ---------------- BUSINESS DASHBOARD ---------------- #

st.subheader("🏢 Your Business(es)")

for biz in st.session_state.businesses:
    st.markdown(f"""
### {biz.get('name')}
- 📍 **Address:** {biz.get('address')}
- 📞 **Phone:** {biz.get('phone_number')}
- ⭐ **Rating:** {biz.get('reviews_average')} ({biz.get('reviews_count')} reviews)
- 🏷️ **Category:** {biz.get('category')}
- 🌐 **Website:** {biz.get('website') or 'N/A'}
""")

st.divider()

# ---------------- UPDATE BUSINESS BUTTON ---------------- #

if st.button("✏️ Update My Business"):
    st.session_state.show_update = True

# ---------------- UPDATE PANEL ---------------- #

if st.session_state.show_update:
    st.subheader("🛠️ Update Your Business Details")

    # Assuming one business per phone (can be extended later)
    business = st.session_state.businesses[0]
    business_id = business["id"]

    # ---- Suggestions ----
    suggestions = get_update_suggestions(business)

    if suggestions:
        st.warning("Suggestions to improve your business profile:")
        for s in suggestions:
            st.markdown(f"- {s}")
    else:
        st.success("Your business profile looks complete 🎉")

    st.divider()

    # ---- Update Form ----
    with st.form("update_business_form"):
        name = st.text_input("Business Name", value=business.get("name") or "")
        address = st.text_input("Address", value=business.get("address") or "")
        phone_number = st.text_input("Phone Number", value=business.get("phone_number") or "")
        website = st.text_input("Website", value=business.get("website") or "")
        category = st.text_input("Category", value=business.get("category") or "")
        subcategory = st.text_input("Subcategory", value=business.get("subcategory") or "")
        area = st.text_input("Area", value=business.get("area") or "")

        save = st.form_submit_button("Save Changes")
        cancel = st.form_submit_button("Cancel")

    if save:
        updates = {
            "name": name,
            "address": address,
            "phone_number": phone_number,
            "website": website,
            "category": category,
            "subcategory": subcategory,
            "area": area,
        }

        update_business(business_id, updates)

        st.success("✅ Business details updated successfully")
        st.session_state.show_update = False

        # Refresh business data
        st.session_state.businesses = get_businesses_by_phone(st.session_state.phone)
        st.rerun()

    if cancel:
        st.session_state.show_update = False
        st.rerun()

st.divider()

# ---------------- CHAT / SEARCH ---------------- #

st.subheader("💬 Ask or Search")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about businesses or general questions...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    if is_bot(user_input):
        with st.chat_message("assistant"):
            st.error("Invalid or suspicious input detected")
        st.stop()

    try:
        if needs_sql(user_input):
            sql_query = generate_sql(user_input)

            conn = sqlite3.connect("businesses.db")
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()

            seen = set()
            answer = ""

            for row in rows:
                record = dict(zip(columns, row))
                if record["name"] in seen:
                    continue
                seen.add(record["name"])

                answer += f"""
### {record.get('name')}
- 📍 {record.get('address')}
- 📞 {record.get('phone_number')}
- ⭐ {record.get('reviews_average')} ({record.get('reviews_count')} reviews)
- 🏷️ {record.get('category')}
- 🌐 {record.get('website') or 'N/A'}
---
"""

            if not answer:
                answer = "No results found."

        else:
            answer = fast_answer(user_input)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(str(e))
