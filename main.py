import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
)


from backend import Backend
from form_window import FormWindow
from view_window import ViewWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.backend = Backend()

        self.setWindowTitle("Report Manager")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.new_btn = QPushButton("New Report")
        layout.addWidget(self.new_btn)

        self.setLayout(layout)

        self.new_btn.clicked.connect(self.open_form)
        self.view_btn = QPushButton("View Reports")
        layout.addWidget(self.view_btn)

        self.view_btn.clicked.connect(self.open_view)

    def open_form(self):
        self.form = FormWindow(self.backend)
        self.form.show()

    def open_view(self):
        self.view = ViewWindow()
        self.view.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())