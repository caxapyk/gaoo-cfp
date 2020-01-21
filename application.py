import resources
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from connection import Connection
from mainwindow import MainWindow
from dialogs import DbSettingsDialog


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)

        self.initializeDefaults()
        self.initialize()

    def initialize(self):
        if self.dbConnect():
            main_window = MainWindow()
            main_window.show()
        else:
            dbsettings_dialog = DbSettingsDialog()
            dbsettings_dialog.show()
            dbsettings_dialog.accepted.connect(self.initialize)

    def initializeDefaults(self):
        QCoreApplication.setOrganizationName("GAOO")
        QCoreApplication.setApplicationName("cfp")

        self.setWindowIcon(QIcon(":/icons/church-16.png"))

    def dbConnect(self):
        conn = Connection()
        if conn.connect():
            return True
        return False
