import bpy
from ...偏好.获取偏好 import 获取偏好
from ...指针 import *

class UVPanel(bpy.types.Panel):
    bl_idname = 'UV_PT_import_xiaoer_UV'
    bl_label = '检查透明材质'
    bl_space_type = 'IMAGE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = '导入小二'        # 侧边栏分类标签

    def draw(self, context):
        偏好 = 获取偏好()
        布局 = self.layout
        模型 = context.active_object  # type:小二物体|bpy.types.Object
        if 模型.判断类型.物体.是网格:
            行 = 布局.row()
            行.label(text=模型.name, icon='MESH_DATA')
            行 = 布局.row()
            # 行.prop(模型, 'material_slots')
            行.template_list(
                "MATERIAL_UL_matslots",  # 内置的材质槽UI列表类型
                "",  # 标识符
                模型, "material_slots",  # 数据路径
                模型, "active_material_index",  # 活动索引路径
                # rows=4  # 显示行数
            )
        # if context.mode == 'EDIT_MESH':
        行 = 布局.row()
        行.operator("object.material_slot_select")
        行.operator("object.material_slot_deselect")
        if 模型.判断类型.物体.是网格:
            材质 = 模型.active_material  # type:小二材质|bpy.types.Material
            if 材质:
                行 = 布局.row(align=True)
                列 = 行.column()
                列.ui_units_x = 6  # 设置固定宽度单位
                列.enabled = 偏好.检测透明材质
                列.prop_enum(偏好, "检测方式", '射线')  # 1.1.2
                列.prop_enum(偏好, "检测方式", '面积')  # 1.1.2
                列 = 行.column()
                列.scale_y = 2.0  # 让这一行更宽
                列.prop(偏好, "检测透明材质", text="检测透明材质", icon='MATERIAL')  # 1.1.0

                列 = 布局.column()
                列.prop(材质, "use_backface_culling")
                列.prop(材质, "blend_method")
                if 材质.blend_method == 'BLEND':
                    列.prop(材质, "show_transparent_back")
                属性 = 材质.小二预设模板
                if 属性.使用插件:
                    if 属性.材质分类+'材质' != 属性.初始分类:
                        列.prop(属性, '代码分类')
                    列.prop(属性, '材质分类')
                    if 属性.使用检测透明材质:
                        列.prop(属性, '检测为透明材质')
                    列.prop(属性, '透明材质')