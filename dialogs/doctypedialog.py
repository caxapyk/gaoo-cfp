from PyQt5.QtSql import QSqlTableModel
from .listviewdialog import ListViewDialog
from models import (DoctypeModel, DefaultItemProxyModel)


class DoctypeDialog(ListViewDialog):
    def __init__(self):
        super(DoctypeDialog, self).__init__()
        self.setWindowTitle("Справочник - Типы документов")

        model = DoctypeModel()
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()

        list_model = DefaultItemProxyModel(2)
        list_model.setSourceModel(model)

        self.setModel(list_model)
