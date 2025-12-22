import bpy
from typing import cast
from ...指针 import XiaoerObject, XiaoerMaterial

class MaterialPanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_import_xiaoer_material_1'
    bl_label = '小二预设材质'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    @classmethod
    def poll(cls, context):
        材质 = cast(XiaoerMaterial, context.material)
        return 材质 and 材质.小二预设材质.使用插件

    def draw(self, context):
        布局 = self.layout
        材质 = cast(XiaoerMaterial, context.material)

        属性 = 材质.小二预设材质

        列 = 布局.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        列.prop(属性, '文件')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')

class TemplateMaterialPanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_import_xiaoer_material_2'
    bl_label = '小二预设模板'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    @classmethod
    def poll(cls, context):
        材质 = cast(XiaoerMaterial, context.material)
        return 材质 and 材质.小二预设模板.使用插件

    def draw(self, context):
        布局 = self.layout
        模型 = cast(XiaoerObject, context.active_object)
        材质 = cast(XiaoerMaterial, context.material)

        属性 = 材质.小二预设模板

        列 = 布局.column()
        列.enabled = not 模型.小二预设模板.加载完成
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        if 模型.小二预设模板.加载完成:
            列.label(text="在模型的物体属性模板",icon='OBJECT_DATA')
            列.label(text="取消加载完成状态",icon='CHECKBOX_HLT')
            列.label(text="可修改材质分类、透明状态",icon='MATERIAL')
            列.label(text="第一次加载时，模板文件必须包含全部节点组",icon='ERROR')
            列.label(text="如果导入贴图，第一次加载时，贴图路径必须包含全部贴图", icon='ERROR')
            列.label(text="不要修改贴图、节点和节点组名称",icon='ERROR')
        if 属性.材质分类+'材质' != 属性.初始分类:
            列.prop(属性, '代码分类')
        列.prop(属性, '材质分类')
        if 属性.使用检测透明材质:
            列.prop(属性, '检测为透明材质')
        列.prop(属性, '透明材质')
        列.prop(属性, '文件')
        列.prop(属性, '贴图')
        列.prop(属性, '游戏')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')