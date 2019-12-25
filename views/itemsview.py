from PyQt5.Qt import Qt
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from PyQt5.QtWidgets import (QWidget)
from PyQt5.uic import loadUi
from models import CFPModel


class ItemsView(QWidget):

    def __init__(self):
        super(GEOView, self).__init__()
        self.ui = loadUi("ui/main_window.ui", self)

        self.model = CFPModel()

        self.ui.tableView_cfp.setModel(model.select())

        self.show()