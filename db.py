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
            estimate_date TEXT,

            description TEXT,

            allocation TEXT,
            account_number TEXT,

            consumer_name TEXT,
            address TEXT,
            
            mobile_no TEXT,

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

        c.execute("SELECT value FROM meta")
        row = c.fetchall()

        last_serial = row[0][0] if row else 0
        book_no = row[1][0] if row else 1

        new_serial = last_serial + 1
        if new_serial > 100:
            book_no+=1
            new_serial-=100

        # Save updated serial
        c.execute("""
        INSERT OR REPLACE INTO meta (key, value)
        VALUES ('last_serial', ?) , ('last_book' , ?)
        """, (new_serial,book_no))

        conn.commit()

        return book_no, new_serial

def get_copy_book_serial():
    with get_conn() as conn:
        c = conn.cursor()

        c.execute("SELECT value FROM meta")
        row = c.fetchall()

        last_serial = row[0][0] if row else 0
        book_no = row[1][0] if row else 1

        new_serial = last_serial + 1
        if new_serial > 100:
            book_no+=1
            new_serial-=100

        return book_no , new_serial


# 📊 Optional helper (used in pagination)
def get_total_rows():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM reports")
        return c.fetchone()[0]