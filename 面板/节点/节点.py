import bpy
from ...指针 import *

class NodePanel(bpy.types.Panel):
    bl_idname = 'NODE_PT_import_xiaoer_node_1'
    bl_label = '小二预设节点'
    bl_space_type = 'NODE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = 'Node'        # 侧边栏分类标签

    @classmethod
    def poll(cls, context):
        节点 = context.active_node  # type:小二节点|bpy.types.Node
        return 节点 and 节点.小二预设节点.使用插件

    def draw(self, context):
        布局 = self.layout
        节点 = context.active_node  # type:小二节点|bpy.types.Node
        属性 = 节点.小二预设节点

        列 = 布局.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        列.prop(属性, '文件')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')

class TemplateNodePanel(bpy.types.Panel):
    bl_idname = 'NODE_PT_import_xiaoer_node_2'
    bl_label = '小二预设模板'
    bl_space_type = 'NODE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = 'Node'        # 侧边栏分类标签

    @classmethod
    def poll(cls, context):
        节点 = context.active_node  # type:小二节点|bpy.types.Node
        return 节点 and 节点.小二预设模板.使用插件

    def draw(self, context):
        布局 = self.layout
        节点 = context.active_node  # type:小二节点|bpy.types.Node
        属性 = 节点.小二预设模板

        列 = 布局.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        列.prop(属性, '文件')
        列.prop(属性, '贴图')
        列.prop(属性, '游戏')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')