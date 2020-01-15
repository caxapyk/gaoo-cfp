from PyQt5.Qt import Qt
from PyQt5.QtCore import (QCoreApplication, QSettings)
from PyQt5.QtWidgets import (QMainWindow, QMessageBox)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QSizePolicy, QMenuBar, QSplitter, QTreeView)
from dialogs import (DoctypeDialog, DocflagDialog, DbSettingsDialog)
from views.geoview import GEOView


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('Межфондовый указатель к документам духовного'
                            'ведомства периода до октября 1917 года')

        self.settings = QSettings()

        # if (self.settings):

        self.restoreSession()
        self.setUi()

    def restoreSession(self):
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value('geometry', None))
        else:
            self.resize(900, 600)

    def setUi(self):
        # load views
        geo_view = GEOView(self)

        splitter = QSplitter(self)
        splitter.addWidget(geo_view.mainWidget())

        tree_view = QTreeView()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(85)
        tree_view.setSizePolicy(sizePolicy)

        splitter.addWidget(tree_view)

        self.geo_view = geo_view

        self.setCentralWidget(splitter)

        self.setMenu()

    def setMenu(self):
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu("Файл")
        exit_action = file_menu.addAction(
            QIcon(":/icons/exit-16.png"), "Выход")

        cat_menu = menubar.addMenu("Cправочники")
        doctype_action = cat_menu.addAction("Виды документов")
        docflag_action = cat_menu.addAction("Доп. сведения (флаги)")

        help_menu = menubar.addMenu("Помощь")
        dbsettings_action = help_menu.addAction("Настройки соединения с БД")
        help_menu.addSeparator()
        about_action = help_menu.addAction("О программе")
        aboutqt_action = help_menu.addAction("O Qt")

        exit_action.triggered.connect(self.close)
        doctype_action.triggered.connect(self.openDoctypeDialog)
        docflag_action.triggered.connect(self.openDocflagDialog)
        dbsettings_action.triggered.connect(self.openDbSettingsDialog)
        about_action.triggered.connect(self.aboutCFP)
        aboutqt_action.triggered.connect(self.aboutQt5)

        self.setMenuBar(menubar)

    def aboutCFP(self):
        text = "<b>Межфондовый указатель к документам духовного ведомства периода \
        до октября 1917 года</b><br/><br/>\
        Государственный архив Орловской области, 2019-2020<br/><br/>\
        Cахарук Александр [<a href=\"mailto:saharuk.alexander@gmail.com\">\
        saharuk.alexander@gmail.com</a>]<br/><br/>\
        Данное программное обеспечение распространяется по лицензии GPLv3:\
        <br/><a href=\"https://www.gnu.org/licenses/gpl-3.0\">\
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

    def openDoctypeDialog(self):
        doctype_dialog = DoctypeDialog()
        doctype_dialog.show()

    def openDocflagDialog(self):
        docflag_dialog = DocflagDialog()
        docflag_dialog.show()

    def openDbSettingsDialog(self):
        dbsettings_dialog = DbSettingsDialog()
        dbsettings_dialog.show()

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)

        super(MainWindow, self).closeEvent(event)
