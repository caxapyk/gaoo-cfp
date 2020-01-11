import sys, db, resources
from PyQt5.QtCore import (QTranslator, QLocale)
from PyQt5.QtWidgets import QApplication

from main import MainWindow

app = QApplication(sys.argv)

# russian translation
qtTranslator = QTranslator()
if qtTranslator.load(QLocale(), ":/qtbase_ru.qm"):
    app.installTranslator(qtTranslator)

# connect to database
db.Connection().connect()

# open main window
MainWindow().show()

sys.exit(app.exec_())
