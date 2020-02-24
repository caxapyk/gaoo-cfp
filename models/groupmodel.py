from models import SqlTreeBaseModel


class GroupModel(SqlTreeBaseModel):
    def __init__(self):
        super(GroupModel, self).__init__()
        self.setParentId("NULL")
        self.setTable("cfp_group")
        self.setForeignKey('parent')
        self.setNewItemName("Новый раздел")
        self.setIconResource(":/icons/folder-16.png")
