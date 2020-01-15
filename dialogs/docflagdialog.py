from PyQt5.QtSql import QSqlTableModel
from .listviewdialog import ListViewDialog


class DocflagDialog(ListViewDialog):
    def __init__(self):
        super(DocflagDialog, self).__init__()

        self.setWindowTitle("Справочник - Дополнительные сведения (флаги)")

        model = QSqlTableModel()
        model.setTable("cfp_docflag")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.setModel(model)