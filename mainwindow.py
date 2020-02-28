from PyQt5.Qt import Qt
from PyQt5.QtCore import (QCoreApplication, QSettings, QModelIndex)
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QWidget, QToolBar, QStatusBar, QAction,
                             QSizePolicy, QMenuBar, QSplitter, QTreeView, QHBoxLayout, QPushButton, QLineEdit)
from PyQt5.QtGui import (QIcon, QPixmap, QKeySequence)
from PyQt5.uic import loadUi

from dialogs import (DoctypeDialog, DocflagDialog, FundDialog, DbSettingsDialog, DocSearchDialog)
from views import (GeoView, DocView)
from models import ChurchModel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('Межфондовый указатель к документам духовного '
                            'ведомства периода до октября 1917 года (ГАОО)')

        self.settings = QSettings()
        self.restoreSession()

        # load views
        self.doc_view = DocView(self)
        self.geo_view = GeoView(self)

        # global actions
        self.doc_search = QAction("Поиск документов")
        self.doc_search.setIcon(QIcon(":/icons/doc-search-16.png"))
        self.doc_search.setShortcut(Qt.Key_F3)
        self.doc_search.triggered.connect(self.openDocSearchDialog)

        self.doc_create = QAction("Новый документ")
        self.doc_create.setIcon(QIcon(":/icons/doc-new-16.png"))
        self.doc_create.setShortcut(QKeySequence.New)
        self.doc_create.setDisabled(True)
        self.doc_create.triggered.connect(self.doc_view.createDocDialog)

        self.doc_update = QAction("Редактировать")
        self.doc_update.setIcon(QIcon(":/icons/doc-edit-16.png"))
        self.doc_update.setDisabled(True)
        self.doc_update.triggered.connect(self.doc_view.editDocDialog)

        self.doc_remove = QAction("Удалить")
        self.doc_remove.setIcon(QIcon(":/icons/delete-16.png"))
        self.doc_remove.setDisabled(True)
        self.doc_remove.setShortcut(QKeySequence.Delete)
        self.doc_remove.triggered.connect(self.doc_view.removeDoc)

        self.doc_refresh = QAction("Обновить")
        self.doc_refresh.setIcon(QIcon(":/icons/refresh-16.png"))
        self.doc_refresh.setShortcut(QKeySequence.Refresh)
        self.doc_refresh.setDisabled(True)
        self.doc_refresh.triggered.connect(self.doc_view.refreshDocs)

        self.filter_panel = QWidget()
        self.filter_panel.setDisabled(True)
        f_layout = QHBoxLayout(self.filter_panel)
        f_layout.setContentsMargins(0, 0, 0, 0)
        f_layout.setAlignment(Qt.AlignRight)

        self.filter_lineedit = QLineEdit(self.filter_panel)
        self.filter_lineedit.setPlaceholderText("Фильтр по единице хранения...")
        self.filter_lineedit.setMaximumWidth(300)
        self.filter_lineedit.textChanged.connect(self.doc_view.filter)

        self.clearfilter_btn = QPushButton(self.filter_panel)
        self.clearfilter_btn.setIcon(QIcon(":/icons/clear-filter-16.png"))
        self.clearfilter_btn.setToolTip("Сбросить фильтр")
        self.clearfilter_btn.setMaximumWidth(30)
        self.clearfilter_btn.setDisabled(True)
        self.clearfilter_btn.clicked.connect(self.doc_view.clearFilter)

        f_layout.addWidget(self.filter_lineedit)
        f_layout.addWidget(self.clearfilter_btn)

        # setup
        self.setupMenu()
        self.toolbar = self.setupToolBar()
        self.statusbar = self.setupStatusBar()

        # main widget
        splitter = QSplitter(self)
        splitter.addWidget(self.geo_view.mainWidget())
        splitter.addWidget(self.doc_view.mainWidget())

        self.setCentralWidget(splitter)
        self.statusBar().showMessage("Готово", 2000)

    def setupMenu(self):
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu("Файл")
        create_menu = file_menu.addMenu("Создать")
        create_menu.addAction(self.doc_create)
        file_menu.addSeparator()
        exit_action = file_menu.addAction(
            QIcon(":/icons/exit-16.png"), "Выход")
        exit_action.setShortcut(QKeySequence.Close)
        exit_action.triggered.connect(self.close)

        edit_menu = menubar.addMenu("Правка")
        edit_menu.addAction(self.doc_search)
        edit_menu.addSeparator()
        edit_menu.addAction(self.doc_update)
        edit_menu.addAction(self.doc_remove)
        edit_menu.addSeparator()
        edit_menu.addAction(self.doc_refresh)

        cat_menu = menubar.addMenu("Cправочники")
        
        fund_action = cat_menu.addAction("Фонды")
        fund_action.triggered.connect(self.openFundDialog)

        cat_menu.addSeparator()

        doctype_action = cat_menu.addAction(
            QIcon(":/icons/doctype-16.png"), "Виды документов")
        doctype_action.triggered.connect(self.openDoctypeDialog)

        docflag_action = cat_menu.addAction(
            QIcon(":/icons/tag-16.png"), "Метки документов (примечания)")
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

    def setupToolBar(self):
        toolbar = QToolBar(self)

        toolbar.addAction(self.doc_create)
        toolbar.addSeparator()
        toolbar.addAction(self.doc_update)
        toolbar.addAction(self.doc_remove)
        toolbar.addSeparator()
        toolbar.addAction(self.doc_search)
        toolbar.addAction(self.doc_refresh)

        toolbar.addWidget(self.filter_panel)

        self.addToolBar(toolbar)

        return toolbar

    def setupStatusBar(self):
        statusbar = QStatusBar(self)
        statusbar.showMessage("Готово")

        self.setStatusBar(statusbar)

        return statusbar

    def restoreSession(self):
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value('geometry', None))
        else:
            self.resize(900, 600)

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
        doctype_dialog = DoctypeDialog(self)
        doctype_dialog.show()

    def openDocflagDialog(self):
        docflag_dialog = DocflagDialog(self)
        docflag_dialog.show()

    def openFundDialog(self):
        fund_dialog = FundDialog(self)
        fund_dialog.show()

    def openDocSearchDialog(self):
        search_dialog = DocSearchDialog()
        search_dialog.show()

    def openDbSettingsDialog(self):
        dbsettings_dialog = DbSettingsDialog()
        dbsettings_dialog.show()

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)

        super(MainWindow, self).closeEvent(event)

    def statusBar(self):
        return self.statusbar

    def toolBar(self):
        return self.toolbar
