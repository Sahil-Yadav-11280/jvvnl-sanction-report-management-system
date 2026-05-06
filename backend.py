from db import get_conn, get_next_book_serial, init_db
from report_generation import generate_report


class Backend:
    def __init__(self):
        init_db()

    def submit_form(
        self,
        office,
        date,
        jen,
        estimate_no,
        description,
        allocation,
        account_number,
        consumer_name,
        address,
        service_no,
        consumer_no
    ):
        # 🔢 Generate book + serial
        book_no, serial_no = get_next_book_serial()

        with get_conn() as conn:
            c = conn.cursor()

            c.execute("""
            INSERT INTO reports (
                book_no, serial_no, office, jen, date,
                estimate_no, description, allocation,
                account_number, consumer_name, address,
                service_no, consumer_no
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                book_no, serial_no, office, jen, date,
                estimate_no, description, allocation,
                account_number, consumer_name, address,
                service_no, consumer_no
            ))

            report_id = c.lastrowid
            conn.commit()

        # 📄 Generate PDF (FAST - reportlab)
        data = {
            "office": office,
            "book_no": book_no,
            "serial_no": serial_no,
            "jen": jen,
            "date": date,
            "estimate_no": estimate_no,
            "description": description,
            "allocation": allocation,
            "account_number": account_number,
            "consumer_name_address": f"{consumer_name}, {address}",
            "service_no": service_no,
            "consumer_no": consumer_no
        }

        pdf_file = generate_report(data, f"report_{report_id}.pdf")

        print("PDF Generated:", pdf_file)