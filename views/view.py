from PyQt5.QtCore import QObject


class View(QObject):
    def __init__(self):
        super(View, self).__init__()

    def setMainWidget(self, widget):
        self.m_widget = widget

    def mainWidget(self):
        return self.m_widget
