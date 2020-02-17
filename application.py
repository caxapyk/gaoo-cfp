import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from connection import Connection
from mainwindow import MainWindow
from dialogs import (DbSettingsDialog, DocSearchDialog)
from PyQt5.QtCore import (QTranslator, QLocale)


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)

        self.initializeDefaults()
        self.initialize()

    def initialize(self):
        if self.dbConnect():
            if len(sys.argv) > 1 and sys.argv[1] == "--searchmode":
                main_window = DocSearchDialog()
            else:
                main_window = MainWindow()

            main_window.show()
        else:
            dbsettings_dialog = DbSettingsDialog()
            dbsettings_dialog.show()
            dbsettings_dialog.accepted.connect(self.initialize)

    def initializeDefaults(self):
        QCoreApplication.setOrganizationName("GAOO")
        QCoreApplication.setApplicationName("cfp")

        qtTranslator = QTranslator()
        if qtTranslator.load(QLocale(), ":/qtbase_ru.qm"):
            QCoreApplication.installTranslator(qtTranslator)

        self.setWindowIcon(QIcon(":/icons/church-16.png"))

    def dbConnect(self):
        conn = Connection()
        if conn.connect():
            return True
        return False
