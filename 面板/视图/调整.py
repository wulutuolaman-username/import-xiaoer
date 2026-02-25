import bpy  # noqa: F401
from ...指针 import *

class MaterialListUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "调整材质"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_snowbreak_7"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    @classmethod
    def poll(cls, context):
        模型 = context.active_object  # type:小二物体|bpy.types.Object
        if 模型 and 模型.判断类型.物体.是网格:
            材质 = 模型.active_material
            if 材质:
                return 模型.小二预设模板.使用插件
        return False

    def draw(self, context):
        布局 = self.layout
        模型 = context.active_object  # type:小二物体|bpy.types.Object
        if 模型.判断类型.物体.是网格:
            # 骨架 = 模型.parent  # type:小二物体|bpy.types.Object
            # if 骨架.判断类型.物体.是骨架:
                行 = 布局.row()
                行.label(text=模型.name.replace("_mesh", ""), icon='MESH_DATA')
                行 = 布局.row()
                行.prop(context.space_data.overlay, "show_bones", text="显示骨骼", icon='ARMATURE_DATA')  # type:ignore
                行.prop(context.space_data.overlay, "show_extras", text="显示其他项", icon='EMPTY_DATA')  # type:ignore
                行 = 布局.row()
                行.template_list(
                    "MATERIAL_UL_matslots",
                    "",
                    模型,
                    "material_slots",
                    模型,
                    "active_material_index"
                    # rows=6
                )
                行 = 布局.row()
                行.operator("object.material_slot_select")
                行.operator("object.material_slot_deselect")
                材质 = 模型.active_material  # type:小二材质|bpy.types.Material
                if 材质:
                    列 = 布局.column()
                    列.prop(材质, "use_backface_culling", toggle=1)
                    列.prop(材质, "blend_method")
                    if 材质.blend_method == 'BLEND':
                        列.prop(材质, "show_transparent_back", toggle=1)
                    属性 = 材质.小二预设模板
                    if 属性.使用插件:
                        if 属性.材质分类+'材质' != 属性.初始分类:
                            列.prop(属性, '代码分类')
                        列.prop(属性, '材质分类')
                        if 属性.使用检测透明材质:
                            列.prop(属性, '检测为透明材质')
                        列.prop(属性, '透明材质', toggle=1)
