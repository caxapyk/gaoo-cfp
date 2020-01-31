from PyQt5.QtCore import QSettings
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi


class DbSettingsDialog(QDialog):
    def __init__(self):
        super(DbSettingsDialog, self).__init__()
        ui = loadUi("ui/dbsettings_dialog.ui", self)
        ui.setWindowIcon(QIcon(":/icons/church-16.png"))

        settings = QSettings()
        settings.beginGroup("Database")
        ui.lineEdit_server.setText(settings.value("server"))
        ui.lineEdit_db.setText(settings.value("db"))
        ui.lineEdit_user.setText(settings.value("user"))
        ui.lineEdit_dbpass.setText(settings.value("password"))
        settings.endGroup()

        ui.pushButton_test.clicked.connect(self.testAction)
        ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        ui.lineEdit_server.textChanged.connect(self.dataChanged)
        ui.lineEdit_db.textChanged.connect(self.dataChanged)
        ui.lineEdit_user.textChanged.connect(self.dataChanged)
        ui.lineEdit_dbpass.textChanged.connect(self.dataChanged)

        ui.buttonBox.button(
            QDialogButtonBox.Cancel).clicked.connect(self.reject)

        self.ui = ui

    def testAction(self):
        db = QSqlDatabase()
        if not db.contains("db_test"):
            test_db = db.addDatabase("QMYSQL", "db_test")
        else:
            test_db = db.database("db_test")

        test_db.setHostName(self.ui.lineEdit_server.text())
        test_db.setDatabaseName(self.ui.lineEdit_db.text())
        test_db.setUserName(self.ui.lineEdit_user.text())
        test_db.setPassword(self.ui.lineEdit_dbpass.text())

        test_db.setConnectOptions("MYSQL_OPT_CONNECT_TIMEOUT=5")

        label = self.ui.label_status
        if test_db.open():
            label.setStyleSheet("color: green")
            label.setText("Подключение успешно!")

            self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
            self.ui.buttonBox.button(
                QDialogButtonBox.Ok).clicked.connect(self.saveSettings)
        else:
            label.setStyleSheet("color: red")
            label.setText("Подключение не выполнено!")

    def saveSettings(self):
        settings = QSettings()
        settings.beginGroup("Database")
        settings.setValue("server", self.ui.lineEdit_server.text())
        settings.setValue("db", self.ui.lineEdit_db.text())
        settings.setValue("user", self.ui.lineEdit_user.text())
        settings.setValue("password", self.ui.lineEdit_dbpass.text())
        settings.endGroup()

        self.accept()

    def dataChanged(self):
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
