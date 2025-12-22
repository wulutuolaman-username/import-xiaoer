import bpy
from ...操作.模块.安装模块 import 检查轮子存在

class InformationFeedbackUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "信息反馈"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_2"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        布局 = self.layout

        # 添加按钮
        行 = 布局.row()
        模块 = True
        try:
            import numpy
            行.label(text=f"numpy {numpy.__version__}")
        except:
            模块 = False
            行.label(text="numpy模块异常", icon='ERROR')

        行 = 布局.row()
        try:
            import PIL
            行.label(text=f"PIL {PIL.__version__}")
        except:
            模块 = False
            行.alert = True
            行.label(text="PIL模块未安装", icon='ERROR')

        行 = 布局.row()
        try:
            import imagehash
            行.label(text=f"imagehash {imagehash.__version__}")
        except:
            模块 = False
            行.alert = True
            行.label(text="imagehash模块未安装", icon='ERROR')

        行 = 布局.row()
        if 模块:
            行.label(text="模块已安装成功", icon='CHECKBOX_HLT')
        else:
            行.alert = True
            行.label(text="模块导入失败", icon='ERROR')

        if 检查轮子存在():
            行 = 布局.row()
            列 = 行.column()
            列.operator("import_xiaoer.install_packages", icon='IMPORT')
            列 = 行.column()
            列.operator("import_xiaoer.uninstall_packages", icon='TRASH')

        行 = 布局.row()
        行.scale_y = 2
        行.operator("screen.info_log_show", text="信息面板", icon='INFO')
        行 = 布局.row()
        行.operator(
            "wm.url_open",
            text="提交错误信息",
            icon='URL'
        ).url = "https://github.com/wulutuolaman-username/import-xiaoer/issues"
        行 = 布局.row(align=True)
        列 = 行.column()
        列.ui_units_x = 15  # 设置固定宽度单位
        列.label(text="联系插件作者")
        列 = 行.column()
        列.operator("wulutuolaman.open_website_tiktok",text="抖音")
        列 = 行.column()
        列.operator("wulutuolaman.open_website_bilibili",text="B站")