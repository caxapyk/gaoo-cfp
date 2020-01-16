from PyQt5.QtSql import QSqlTableModel
from .listviewdialog import ListViewDialog
from models import SqlListModel


class DocflagDialog(ListViewDialog):
    def __init__(self):
        super(DocflagDialog, self).__init__()

        self.setWindowTitle("Справочник - Дополнительные сведения (флаги)")

        model = SqlListModel()
        model.setTable("cfp_docflag")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.setModel(model)
