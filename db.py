import sqlite3

DB_NAME = "reports.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_conn() as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_no INTEGER,
            page_no INTEGER,
            purpose TEXT,
            date TEXT,
            customer_name TEXT,
            address TEXT,
            sanction_number TEXT,
            sanction_date TEXT,
            consumer_number TEXT,
            jen TEXT,
            proposed_work TEXT,
            receipt_number TEXT,
            receipt_date TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
        """)

        conn.commit()


def get_next_book_page():
    with get_conn() as conn:
        c = conn.cursor()

        c.execute("SELECT value FROM meta WHERE key='last_page'")
        row = c.fetchone()

        last_page = row[0] if row else 0

        new_page = last_page + 1
        book_no = (new_page - 1) // 100 + 1
        page_no = ((new_page - 1) % 100) + 1

        c.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('last_page', ?)",
            (new_page,)
        )

        conn.commit()
        return book_no, page_no

if __name__ == "__main__":
    init_db()