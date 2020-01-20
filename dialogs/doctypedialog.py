from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QObject
from .listviewdialog import ListViewDialog


class DoctypeDialog(QObject):
    def __init__(self):
        super(DoctypeDialog, self).__init__()

        model = QSqlTableModel()
        model.setTable("cfp_doctype")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()

        listviewdialog = ListViewDialog(model)
        listviewdialog.setWindowTitle("Справочник - Виды документов")
        listviewdialog.show()

        #self.setModel(model, 1, 2)
