from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget


class View(QObject):
    __m_widget__ = None
    __view_action__ = {}
    __t_widget__ = {}

    def __init__(self):
        super(View, self).__init__()

    def setMainWidget(self, widget):
        self.__m_widget__ = widget

    def mainWidget(self):
        if self.__m_widget__:
            return self.__m_widget__
        return QWidget()

    def addViewAction(self, name, action):
        self.__view_action__[name] = action

    def vAction(self, name):
        return self.__view_action__[name]

    def addToolBarWidget(self, name, widget):
        self.__t_widget__[name] = widget

    def vToolBarWidget(self, name):
        return self.__t_widget__[name]
