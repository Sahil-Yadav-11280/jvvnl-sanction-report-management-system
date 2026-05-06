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
        consumer_no,
        filepath,
    ):


        book_no , serial_no = get_next_book_serial()
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
            conn.commit()

        data = [book_no , serial_no , office , jen , date , estimate_no , description , allocation , account_number , f'{consumer_name}, {address}' , service_no  , consumer_no]

        pdf_file = generate_report(data, filepath)

        print("PDF Generated:", pdf_file)