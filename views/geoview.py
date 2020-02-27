from PyQt5.QtCore import (QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QSizePolicy, QFrame, QVBoxLayout)
from models import (GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SqlTreeModel)
from views import View
from .treebaseview import TreeBaseView


class GeoView(View):
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

        self.tree_view = TreeBaseView(parent)
        # set model to tree_view
        self.tree_view.setModel(self.model)

        v_layout.addWidget(self.tree_view.mainWidget())

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)

        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMinimumSize(QSize(250, 0))

        # set main ad default widget
        self.setMainWidget(self.main_widget)
