import bpy
from ...指针 import *
from ...属性.物体 import *

class ModelObjectPanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_import_xiaoer_model_object_1'
    bl_label = '小二预设模型'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        物体 = context.active_object  # type:小二物体|bpy.types.Object
        return 物体 and 物体.小二预设模型.使用插件

    def draw(self, context):
        布局 = self.layout
        物体 = context.active_object  # type:小二物体|bpy.types.Object
        属性 = 物体.小二预设模型

        列 = 布局.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        if 物体.判断类型.物体.是网格:
            列.prop(属性, '导入完成')
        列.prop(属性, '文件')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')

class TemplateObjectPanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_import_xiaoer_model_object_2'
    bl_label = '小二预设模板'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        物体 = context.active_object  # type:小二物体|bpy.types.Object
        return 物体 and (物体.小二预设模板.使用插件 or 物体.小二预设模板.加载完成)

    def draw(self, context):
        布局 = self.layout
        物体 = context.active_object  # type:小二物体|bpy.types.Object
        属性 = 物体.小二预设模板

        列 = 布局.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        if 物体.判断类型.物体.是网格:
            列.prop(属性, '加载完成')
        列.prop(属性, '文件')
        列.prop(属性, '贴图')
        列.prop(属性, '游戏')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')
        if 物体.判断类型.物体.是网格:
            列.prop(属性, '显示导入节点组')
        if 属性.显示导入节点组:
            for 群组 in 属性.导入节点组:  # type:XiaoerAddonNodeTree
                列.prop(群组, '节点组', text='')
        if 属性.完成导入贴图:
            列.prop(属性, '显示导入贴图')
            if 属性.显示导入贴图:
                列.prop(属性, '显示基础贴图')
                if 属性.显示基础贴图:
                    for 图像 in 属性.基础贴图:  # type:XiaoerAddonImage
                        列.prop(图像, '贴图', text='')
                else:
                    for 图像 in 属性.导入贴图:  # type:XiaoerAddonImage
                        列.prop(图像, '贴图', text='')