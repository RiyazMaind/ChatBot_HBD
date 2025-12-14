# run_sql.py

import sqlite3
from text_to_sql import generate_sql_query

def run_query(user_text: str):
    sql_query = generate_sql_query(user_text)
    print("Generated SQL Query:", sql_query)

    conn = sqlite3.connect('businesses.db')
    cursor = conn.cursor()

    cursor.execute(sql_query)
    rows = cursor.fetchall()

    # Print results
    for row in rows:
        print(row)

    conn.close()