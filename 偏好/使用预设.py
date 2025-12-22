import bpy

class XiaoerAddonImortSettings:

    自动查找预设: bpy.props.BoolProperty(
        name="自动查找预设",
        description="先在偏好设置中设置包含所有预设文件的目录，启用自动查找预设文件",
        default=True
    )

    查找预设深度检索: bpy.props.BoolProperty(
        name="深度检索",
        description="进一步增强查找预设，增加查找时间",
        default=True
    )

    预设目录: bpy.props.StringProperty(
        name="预设目录",
        description="设置预设文件的搜索根目录",
        # subtype='DIR_PATH'
    )

    def 设置目录(self, 布局):
        行 = 布局.row(align=True)
        行.prop(self, "预设目录", text="预设目录", icon='FILE_FOLDER')
        行.scale_x = 0.5
        键 = 行.operator("xiaoer.set_user_path", text="选择预设目录", icon='FILE_FOLDER')
        键.属性 = "预设目录"  # 将路径属性名传递给操作符