import bpy
from ...图标 import 加载图标
图标预览 = 加载图标()

class XiaoerUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "小二主页"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_1"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        layout = self.layout

        # 添加按钮
        行 = layout.row(align=True)
        行.operator(
            "xiaoer.open_website_bilibili",  # 操作符 ID
            icon_value=图标预览["小二"].icon_id,   # 按钮图标
            emboss=False  # 隐藏按钮背景
        )
        左侧 = 行.split(factor=0.08, align=True)
        右端 = 左侧.column(align=True)
        右端.label(icon='FUND')