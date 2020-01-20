from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QObject
from .listviewdialog import ListViewDialog


class DocflagDialog(QObject):
    def __init__(self):
        super(DocflagDialog, self).__init__()

        model = QSqlTableModel()
        model.setTable("cfp_docflag")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()

        listviewdialog = ListViewDialog(model)
        listviewdialog.setWindowTitle(
            "Справочник - Дополнительные сведения (флаги)")
        listviewdialog.show()

        #self.setModel(model, 1, 2)
