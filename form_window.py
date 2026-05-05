# form_window.py

from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QDateEdit
)
from PySide6.QtCore import QDate


class FormWindow(QWidget):
    def __init__(self, backend):
        super().__init__()

        self.backend = backend
        self.setWindowTitle("New Report")

        layout = QFormLayout()

        self.purpose = QLineEdit()

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())

        self.name = QLineEdit()
        self.address = QLineEdit()
        self.sanction_no = QLineEdit()

        self.sanction_date = QDateEdit()
        self.sanction_date.setCalendarPopup(True)
        self.sanction_date.setDate(QDate.currentDate())

        self.consumer_no = QLineEdit()

        self.jen = QComboBox()
        self.jen.addItems(["A", "B", "C", "D"])

        self.work = QTextEdit()

        self.receipt_no = QLineEdit()

        self.receipt_date = QDateEdit()
        self.receipt_date.setCalendarPopup(True)
        self.receipt_date.setDate(QDate.currentDate())

        layout.addRow("Purpose", self.purpose)
        layout.addRow("Date", self.date)
        layout.addRow("Customer Name", self.name)
        layout.addRow("Address", self.address)
        layout.addRow("Sanction No", self.sanction_no)
        layout.addRow("Sanction Date", self.sanction_date)
        layout.addRow("Consumer No", self.consumer_no)
        layout.addRow("JEN", self.jen)
        layout.addRow("Work", self.work)
        layout.addRow("Receipt No", self.receipt_no)
        layout.addRow("Receipt Date", self.receipt_date)

        self.submit_btn = QPushButton("Submit")
        layout.addRow(self.submit_btn)

        self.setLayout(layout)

        self.submit_btn.clicked.connect(self.submit)

    def submit(self):
        if self.backend:
            self.backend.submit_form(
                self.purpose.text(),
                self.date.date().toString("dd-MM-yyyy"),
                self.name.text(),
                self.address.text(),
                self.sanction_no.text(),
                self.sanction_date.date().toString("dd-MM-yyyy"),
                self.consumer_no.text(),
                self.jen.currentText(),
                self.work.toPlainText(),
                self.receipt_no.text(),
                self.receipt_date.date().toString("dd-MM-yyyy")
            )