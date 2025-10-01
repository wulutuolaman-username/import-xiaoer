import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty

class XiaoerAddonImortSettings:

    自动查找预设: BoolProperty(
        name="自动查找预设",
        description="先在偏好设置中设置包含所有预设文件的目录，启用自动查找预设文件",
        default=True
    )

    查找预设深度检索: BoolProperty(
        name="深度检索",
        description="进一步增强查找预设，增加查找时间",
        default=True
    )

    预设目录: StringProperty(
        name="预设目录",
        description="设置预设文件的搜索根目录",
        # subtype='DIR_PATH'
    )

    默认姿态: BoolProperty(
        name="默认姿态",
        description="若当前模型是默认的姿态，开启则继承面部定位属性；关闭后可以精准定位，但是调整变换属性",
        default=True
    )

    def 设置目录(self, layout):
        行 = layout.row(align=True)
        行.prop(self, "预设目录", text="预设目录", icon='FILE_FOLDER')
        行.scale_x = 0.5
        键 = 行.operator("xiaoer.set_user_path", text="选择预设目录", icon='FILE_FOLDER')
        键.属性 = "预设目录"  # 将路径属性名传递给操作符