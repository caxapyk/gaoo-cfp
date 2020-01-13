from PyQt5.QtCore import QObject


class View(QObject):

    __main_widget__ = None

    def __init__(self):
        super(View, self).__init__()

    def setMainWidget(self, widget):
        self.__main_widget__ = widget

    def mainWidget(self):
        return self.__main_widget__
