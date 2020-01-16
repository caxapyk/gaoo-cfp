import sys
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings


class Connection():

    def __init__(self):
        db = QSqlDatabase().addDatabase("QMYSQL")
        db.setConnectOptions(
            "MYSQL_OPT_CONNECT_TIMEOUT=10;MYSQL_OPT_RECONNECT=1")

        settings = QSettings()

        settings.beginGroup("Database")
        db.setHostName(settings.value("server"))
        db.setDatabaseName(settings.value("db"))
        db.setUserName(settings.value("user"))
        # qS4yMREesPtayIaO
        db.setPassword(settings.value("password"))
        settings.endGroup()

        if db.isDriverAvailable("QMYSQL"):
            print('QMYSQL driver loaded')
        else:
            QMessageBox.critical(None, "Ошибка подключения к базе данных",
                                 "QMYSQL driver not found.\n\n\
                                 Нажмите Отмена для выхода.",
                                 QMessageBox.Cancel)
            sys.exit()

        self.db = db

    def connect(self):
        if not self.db.open():
            print('Connection error: ', self.db.lastError().text())
            result = QMessageBox.critical(None, "Ошибка подключения к базе данных",
                                          "Настроить подключение к базе данных?",
                                          QMessageBox.Cancel | QMessageBox.Ok)
            if result == QMessageBox.Cancel:
                sys.exit()
            return False
        return True
