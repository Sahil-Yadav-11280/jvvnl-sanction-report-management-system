from PySide6.QtCore import QObject, Slot
import db
from Report_generation import generate_report


class Backend(QObject):

    @Slot(str, str, str, str, str, str, str, str, str, str, str)
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
        book_no, page_no = db.get_next_book_page()

        with db.get_conn() as conn:
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

        pdf_path = generate_report(
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

        print(f"Generated: {pdf_path}")