from models import SqlTreeBaseModel


class GroupModel(SqlTreeBaseModel):

    TypeFolder = 0
    TypeGroup = 1

    def __init__(self):
        super(GroupModel, self).__init__()
        self.setParentId("NULL")
        self.setTable("cfp_group")
        self.setForeignKey('parent')
        self.setDisplayName("группировку")
        self.setNewItemName("Новая группировка")
        self.setTypeIconResource(self.TypeFolder,":/icons/folder-16.png")
        self.setTypeIconResource(self.TypeGroup,":/icons/church-16.png")

        self.setTypeColumn(3)
