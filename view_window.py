from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QComboBox, QLabel, QLineEdit, QDateEdit , QFileDialog , QMessageBox
)
from PySide6.QtCore import QDate
from db import get_conn
from report_generation import generate_report
from form_window import FormWindow


class ViewWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.form = FormWindow
        self.setWindowTitle("View Reports")
        self.resize(1340, 753.75)

        self.page = 0
        self.page_size = 20
        self.active_filter = None  # ✅ filter state

        layout = QVBoxLayout()

        # 🔹 Controls
        self.control_layout = QHBoxLayout()

        self.sort_box = QComboBox()
        self.sort_box.addItems(["date"])

        self.filter_type = QComboBox()
        self.filter_type.addItems([
            "None", "office" , "jen" ,"date", "address"
        ])

        self.filter_value = QLineEdit()
        self.filter_btn = QPushButton("Filter")
        self.download_btn = QPushButton("Download Group")

        self.control_layout.addWidget(QLabel("Sort By:"))
        self.control_layout.addWidget(self.sort_box)
        self.control_layout.addWidget(QLabel("Filter By:"))
        self.control_layout.addWidget(self.filter_type)
        self.control_layout.addWidget(self.filter_value)
        self.control_layout.addWidget(self.filter_btn)
        self.control_layout.addWidget(self.download_btn)

        layout.addLayout(self.control_layout)

        # 🔹 Table
        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels(
            ["ID","Office" , "Book no" , "Serial no" , "JEN" , "Date" ,
             "Account No" , "Customer" , "Service No", "Consumer No",
             "Download", "Edit", "Delete"]
        )

        layout.addWidget(self.table)

        # 🔹 Pagination
        nav = QHBoxLayout()

        self.prev_btn = QPushButton("Prev")
        self.next_btn = QPushButton("Next")
        self.page_label = QLabel()

        nav.addWidget(self.prev_btn)
        nav.addWidget(self.page_label)
        nav.addWidget(self.next_btn)

        layout.addLayout(nav)

        self.setLayout(layout)

        # 🔗 Connections
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.sort_box.currentTextChanged.connect(self.load_data)
        self.filter_type.currentTextChanged.connect(self.update_filter_input)
        self.filter_btn.clicked.connect(self.apply_filter)
        self.download_btn.clicked.connect(self.download_group)

        self.load_data()

    # 🔄 Change input type (NO auto filtering)
    def update_filter_input(self):
        # remove old widget
        self.control_layout.removeWidget(self.filter_value)
        self.filter_value.deleteLater()

        ftype = self.filter_type.currentText()

        if ftype == "date":
            self.filter_value = QDateEdit()
            self.filter_value.setCalendarPopup(True)
            self.filter_value.setDate(QDate.currentDate())

        elif ftype == "jen":
            self.filter_value = QComboBox()
            self.filter_value.addItems(["A", "B", "C", "D"])

        elif ftype == "address":
            self.filter_value = QComboBox()
            with get_conn() as conn:
                c = conn.cursor()
                c.execute("SELECT DISTINCT address FROM reports")
                addresses = [r[0] for r in c.fetchall()]
            self.filter_value.addItems(addresses)

        elif ftype == "office":
            self.filter_value = QComboBox()
            with get_conn() as conn:
                c = conn.cursor()
                c.execute("SELECT DISTINCT office FROM reports")
                offices = [r[0] for r in c.fetchall()]
            self.filter_value.addItems(offices)

        else:
            self.filter_value = QLineEdit()

        # 👇 insert exactly after filter_type
        self.control_layout.insertWidget(4, self.filter_value)



    # ✅ Apply filter ONLY when button is pressed
    def apply_filter(self):
        ftype = self.filter_type.currentText()

        if ftype == "None":
            self.active_filter = None
        else:
            if isinstance(self.filter_value, QDateEdit):
                val = self.filter_value.date().toString("dd-MM-yyyy")
            elif isinstance(self.filter_value, QComboBox):
                val = self.filter_value.currentText()
            else:
                val = self.filter_value.text()

            self.active_filter = (ftype, val)

        self.page = 0
        self.load_data()

    # 📊 Load data
    def load_data(self):
        sort_col = self.sort_box.currentText()
        offset = self.page * self.page_size

        query = """
        SELECT id, office , book_no , serial_no , jen , date, account_number ,  consumer_name, service_no , consumer_no FROM reports
        """
        params = []

        if self.active_filter:
            ftype, val = self.active_filter
            query += f" WHERE {ftype} = ?"
            params.append(val)

        query += f" ORDER BY {sort_col} DESC LIMIT ? OFFSET ?"
        params.extend([self.page_size, offset])

        with get_conn() as conn:
            c = conn.cursor()
            c.execute(query, params)
            rows = c.fetchall()

        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

            report_id = row[0]

            # Download
            btn_download = QPushButton("Download")
            btn_download.clicked.connect(
                lambda _, rid=report_id: self.download_single(rid)
            )
            self.table.setCellWidget(i, 10, btn_download)

            # Edit
            btn_edit = QPushButton("Edit")
            btn_edit.clicked.connect(
                lambda _, rid=report_id: self.edit_report(rid)
            )
            self.table.setCellWidget(i, 11, btn_edit)

            # Delete
            btn_delete = QPushButton("Delete")
            btn_delete.clicked.connect(
                lambda _, rid=report_id: self.delete_report(rid)
            )
            self.table.setCellWidget(i, 12, btn_delete)

        total = self.get_total_rows()
        max_page = (total - 1) // self.page_size if total else 0

        self.page_label.setText(f"Page {self.page + 1} / {max_page + 1}")
        self.next_btn.setEnabled(self.page < max_page)
        self.prev_btn.setEnabled(self.page > 0)

    def get_total_rows(self):
        with get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM reports")
            return c.fetchone()[0]

    def next_page(self):
        total = self.get_total_rows()
        max_page = (total - 1) // self.page_size if total else 0

        if self.page < max_page:
            self.page += 1
            self.load_data()

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.load_data()

    def download_single(self, report_id):
        with get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM reports WHERE id=?", (report_id,))
            row = c.fetchone()

        if row:
            filename = f'report_{row[1]}_{row[2]}.pdf'
            data = row[1:]

            filepath , selected_filter = QFileDialog.getSaveFileName(
                self,
                'Save single report',
                f'{filename}',
                ''
            )

            if filepath:
                try:
                    generate_report(data , filename)
                except PermissionError:
                    QMessageBox.warning(
                        self,
                        'Cannot save file',
                        'This file is currently open in another program.\n\nPlease close it and try again.',
                        QMessageBox.Ok
                    )
            else:
                QMessageBox.information(
                    self,
                    'Save unsuccessful',
                    'No path selected, save operation cancelled',
                    QMessageBox.Ok
                )

    def delete_report(self, report_id):
        with get_conn() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM reports WHERE id=?", (report_id,))
            conn.commit()

        self.load_data()

    def edit_report(self, report_id):
        with get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM reports WHERE id=?", (report_id,))
            row = c.fetchone()

        if row:
            self.form = FormWindow(None)

            self.form.office.setText(row[3])
            self.form.jen.setCurrentText(row[4])
            self.form.date.setDate(QDate.fromString(row[5], "dd-MM-yyyy"))
            self.form.estimate_no.setText(row[6])
            self.form.estimate_date.setDate(QDate.fromString(row[7], "dd-MM-yyyy"))
            self.form.description.setText(row[8])
            self.form.allocation.setText(row[9])
            self.form.account_number.setText(row[10])
            self.form.consumer_name.setText(row[11])
            self.form.address.setText(row[12])
            self.form.mobile_no.setText(row[13])
            self.form.service_no.setText(row[14])
            self.form.consumer_no.setText(row[15])

            def update():

                office = self.form.office.text()
                date = self.form.date.date().toString("dd-MM-yyyy")
                jen = self.form.jen.currentText()
                estimate_no = self.form.estimate_no.text()
                estimate_date = self.form.estimate_date.date().toString("dd-MM-yyyy")
                description = self.form.description.toPlainText()
                allocation = self.form.allocation.text()
                account_number = self.form.account_number.text()
                consumer_name = self.form.consumer_name.text()
                address = self.form.address.text()
                mobile_no = self.form.mobile_no.text()
                service_no = self.form.service_no.text()
                consumer_no = self.form.consumer_no.text()

                if office and date and jen and description and allocation and account_number and consumer_name and address and mobile_no and service_no and consumer_no:
                    with get_conn() as conn:
                        c = conn.cursor()
                        c.execute("""
                        UPDATE reports SET
                            office=?, date=?, jen=?, estimate_no=?, estimate_date=?,
                            description=?, allocation=?, account_number=?,
                            consumer_name=?, address=?, mobile_no=?, service_no=?, consumer_no=?
                        WHERE id=?
                        """, (
                            office,
                            date,
                            jen,
                            estimate_no,
                            estimate_date,
                            description,
                            allocation,
                            account_number,
                            consumer_name,
                            address,
                            mobile_no,
                            service_no,
                            consumer_no,
                            report_id
                        ))

                        conn.commit()
                        self.form.close()
                        self.load_data()
                else:
                    QMessageBox.warning(
                        self.form,
                        'Incomplete details',
                        'Cannot submit form as one or more required fields are empty',
                        QMessageBox.Ok
                    )

            self.form.submit_btn.clicked.disconnect()
            self.form.submit_btn.clicked.connect(update)
            self.form.show()

    def download_group(self):
        ftype = None
        val = None
        if self.active_filter:
            ftype, val = self.active_filter
            query = f"SELECT * FROM reports WHERE {ftype}=?"
            params = (val,)
        else:
            query = "SELECT * FROM reports"
            params = ()

        with get_conn() as conn:
            c = conn.cursor()
            c.execute(query, params)
            rows = c.fetchall()

        from PyPDF2 import PdfMerger
        merger = PdfMerger()

        for row in rows:
            pdf = generate_report(row[1:] , f'report_{row[1]}_{row[2]}.pdf')
            merger.append(pdf)

        filepath , selected_filter = QFileDialog.getSaveFileName(
            self,
            'Merged reports download',
            f'report_{ftype}_{val}.pdf',
            ''
        )

        if filepath:
            try:
                merger.write(f"report_{ftype}_{val}.pdf")
            except PermissionError:
                QMessageBox.warning(
                    self,
                    'Cannot save file',
                    'This file is currently open in another program.\n\nPlease close it and try again.',
                    QMessageBox.Ok
                )

        else:
            QMessageBox.information(
                self,
                'Save unsuccessful',
                'No path selected, save operation cancelled',
                QMessageBox.Ok
            )

        merger.close()

        print("Group PDF created")