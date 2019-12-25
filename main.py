import sys
from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtWidgets import QApplication
import db

from views.mainview import MainWindowView
from views.geoview import GEOView


app = QApplication(sys.argv)
db = db.DBMySql()
db.connect()

print(QLocale.system().name())
translator = QTranslator()
translator.load("qtbase_ru.ts")
app.installTranslator(translator)

main_window = MainWindowView()
geoview = GEOView(main_window)

sys.exit(app.exec_())
