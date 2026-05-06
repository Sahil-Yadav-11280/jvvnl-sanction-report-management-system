import sqlite3

DB_NAME = "reports.db"


def get_conn():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_conn() as conn:
        c = conn.cursor()

        # 🔹 Main reports table
        c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            book_no INTEGER,
            serial_no INTEGER,

            office TEXT,
            jen TEXT,

            date TEXT,
            estimate_no TEXT,

            description TEXT,

            allocation TEXT,
            account_number TEXT,

            consumer_name TEXT,
            address TEXT,

            service_no TEXT,
            consumer_no TEXT
        )
        """)

        # 🔹 Meta table (for book/page logic)
        c.execute("""
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
        """)

        conn.commit()


# 🔢 Book & Serial logic (100 per book)
def get_next_book_serial():
    with get_conn() as conn:
        c = conn.cursor()

        c.execute("SELECT value FROM meta WHERE key='last_serial'")
        row = c.fetchone()

        last_serial = row[0] if row else 0

        new_serial = last_serial + 1

        # Every 100 → new book
        book_no = (new_serial - 1) // 100 + 1

        # Save updated serial
        c.execute("""
        INSERT OR REPLACE INTO meta (key, value)
        VALUES ('last_serial', ?)
        """, (new_serial,))

        conn.commit()

        return book_no, new_serial


# 📊 Optional helper (used in pagination)
def get_total_rows():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM reports")
        return c.fetchone()[0]