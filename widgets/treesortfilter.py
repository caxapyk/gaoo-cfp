from PyQt5.Qt import Qt, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QLineEdit, QButtonGroup, QFrame)


class TreeSortFilter(QFrame):

    # Display only filter widgets
    FilterMode = 0
    # Display sort and filter widgets
    SortFilterMode = 1

    def __init__(self):
        super(TreeSortFilter, self).__init__()

        self.__isFiltered__ = False
        self.__isSorted__ = False

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
            (":/icons/delete-16.png", "Сбросить сортировку"),
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
    	self.widget = widget

    def setFilterPlaceHolder(self, text):
    	self.geofilter_lineedit.setPlaceholderText(text)

    def doFilter(self, text):
        self.clearfilter_btn.setDisabled((len(text) == 0))

        self.widget.expandAll()

        self.widget.model().setRecursiveFilteringEnabled(True)
        self.widget.model().setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

        self.__isFiltered__ = True

    def isFiltered(self):
    	return self.__isFiltered__

    def clearFilter(self):
        if len(self.geofilter_lineedit.text()) > 0:
            self.geofilter_lineedit.setText("")
            self.clearfilter_btn.setDisabled(True)

            self.widget.model().invalidateFilter()

            self.__isFiltered__ = False

    def sort(self, order):
        if order == 0:
            sort_order = Qt.AscendingOrder
        elif order == 1:
        	sort_order = Qt.DescendingOrder
        else:
        	self.clearSort()
        	return

        self.widget.model().sort(0, sort_order)

        self.__isSorted__ = True

    def isSorted(self):
    	return self.__isSorted__

    def clearSort(self):
    	if self.isSorted():
	        self.sort_group.setExclusive(False)
	        self.sort_group.checkedButton().setChecked(False)
	        self.sort_group.setExclusive(True)

	        self.widget.model().sort(-1)

	        self.__isSorted__ = False

    def clearAllFilters(self):
        self.clearFilter()
        self.clearSort()





