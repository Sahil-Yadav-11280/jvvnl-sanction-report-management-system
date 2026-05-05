from db import get_conn, get_next_book_page, init_db
from report_generation import generate_report


class Backend:
    def __init__(self):
        init_db()

    def submit_form(
        self,
        purpose,
        date,
        name,
        address,
        sanction_no,
        sanction_date,
        consumer_no,
        jen,
        work,
        receipt_no,
        receipt_date
    ):
        book_no, page_no = get_next_book_page()

        with get_conn() as conn:
            c = conn.cursor()

            c.execute("""
            INSERT INTO reports (
                book_no, page_no, purpose, date,
                customer_name, address, sanction_number,
                sanction_date, consumer_number, jen,
                proposed_work, receipt_number, receipt_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                book_no, page_no, purpose, date,
                name, address, sanction_no,
                sanction_date, consumer_no,
                jen, work, receipt_no, receipt_date
            ))

            report_id = c.lastrowid
            conn.commit()

        pdf = generate_report(
            report_id,
            book_no,
            page_no,
            purpose,
            date,
            name,
            address,
            sanction_no,
            sanction_date,
            consumer_no,
            jen,
            work,
            receipt_no,
            receipt_date
        )

        print("PDF Generated:", pdf)