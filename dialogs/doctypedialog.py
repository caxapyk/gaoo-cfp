from PyQt5.QtSql import QSqlTableModel
from .listviewdialog import ListViewDialog
from models import SqlListModel


class DoctypeDialog(ListViewDialog):
    def __init__(self):
        super(DoctypeDialog, self).__init__()

        self.setWindowTitle("Справочник - Виды документов")

        model = SqlListModel()
        model.setTable("cfp_doctype")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.setModel(model)
