from PyQt5.QtSql import QSqlTableModel
from .listviewdialog import ListViewDialog
from models import (DocflagModel, SqlListProxyModel)


class DocflagDialog(ListViewDialog):
    def __init__(self):
        super(DocflagDialog, self).__init__()
        self.setWindowTitle(
            "Справочник - Флаги")

        model = DocflagModel()
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()

        list_model = SqlListProxyModel(2)
        list_model.setSourceModel(model)

        self.setModel(list_model)
