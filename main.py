import sys
from PyQt5.QtCore import (QTranslator, QLocale)
from PyQt5.QtWidgets import QApplication
import db
import resources

from views.mainview import MainWindowView
from views.geoview import GEOView


app = QApplication(sys.argv)
db = db.DBMySql()
db.connect()

# russian translation
qtTranslator = QTranslator()
if qtTranslator.load(QLocale(), ":/qtbase_ru.qm"):
    app.installTranslator(qtTranslator)

main_window = MainWindowView()
geoview = GEOView(main_window)

sys.exit(app.exec_())
