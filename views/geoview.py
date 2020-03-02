from PyQt5.QtCore import (QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QSizePolicy, QFrame, QVBoxLayout)
from models import (GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SqlTreeModel)
from views import TreeBaseView
from widgets import TreeSortFilter


class GeoView(TreeBaseView):
    def __init__(self, parent):
        super(GeoView, self).__init__(parent)

        self.parent = parent
        self.docview = self.parent.doc_view

        # set models
        gubernia = GuberniaModel()
        uezd = UezdModel()
        locality = LocalityModel()
        church = ChurchModel()

        geo_model = SqlTreeModel(
            (gubernia, uezd, locality, church),
            ("Территория",))
        geo_model.setModelColumn(0, 1)
        geo_model.setModelColumn(1, 2)
        geo_model.setModelColumn(2, 2)
        geo_model.setModelColumn(3, 2)

        geo_model.select()

        self.model = QSortFilterProxyModel()
        self.model.setFilterKeyColumn(0)
        self.model.setSourceModel(geo_model)
        # disable auto filtering
        self.model.setDynamicSortFilter(False)

        self.main_widget = QFrame()
        v_layout = QVBoxLayout(self.main_widget)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        # set model to tree_view
        self.tree_view.setModel(self.model)
        self.tree_view.doubleClicked.connect(self.loadDocs)

        # tree filter
        self.tree_filter = TreeSortFilter(self)
        self.tree_filter.setMode(TreeSortFilter.SortFilterMode)

        v_layout.addWidget(self.tree_filter)
        v_layout.addWidget(self.tree_view)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)

        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMinimumSize(QSize(250, 0))

        # set main ad default widget
        self.setMainWidget(self.main_widget)

    def loadDocs(self, index):
        if self.isEndPointReached(index):
            index = self.model.mapToSource(index)
            sql_model = index.internalPointer()

            self.docview.loadData(sql_model.uid())

    def isEndPointReached(self, index):
        if index.isValid():
            # reach endpoint if item class is ChurchModel
            source_index = self.model.mapToSource(index)
            item_model = source_index.internalPointer().model()

            if isinstance(item_model, ChurchModel):
                return True
        return False

    def showContextMenu(self, point):
        index = self.tree_view.indexAt(point)

        default_name = ""
        if index.isValid():
            if not self.isEndPointReached(index):
                source_index = self.model.mapToSource(index)
                level = source_index.internalPointer().level()
                model = self.model.sourceModel().models()[level + 1]
                default_name = model.displayName()
        else:
            model = self.model.sourceModel().models()[0]
            default_name = model.displayName()

        self.setDefaultItemName(default_name)

        if self.isEndPointReached(index):
            action_doc_open = self.context_menu.addAction(
                "Документы")
            action_doc_open.triggered.connect(lambda: self.loadDocs(index))

            self.context_menu.addSeparator()

        super().showContextMenu(point)
