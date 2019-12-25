from PyQt5.QtWidgets import (QMainWindow)
from PyQt5.uic import loadUi


class MainWindowView(QMainWindow):
    def __init__(self):
        super(MainWindowView, self).__init__()
        self.ui = loadUi("ui/main_window.ui", self)

        self.show()
