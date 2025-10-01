# coding: utf-8

import bpy
from .预设 import XiaoerAddonPresetsInformation
from .模板 import XiaoerAddonPresetsTemplateInformation

class XiaoerAddonMaterial(bpy.types.PropertyGroup):
    """ 存储单个贴图选项 """
    材质: bpy.props.PointerProperty(type=bpy.types.Material)

class XiaoerAddonImage(bpy.types.PropertyGroup):
    """ 存储单个贴图选项 """
    贴图: bpy.props.PointerProperty(type=bpy.types.Image)

class XiaoerAddonNodeTree(bpy.types.PropertyGroup):
    """ 存储单个节点组 """
    节点组: bpy.props.PointerProperty(type=bpy.types.NodeTree)

class XiaoerAddonModelPresets(XiaoerAddonPresetsInformation):

    预设材质: bpy.props.CollectionProperty(
        type=XiaoerAddonMaterial
    )
    显示预设材质: bpy.props.BoolProperty(
        name="显示预设材质",
        default=False,
    )

    预设贴图: bpy.props.CollectionProperty(
        type=XiaoerAddonImage
    )
    显示预设贴图: bpy.props.BoolProperty(
        name="显示预设贴图",
        default=False,
    )

    预设节点组: bpy.props.CollectionProperty(
        type=XiaoerAddonNodeTree
    )
    显示预设节点组: bpy.props.BoolProperty(
        name="显示预设节点组",
        default=False,
    )

class XiaoerAddonModelPresetsTemplateInformation(XiaoerAddonPresetsTemplateInformation):

    完成导入模板: bpy.props.BoolProperty(  # 完成模板文件的节点组导入
        name="完成导入模板",
        default=False,
    )
    导入节点组: bpy.props.CollectionProperty(  # 所有导入的节点组
        type=XiaoerAddonNodeTree
    )
    显示导入节点组: bpy.props.BoolProperty(  # 面板显示所有导入的节点组
        name="显示导入节点组",
        default=False,
    )

    完成导入贴图: bpy.props.BoolProperty(  # 完成贴图路径的贴图导入
        name="完成导入贴图",
        default=False,
    )
    导入贴图: bpy.props.CollectionProperty(  # 所有导入贴图
        type=XiaoerAddonImage
    )
    显示导入贴图: bpy.props.BoolProperty(  # 面板显示所有导入的贴图
        name="显示导入贴图",
        default=False,
    )

    基础贴图: bpy.props.CollectionProperty(  # 所有基础贴图
        type=XiaoerAddonImage
    )

    绑定骨骼: bpy.props.StringProperty(
        name="绑定骨骼",
        default="",
    )

    @property
    def 基础贴图枚举项(self):
        """动态生成EnumProperty需要的三元组"""
        return [(贴图.贴图.name, 贴图.贴图.name, "") for 贴图 in self.基础贴图]
    显示基础贴图: bpy.props.BoolProperty(  # 面板只显示所有基础贴图
        name="显示基础贴图",
        default=False,
    )
    完成匹配贴图: bpy.props.BoolProperty(  # 完成模型基础贴图和导入基础贴图的匹配
        name="完成匹配贴图",
        default=False,
    )
