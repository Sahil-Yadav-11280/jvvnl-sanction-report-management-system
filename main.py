import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

import db
from backend import Backend

app = QApplication(sys.argv)

db.init_db()

engine = QQmlApplicationEngine()

backend = Backend()
engine.rootContext().setContextProperty("backend", backend)

engine.load("ui/main.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())