from .listviewdialog import ListViewDialog
from models import (DocflagModel, DefaultItemProxyModel)


class DocflagDialog(ListViewDialog):
    def __init__(self, parent):
        super(DocflagDialog, self).__init__(parent)
        self.setWindowTitle(
            "Справочник [Метки документов (примечания)]")

        model = DocflagModel()
        model.setEditStrategy(DocflagDialog.OnFieldChange)
        model.select()

        list_model = DefaultItemProxyModel(2)
        list_model.setSourceModel(model)

        self.setModel(list_model)
