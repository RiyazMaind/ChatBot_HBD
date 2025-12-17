# business_by_phone.py

import sqlite3


def get_businesses_by_phone(phone: str):
    conn = sqlite3.connect("businesses.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT
            id,
            name,
            address,
            phone_number,
            reviews_average,
            reviews_count,
            category,
            subcategory,
            website,
            area
        FROM google_maps_listings
        WHERE phone_number LIKE ?
        """,
        (f"%{phone}%",)
    )

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return [dict(zip(columns, row)) for row in rows]
