from bpy.props import BoolProperty

class RenameAssets:
    重命名资产: BoolProperty(
        name="重命名资产",
        description="建议在连续导入时开启,开启后可以对材质、节点组、贴图、驱动物体等对象的名称添加角色名重命名,以防止混淆，并放在单独的集合",
        default=False
    )

    独立集合: BoolProperty(
        name="集合",
        description="",
        default=True
    )  # 1.0.4新增

    重命名材质: BoolProperty(
        name="材质",
        description="",
        default=True
    )  # 1.0.4新增

    重命名贴图: BoolProperty(
        name="贴图",
        description="",
        default=True
    )  # 1.0.4新增

    重命名动作: BoolProperty(
        name="动作",
        description="",
        default=True
    )  # 1.0.4新增

    重命名节点组: BoolProperty(
        name="节点组",
        description="",
        default=True
    )  # 1.0.4新增

    重命名形态键: BoolProperty(
        name="形态键",
        description="",
        default=True
    )  # 1.0.4新增

    重命名驱动物体: BoolProperty(
        name="驱动物体",
        description="",
        default=True
    )  # 1.0.4新增

    重命名刚体和关节: BoolProperty(
        name="刚体和关节",
        description="",
        default=True
    )  # 1.0.4新增

    def 重命名可选项(self,layout):
        列 = layout.column(align=True)  # 1.0.4新增
        行 = 列.row(align=True)
        分割 = 行.split(factor=0.3)
        左侧 = 分割.column()  # 分割行，左侧占30%宽度
        左侧.prop(self, "重命名资产", text="重命名资产可选项： ", icon='ASSET_MANAGER')
        左侧.scale_y = 2
        右侧 = 分割.column()  # 右侧子行
        右侧.enabled = self.重命名资产
        右行 = 右侧.row(align=True)
        右行.prop(self, "独立集合", icon='OUTLINER_COLLECTION')
        右行.prop(self, "重命名材质", icon='MATERIAL')
        右行.prop(self, "重命名贴图", icon='IMAGE_DATA')
        右行.prop(self, "重命名节点组", icon='NODETREE')
        右行 = 右侧.row(align=True)
        右行.prop(self, "重命名动作", icon='ACTION')
        右行.prop(self, "重命名形态键", icon='SHAPEKEY_DATA')
        右行.prop(self, "重命名驱动物体", icon='OBJECT_DATA')
        右行.prop(self, "重命名刚体和关节", icon='RIGID_BODY')