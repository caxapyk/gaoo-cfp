from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import (QSettings)
from PyQt5.QtSql import QSqlDatabase


class DbSettingsDialog(QDialog):
    def __init__(self):
        super(DbSettingsDialog, self).__init__()
        ui = loadUi("ui/dbsettings_dialog.ui", self)
        ui.setWindowIcon(QIcon(":/icons/church-16.png"))

        ui.pushButton_test.clicked.connect(self.testAction)
        ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)

        ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(
            self.accept)

        self.ui = ui

        self.show()

    def testAction(self):
        db = QSqlDatabase().addDatabase("QMYSQL")

        db.setHostName(self.ui.lineEdit_server.text())
        db.setDatabaseName(self.ui.lineEdit_db.text())
        db.setUserName(self.ui.lineEdit_user.text())
        db.setPassword(self.ui.lineEdit_dbpass.text())

        label = self.ui.label_status
        if db.open():
            label.setStyleSheet("color: green")
            label.setText("Подключение успешно!")

            self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(False)
            self.ui.buttonBox.button(
                QDialogButtonBox.Save).clicked.connect(self.saveAction)
        else:
            label.setStyleSheet("color: red")
            label.setText("Подключение не выполнено!")

    def saveAction(self):
        settings = QSettings()
        settings.beginGroup("Database")
        settings.setValue("server", self.ui.lineEdit_server.text())
        settings.setValue("db", self.ui.lineEdit_db.text())
        settings.setValue("user", self.ui.lineEdit_user.text())
        settings.setValue("password", self.ui.lineEdit_dbpass.text())
        settings.endGroup()

        self.ui.label_status.setText("")
        self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)
