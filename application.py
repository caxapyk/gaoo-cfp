import resources
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import (QCoreApplication, QTranslator, QLocale)
from PyQt5.QtGui import QIcon
from connection import Connection
from mainwindow import MainWindow


class Application(QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        self.initializeDefaults()
        self.openConnection()

        main_window = MainWindow()
        main_window.show()

    def initializeDefaults(self):
        QCoreApplication.setOrganizationName("GAOO")
        QCoreApplication.setApplicationName("cfp")

        qtTranslator = QTranslator()
        if qtTranslator.load(QLocale(), ":/qtbase_ru.qm"):
            QCoreApplication.installTranslator(qtTranslator)

        self.setWindowIcon(QIcon(":/icons/church-16.png"))

    def openConnection(self):
        conn = Connection()
        if conn.connect():
            print("Connected to database.")
