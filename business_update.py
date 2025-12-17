# business_update.py

import sqlite3

ALLOWED_FIELDS = [
    "name",
    "address",
    "phone_number",
    "website",
    "category",
    "subcategory",
    "area"
]

def update_business(business_id: int, updates: dict):
    updates = {k: v for k, v in updates.items() if k in ALLOWED_FIELDS}

    if not updates:
        return False

    fields = []
    values = []

    for k, v in updates.items():
        fields.append(f"{k} = ?")
        values.append(v)

    values.append(business_id)

    query = f"""
        UPDATE google_maps_listings
        SET {', '.join(fields)}
        WHERE id = ?
    """

    conn = sqlite3.connect("businesses.db")
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return True
