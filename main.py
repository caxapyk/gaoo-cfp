import sys
from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtWidgets import QApplication
import db
from controllers.CFPController import CFPController

app = QApplication(sys.argv)
db = db.DBMySql()
db.connect()

print(QLocale.system().name())
translator = QTranslator()
translator.load("qtbase_ru.ts")
app.installTranslator(translator)

main_window = CFPController()
sys.exit(app.exec_())
