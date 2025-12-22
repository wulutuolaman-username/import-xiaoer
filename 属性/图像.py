# coding: utf-8

import bpy
from .模板 import XiaoerAddonPresetsTemplateInformation

class XiaoerAddonImageNodeTree(bpy.types.PropertyGroup):
    """ 存储单个节点组 """
    材质分类: bpy.props.StringProperty()
    节点组: bpy.props.PointerProperty(type=bpy.types.NodeTree)

class XiaoerAddonImagePresetsTemplateInformation(XiaoerAddonPresetsTemplateInformation):

    def 获取前缀(self):
        return self.正则前缀
    前缀: bpy.props.StringProperty(
        name="前缀",
        get=获取前缀
    )
    正则前缀: bpy.props.StringProperty()

    def 获取部件(self):
        return self.正则部件
    部件: bpy.props.StringProperty(
        name="部件",
        get=获取部件
    )
    正则部件: bpy.props.StringProperty()

    def 获取类型(self):
        return self.正则类型
    类型: bpy.props.StringProperty(
        name="类型",
        get=获取类型
    )
    正则类型: bpy.props.StringProperty()

    匹配贴图: bpy.props.PointerProperty(
        name="匹配贴图",
        type=bpy.types.Image,
    )

    匹配节点组: bpy.props.PointerProperty(
        type=bpy.types.NodeTree,
    )
