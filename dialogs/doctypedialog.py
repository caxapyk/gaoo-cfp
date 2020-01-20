from PyQt5.QtSql import QSqlTableModel
from .listviewdialog import ListViewDialog
from models import (DoctypeModel, SqlListProxyModel)


class DoctypeDialog(ListViewDialog):
    def __init__(self):
        super(DoctypeDialog, self).__init__()
        self.setWindowTitle("Справочник - Виды документов")

        model = DoctypeModel()
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()

        list_model = SqlListProxyModel(2)
        list_model.setSourceModel(model)

        self.setModel(list_model)
