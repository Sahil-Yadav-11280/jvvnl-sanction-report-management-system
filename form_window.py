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

        self.description = QTextEdit()

        self.allocation = QLineEdit()
        self.account_number = QLineEdit()

        self.consumer_name = QLineEdit()
        self.address = QLineEdit()

        self.service_no = QLineEdit()
        self.consumer_no = QLineEdit()

        # 🔹 Layout
        layout.addRow("Office", self.office)
        layout.addRow("Date", self.date)
        layout.addRow("JEN", self.jen)
        layout.addRow("Estimate No", self.estimate_no)
        layout.addRow("Description of Work", self.description)
        layout.addRow("Allocation", self.allocation)
        layout.addRow("Account Number", self.account_number)
        layout.addRow("Consumer Name", self.consumer_name)
        layout.addRow("Address", self.address)
        layout.addRow("Service No", self.service_no)
        layout.addRow("Consumer No", self.consumer_no)

        self.submit_btn = QPushButton("Submit")
        layout.addRow(self.submit_btn)

        self.setLayout(layout)

        self.submit_btn.clicked.connect(self.submit)

    def submit(self):
        if self.backend:
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
                        self.office.text(),
                        self.date.date().toString("dd-MM-yyyy"),  # ✅ important
                        self.jen.currentText(),
                        self.estimate_no.text(),
                        self.description.toPlainText(),
                        self.allocation.text(),
                        self.account_number.text(),
                        self.consumer_name.text(),
                        self.address.text(),
                        self.service_no.text(),
                        self.consumer_no.text(),
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

