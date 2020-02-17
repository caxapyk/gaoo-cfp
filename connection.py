import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
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
        # db_nsa:qS4yMREesPtayIaO
        # db_oiipd:qs}@yo(j62F5
        db.setPassword(settings.value("password"))
        settings.endGroup()

        if not db.isDriverAvailable("QMYSQL"):
            print('QMYSQL driver not avaible')
            QMessageBox.critical(None, "Ошибка подключения к базе данных",
                                 self.db.lastError().text() +
                                 "QMYSQL driver not found.\n Нажмите Отмена для выхода.",
                                 QMessageBox.Cancel)
            sys.exit()

        self.db = db

    def connect(self):
        if self.db.open():
            query = "SET NAMES utf8"

            sql_query = QSqlQuery()
            sql_query.prepare(query)

            if not sql_query.exec_():
                print(sql_query.lastError().text())
                return False
        else:
            result = QMessageBox.critical(None, "Ошибка подключения к базе данных",
                                          "Настроить подключение к базе данных?",
                                          QMessageBox.Cancel | QMessageBox.Ok)
            if result == QMessageBox.Cancel:
                sys.exit()
            return False
        return True
