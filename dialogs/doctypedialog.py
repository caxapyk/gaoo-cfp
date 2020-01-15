from PyQt5.QtSql import QSqlTableModel
from .listviewdialog import ListViewDialog


class DoctypeDialog(ListViewDialog):
    def __init__(self):
        super(DoctypeDialog, self).__init__()

        self.setWindowTitle("Справочник - Виды документов")

        model = QSqlTableModel()
        model.setTable("cfp_doctype")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.setModel(model)
