from .listviewdialog import ListViewDialog
from models import FundModel


class FundDialog(ListViewDialog):
    def __init__(self, parent):
        super(FundDialog, self).__init__(parent)
        self.setWindowTitle("Справочник [Фонды]")

        model = FundModel()
        model.setEditStrategy(FundModel.OnFieldChange)
        model.select()

        self.setModel(model)
