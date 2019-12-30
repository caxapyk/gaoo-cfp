from PyQt5.Qt import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QDialog)
from PyQt5.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate, QSqlRelationalTableModel, QSqlTableModel, QSqlQueryModel)

from PyQt5.uic import loadUi
from models import SQLDoctypeModel


class DocTypeDialog(QDialog):
    def __init__(self):
        super(DocTypeDialog, self).__init__()
        self.ui = loadUi("ui/doctype_dialog.ui", self)

        self.model = QSqlQueryModel()
        self.model.setQuery("SELECT * FROM cfp_uezd")

        # self.dt_model = SQLDoctypeModel(self.model)
        standart_m = QStandardItemModel(2, 1)

        #item = QStandardItem("Item 1")
        #item.setFlags(Qt.NoItemFlags)
        #item.setCheckState(Qt.Checked)
        #item2 = QStandardItem("Item 2")
        #item2.setCheckState(Qt.Unchecked)
        #item2.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        #standart_m.setItem(0, 0, item)
        #standart_m.setItem(1, 0, item2)

        model = QStandardItemModel()
        #parentItem = model.invisibleRootItem()
        for i in range(4):
            item0 = QStandardItem("item %d" % i)
            #parentItem.appendRow(item)
            while self.model.query().next():
            	val = self.model.query().value("name")
            	item = QStandardItem(val)
            	if val == "Орловский уезд":
            		item.setCheckState(Qt.Checked)
            	model.appendRow(item)
            #parentItem = item


        self.ui.listView_doctype.setModel(model)
        self.ui.listView_doctype.setModelColumn(2)

        self.show()
