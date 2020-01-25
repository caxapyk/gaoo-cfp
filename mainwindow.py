from PyQt5.Qt import Qt
from PyQt5.QtCore import (QCoreApplication, QSettings)
from PyQt5.QtWidgets import (QMainWindow, QMessageBox)
from PyQt5.uic import loadUi
from PyQt5.QtGui import (QIcon, QPixmap, QKeySequence)
from PyQt5.QtWidgets import (QWidget, QToolBar, QStatusBar, QAction, QSizePolicy, QMenuBar, QSplitter, QTreeView, QHBoxLayout, QPushButton, QLineEdit)
from dialogs import (DoctypeDialog, DocflagDialog, DocFormDialog, DbSettingsDialog)
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
        geo_view = GEOView(self)
        geo_view.tree_view.doubleClicked.connect(self.showDocs)

        doc_view = DocView(self)
        doc_view.tree_view.pressed.connect(self.docSelected)

        # global actions

        action_create = QAction("Новый документ")
        action_create.setIcon(QIcon(":/icons/doc-new-20.png"))
        action_create.setDisabled(True)
        action_create.setShortcut(QKeySequence.New)
        action_create.triggered.connect(self.openDocFormDialogCreate)

        action_edit = QAction("Редактировать")
        action_edit.setIcon(QIcon(":/icons/doc-edit-20.png"))
        action_edit.setDisabled(True)
        action_edit.triggered.connect(self.openDocFormDialogEdit)

        action_delete = QAction("Удалить")
        action_delete.setIcon(QIcon(":/icons/delete-20.png"))
        action_delete.setDisabled(True)
        action_delete.setShortcut(QKeySequence.Delete)
        action_delete.triggered.connect(doc_view.deleteRow)

        # menubar
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu("Файл")
        create_menu = file_menu.addMenu("Создать")
        create_menu.addAction(action_create)
        file_menu.addSeparator()
        exit_action = file_menu.addAction(
            QIcon(":/icons/exit-16.png"), "Выход")
        exit_action.setShortcut(QKeySequence.Close)
        exit_action.triggered.connect(self.close)

        edit_menu = menubar.addMenu("Правка")
        edit_menu.addAction(action_edit)
        edit_menu.addAction(action_delete)

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

        toolbar.addAction(action_create)
        toolbar.addAction(action_edit)
        toolbar.addAction(action_delete)

        # filter panel
        filter_panel = QWidget(toolbar)
        f_layout = QHBoxLayout(filter_panel)
        f_layout.setContentsMargins(0, 0, 0, 0)
        f_layout.setAlignment(Qt.AlignRight)

        filter_line = QLineEdit(filter_panel)
        filter_line.setPlaceholderText("Фильтр по единице хранения...")
        filter_line.setMaximumWidth(300)
        filter_line.setDisabled(True)
        filter_line.textChanged.connect(doc_view.filter)

        clearfilter_btn = QPushButton(filter_panel)
        clearfilter_btn.setIcon(QIcon(":/icons/clear-filter-16.png"))
        clearfilter_btn.setToolTip("Сбросить фильтр")
        clearfilter_btn.setMaximumWidth(30)
        clearfilter_btn.setDisabled(True)
        clearfilter_btn.clicked.connect(doc_view.clearFilter)

        f_layout.addWidget(filter_line)
        f_layout.addWidget(clearfilter_btn)

        toolbar.addWidget(filter_panel)

        self.addToolBar(toolbar)

        # statusbar
        statusbar = QStatusBar(self)
        statusbar.showMessage("Готово")

        self.setStatusBar(statusbar)

        self.toolbar = toolbar
        self.action_create = action_create
        self.action_edit = action_edit
        self.action_delete = action_delete
        self.filter_line = filter_line
        self.clearfilter_btn = clearfilter_btn
        self.statusbar = statusbar

        # main widget
        splitter = QSplitter(self)
        splitter.addWidget(geo_view.mainWidget())
        splitter.addWidget(doc_view.mainWidget())

        self.geo_view = geo_view
        self.doc_view = doc_view

        self.setCentralWidget(splitter)

    def showDocs(self, index):
        index = self.geo_view.model.mapToSource(index)
        sql_model = index.internalPointer()

        if isinstance(sql_model.model(), ChurchModel):
            self.doc_view.loadData(index)

            self.action_create.setDisabled(False)
            self.action_edit.setDisabled(True)
            self.action_delete.setDisabled(True)
            self.filter_line.setDisabled(False)

    def docSelected(self):
        self.action_edit.setDisabled(False)
        self.action_delete.setDisabled(False)

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

    def openDocFormDialogEdit(self):
        if self.doc_view.tree_view.selectedIndexes():
            proxy_index = self.doc_view.tree_view.currentIndex()
            index = self.doc_view.model.mapToSource(proxy_index)
        else:
            index = QModelIndex()
        docform_dialog = DocFormDialog(index)
        docform_dialog.show()

    def openDocFormDialogCreate(self):
        docform_dialog = DocFormDialog()
        docform_dialog.show()

    def openDocFormDialogEdit(self):
        index = self.doc_view.currentIndex()
        docform_dialog = DocFormDialog(index)
        docform_dialog.show()

    def openDbSettingsDialog(self):
        dbsettings_dialog = DbSettingsDialog()
        dbsettings_dialog.show()

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)

        super(MainWindow, self).closeEvent(event)
