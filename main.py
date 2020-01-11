from PyQt5.Qt import Qt
from PyQt5.QtCore import (QCoreApplication, QSettings)
from PyQt5.QtWidgets import (QMainWindow, QMessageBox)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from dialogs import (DoctypeDialog, DocflagDialog)
from views.geoview import GEOView


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = loadUi("ui/main_window.ui", self)
        self.ui.setWindowIcon(QIcon(":/icons/church-16.png"))

        QCoreApplication.setOrganizationName("GAOO")
        QCoreApplication.setApplicationName("cfp")

        self.settings = QSettings()

        # restore geometry
        geometry = self.settings.value('geometry', None)
        if geometry:
            self.restoreGeometry(geometry)

        self.ui.action_doctype.triggered.connect(DoctypeDialog)
        self.ui.action_docflag.triggered.connect(DocflagDialog)

        self.ui.action_about.triggered.connect(self.aboutCFP)
        self.ui.action_aboutqt.triggered.connect(self.aboutQt5)

        geoview = GEOView(self)

    def aboutCFP(self):
        text = "<b>Межфондовый указатель к документам духовного ведомства периода \
до октября 1917 года</b><br/><br/>\
Государственный архив Орловской области, 2019-2020<br/><br/>\
Cахарук Александр [<a href=\"mailto:saharuk.alexander@gmail.com\">\
saharuk.alexander@gmail.com</a>]<br/><br/>\
Данное программное обеспечение распространяется по лицензии GPLv3:<br/>\
<a href=\"https://www.gnu.org/licenses/gpl-3.0\">\
https://www.gnu.org/licenses/gpl-3.0</a><br/><br/>\
<span style=\"color:#999\">Иконки приложения: \
<a href=\"https://icons8.com\" style=\"color:#999;font-size:8;\">\
https://icons8.com</a></span>"

        about_box = QMessageBox()
        about_box.setWindowIcon(self.windowIcon())
        about_box.setIconPixmap(QPixmap(":/icons/church-48.png"))

        about_box.setWindowTitle("О программе")
        about_box.setTextFormat(Qt.RichText)
        about_box.setText(text)

        about_box.exec()

    def aboutQt5(self):
        return QMessageBox.aboutQt(self)

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)

        super(MainWindow, self).closeEvent(event)
