from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QDateEdit , QFileDialog , QMessageBox
)
from PySide6.QtCore import QDate
from db import get_copy_book_serial


class FormWindow(QWidget):

    def __init__(self, backend):
        super().__init__()

        self.backend = backend
        self.setWindowTitle("New Report")

        layout = QFormLayout()

        # 🔹 New Fields
        self.office = QLineEdit()

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())

        self.jen = QComboBox()
        self.jen.addItems(["A", "B", "C", "D"])

        self.estimate_no = QLineEdit()
        self.estimate_date = QDateEdit()
        self.estimate_date.setCalendarPopup(True)
        self.estimate_date.setDate(QDate.currentDate())

        self.description = QTextEdit()

        self.allocation = QLineEdit()
        self.account_number = QLineEdit()

        self.consumer_name = QLineEdit()
        self.address = QLineEdit()

        self.mobile_no = QLineEdit()

        self.service_no = QLineEdit()
        self.consumer_no = QLineEdit()

        # 🔹 Layout
        layout.addRow("Office", self.office)
        layout.addRow("Date", self.date)
        layout.addRow("JEN", self.jen)
        layout.addRow("Estimate No (optional)", self.estimate_no)
        layout.addRow("Estimate Date (optional)" , self.estimate_date)
        layout.addRow("Description of Work", self.description)
        layout.addRow("Allocation", self.allocation)
        layout.addRow("Account Number", self.account_number)
        layout.addRow("Consumer Name", self.consumer_name)
        layout.addRow("Address", self.address)
        layout.addRow("Mobile No", self.mobile_no)
        layout.addRow("Service No", self.service_no)
        layout.addRow("Consumer No", self.consumer_no)

        self.submit_btn = QPushButton("Submit")
        layout.addRow(self.submit_btn)

        self.setLayout(layout)

        self.submit_btn.clicked.connect(self.submit)

    def submit(self):
        if self.backend:

            office = self.office.text()
            date = self.date.date().toString("dd-MM-yyyy")
            jen = self.jen.currentText()
            estimate_no = self.estimate_no.text()
            estimate_date = self.estimate_date.date().toString("dd-MM-yyyy")
            description = self.description.toPlainText()
            allocation = self.allocation.text()
            account_number = self.account_number.text()
            consumer_name = self.consumer_name.text()
            address = self.address.text()
            mobile_no = self.mobile_no.text()
            service_no = self.service_no.text()
            consumer_no = self.consumer_no.text()

            if office and date and jen and description and allocation and account_number and consumer_name and address and mobile_no and service_no and consumer_no:

                book_no , serial_no = get_copy_book_serial()
                default_path = f'report_{book_no}_{serial_no}.pdf'

                file_path , selected_filter = QFileDialog.getSaveFileName(
                    self,
                    'Save your report',
                    f'{default_path}',
                    ''
                )
                if file_path:
                    try:
                            self.backend.submit_form(
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
                                file_path,
                            )
                            self.close()

                    except PermissionError:
                        QMessageBox.warning(
                            self,
                            'Cannot save file',
                            'This file is currently open in another program.\n\nPlease close it and try again',
                            QMessageBox.Ok
                        )
                else:
                    QMessageBox.information(
                        self,
                        'Save Unsuccessful',
                        'No path selected, save operation cancelled',
                        QMessageBox.Ok
                    )
            else:
                QMessageBox.warning(
                    self,
                    'Incomplete details',
                    'Cannot submit form as one or more required fields are empty',
                    QMessageBox.Ok
                )