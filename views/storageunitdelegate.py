from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QItemDelegate, QLineEdit)


class StorageUnitDelegate(QItemDelegate):
    def __init__(self, model):
        super(StorageUnitDelegate, self).__init__()
        print("sdfsdf")