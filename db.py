import sys
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMessageBox


class Connection():

    def __init__(self):
        super(Connection, self).__init__()
        db = QSqlDatabase().addDatabase("QMYSQL")

        db.setHostName("services.lsk.gaorel.ru")
        db.setDatabaseName('cfp')
        db.setUserName('db_nsa')
        db.setPassword('qS4yMREesPtayIaO')

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
            QMessageBox.critical(None, "Ошибка подключения к базе данных",
                                 "Unable to establish a database connection. %s\n\
                                 \n\nНажмите Отмена для выхода."
                                 % self.db.lastError().text(),
                                 QMessageBox.Cancel)
            sys.exit()
        return True
