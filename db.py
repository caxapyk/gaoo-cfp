import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QMessageBox

class DBMySql():

    def __init__(self):
        super(DBMySql, self).__init__()
        self.db = QSqlDatabase().addDatabase("QMYSQL")
        print('QMYSQL driver available: ', self.db.isDriverAvailable("QMYSQL"))
        self.db.setHostName("services.lsk.gaorel.ru")
        self.db.setDatabaseName('cfp')
        self.db.setUserName('root')
        self.db.setPassword('antilopagnu')

    def connect(self):
        if not self.db.open():
            print('Connection error: ', self.db.lastError().text())
            QMessageBox.critical(None, "Ошибка подключения к базе данных",
            "Unable to establish a database connection.\n"
            +self.db.lastError().text()+
            "\n\n"
            "Нажмите Отмена для выхода.",
            QMessageBox.Cancel)
            sys.exit()

        self.query = QSqlQuery(self.db)
        self.qstring = None
        print('Database opened:  ',self.db.isOpen())
        return True
