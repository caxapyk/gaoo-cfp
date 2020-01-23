from PyQt5.QtWidgets import QItemDelegate


class StorageUnitDelegate(QItemDelegate):
    def __init__(self, model):
        super(StorageUnitDelegate, self).__init__()
