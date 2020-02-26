from PyQt5.QtCore import (QObject)
from PyQt5.QtWidgets import QWidget


class View(QObject):
    __m_widget__ = None

    def __init__(self, parent):
        super(View, self).__init__(parent)

    def setMainWidget(self, widget):
        self.__m_widget__ = widget

    def mainWidget(self):
        if self.__m_widget__:
            return self.__m_widget__
        return QWidget()
