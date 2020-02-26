from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QHBoxLayout, QPushButton, QLineEdit, QButtonGroup, QFrame)
from views import TreeBaseView


class TreeSortFilter(QFrame):

    # Display only filter widgets
    FilterMode = 0
    # Display sort and filter widgets
    SortFilterMode = 1

    def __init__(self, parent):
        super(TreeSortFilter, self).__init__()

        self.treeview = None

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)
        self.layout.setSpacing(0)

        self.filterUi()

    def setMode(self, mode=0):
        if mode == self.SortFilterMode:
            self.sortUi()

    def filterUi(self):
        self.geofilter_lineedit = QLineEdit(self)
        self.geofilter_lineedit.textChanged.connect(self.doFilter)

        self.clearfilter_btn = QPushButton(self)
        self.clearfilter_btn.setIcon(QIcon(":/icons/clear-filter-16.png"))
        self.clearfilter_btn.setToolTip("Очистить фильтр")
        self.clearfilter_btn.setDisabled(True)
        self.clearfilter_btn.setFlat(True)
        self.clearfilter_btn.clicked.connect(self.clearFilter)

        self.layout.addWidget(self.geofilter_lineedit)
        self.layout.addWidget(self.clearfilter_btn)

    def sortUi(self):
        self.sort_group = QButtonGroup(self)

        sort_buttons = (
            (":/icons/sort-az-16.png", "Cортировка по возрастанию"),
            (":/icons/sort-za-16.png", "Cортировка по убыванию"),
        )
        for i, button in enumerate(sort_buttons):
            sort_btn = QPushButton(self)
            sort_btn.setIcon(QIcon(button[0]))
            sort_btn.setToolTip(button[1])
            sort_btn.setCheckable(True)
            sort_btn.setFlat(True)

            self.sort_group.addButton(sort_btn, i)
            self.layout.addWidget(sort_btn)

        self.sort_group.buttonClicked[int].connect(self.sort)

    def setWidget(self, widget):
        if isinstance(widget, TreeBaseView):
            self.treeview = widget

            self.treeview.treeSorted.connect(self.externalSorted)
            self.treeview.treeFilterCleared.connect(self.clearFilter)
            self.treeview.treeSortCleared.connect(self.clearSort)
        else:
            print("Error! Widget must be instance of TreeBaseView Class")

    def setFilterPlaceHolder(self, text):
        self.geofilter_lineedit.setPlaceholderText(text)

    def doFilter(self, text):
        self.clearfilter_btn.setDisabled((len(text) == 0))
        for button in self.sort_group.buttons():
            button.setDisabled(True)

        self.treeview.filter(text)

    def clearFilter(self):
        if len(self.geofilter_lineedit.text()) > 0:
            self.geofilter_lineedit.setText("")
            self.clearfilter_btn.setDisabled(True)
            for button in self.sort_group.buttons():
                button.setDisabled(False)

            self.treeview.clearFilter()

    def sort(self, order):
        return self.treeview.sort(order)

    def externalSorted(self, order):
        if order < 2:
            self.sort_group.button(order).setChecked(True)

    def clearSort(self):
        if self.sort_group.checkedButton() is not None:
            self.sort_group.setExclusive(False)
            self.sort_group.checkedButton().setChecked(False)
            self.sort_group.setExclusive(True)
