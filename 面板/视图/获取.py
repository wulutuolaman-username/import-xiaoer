import bpy
from ...图标 import 图标预览
# 图标预览 = 加载图标()

class GetMatPresetsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "获取预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_5"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        行 = self.layout.row()
        列 = 行.column(align=True)
        列.operator(
            "xiaoer.open_website_afdian",  # 操作符 ID
            text="爱发电",
            icon_value=图标预览["爱发电"]  # type: ignore
        )
        列 = 行.column(align=True)
        列.operator(
            "xiaoer.open_website_aplaybox",  # 操作符 ID
            text="模之屋",
            icon_value=图标预览["模之屋"]  # type: ignore
        )