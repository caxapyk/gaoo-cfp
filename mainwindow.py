from PyQt5.Qt import Qt
from PyQt5.QtCore import (QCoreApplication, QSettings, QModelIndex)
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QWidget, QToolBar, QStatusBar, QAction,
                             QSizePolicy, QMenuBar, QSplitter, QTreeView, QHBoxLayout,QPushButton, QLineEdit)
from PyQt5.QtGui import (QIcon, QPixmap, QKeySequence)
from PyQt5.uic import loadUi

from dialogs import (DoctypeDialog, DocflagDialog, DbSettingsDialog)
from views import (GEOView, DocView)
from models import ChurchModel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('Межфондовый указатель к документам духовного '
                            'ведомства периода до октября 1917 года (ГАОО)')

        self.settings = QSettings()

        # if (self.settings):

        self.restoreSession()
        self.initUi()

    def restoreSession(self):
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value('geometry', None))
        else:
            self.resize(900, 600)

    def initUi(self):
        # load views
        doc_view = DocView(self)
        geo_view = GEOView(self, doc_view)

        # menubar
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu("Файл")
        create_menu = file_menu.addMenu("Создать")
        create_menu.addAction(doc_view.vAction("doc_create"))
        file_menu.addSeparator()
        exit_action = file_menu.addAction(
            QIcon(":/icons/exit-16.png"), "Выход")
        exit_action.setShortcut(QKeySequence.Close)
        exit_action.triggered.connect(self.close)

        edit_menu = menubar.addMenu("Правка")
        edit_menu.addAction(doc_view.vAction("doc_update"))
        edit_menu.addAction(doc_view.vAction("doc_remove"))

        cat_menu = menubar.addMenu("Cправочники")
        doctype_action = cat_menu.addAction(
            QIcon(":/icons/doctype-16.png"), "Типы документов")
        doctype_action.triggered.connect(self.openDoctypeDialog)

        docflag_action = cat_menu.addAction(
            QIcon(":/icons/flag-16.png"), "Флаги")
        docflag_action.triggered.connect(self.openDocflagDialog)

        settings_menu = menubar.addMenu("Сервис")
        dbsettings_action = settings_menu.addAction(
            QIcon(":/icons/dbsettings-16.png"), "Настройка подключения")
        dbsettings_action.triggered.connect(self.openDbSettingsDialog)

        help_menu = menubar.addMenu("Справка")
        about_action = help_menu.addAction(
            QIcon(":/icons/info-16.png"), "О программе")
        help_menu.addSeparator()
        about_action.triggered.connect(self.aboutCFP)

        aboutqt_action = help_menu.addAction("O Qt")
        aboutqt_action.triggered.connect(self.aboutQt5)

        self.setMenuBar(menubar)

        # toolbar
        toolbar = QToolBar(self)

        toolbar.addAction(doc_view.vAction("doc_create"))
        toolbar.addAction(doc_view.vAction("doc_update"))
        toolbar.addAction(doc_view.vAction("doc_remove"))

        # filter panel
        toolbar.addWidget(doc_view.vToolBarWidget("doc_filter"))

        self.addToolBar(toolbar)

        # statusbar
        statusbar = QStatusBar(self)
        statusbar.showMessage("Готово")

        self.setStatusBar(statusbar)

        # main widget
        splitter = QSplitter(self)
        splitter.addWidget(geo_view.mainWidget())
        splitter.addWidget(doc_view.mainWidget())

        self.geo_view = geo_view
        self.doc_view = doc_view

        self.setCentralWidget(splitter)

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
