import sys
from PyQt5.QtWidgets import QApplication
import db
from controllers.CFPController import CFPController

app = QApplication(sys.argv)
db = db.DBMySql()
db.connect()

main_window = CFPController()
sys.exit(app.exec_())
