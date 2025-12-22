import bpy
from typing import cast
from ...指针 import XiaoerShaderNodeTree, XiaoerGeometryNodeTree, XiaoerCompositorNodeTree

class NodeGroupPanel(bpy.types.Panel):
    bl_idname = 'NODE_PT_import_xiaoer_nodegroup_1'
    bl_label = '小二预设节点组'
    bl_space_type = 'NODE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = 'Group'        # 侧边栏分类标签

    @classmethod
    def poll(cls, context):
        节点树 = cast(XiaoerShaderNodeTree|XiaoerGeometryNodeTree|XiaoerCompositorNodeTree, context.space_data.edit_tree)  # type:ignore
        return 节点树 and 节点树.type in ['SHADER', 'GEOMETRY', "COMPOSITING"] and 节点树.小二预设模板.使用插件 and 节点树.name in bpy.data.node_groups

    def draw(self, context):
        布局 = self.layout
        节点树 = cast(XiaoerShaderNodeTree|XiaoerGeometryNodeTree|XiaoerCompositorNodeTree, context.space_data.edit_tree)  # type:ignore
        属性 = 节点树.小二预设节点树

        列 = 布局.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        列.prop(属性, '文件')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')

class TemplateNodeGroupPanel(bpy.types.Panel):
    bl_idname = 'NODE_PT_import_xiaoer_nodegroup_2'
    bl_label = '小二预设模板'
    bl_space_type = 'NODE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = 'Group'        # 侧边栏分类标签

    @classmethod
    def poll(cls, context):
        节点树 = cast(XiaoerShaderNodeTree|XiaoerGeometryNodeTree|XiaoerCompositorNodeTree, context.space_data.edit_tree)  # type:ignore
        return 节点树 and 节点树.type in ['SHADER', 'GEOMETRY', "COMPOSITING"] and 节点树.小二预设模板.使用插件 and 节点树.name in bpy.data.node_groups

    def draw(self, context):
        布局 = self.layout
        节点树 = cast(XiaoerShaderNodeTree|XiaoerGeometryNodeTree|XiaoerCompositorNodeTree, context.space_data.edit_tree)  # type:ignore
        属性 = 节点树.小二预设模板

        列 = 布局.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        列.prop(属性, '文件')
        列.prop(属性, '贴图')
        列.prop(属性, '游戏')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')