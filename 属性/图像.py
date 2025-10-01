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

    # def 限制贴图修改(self, context):
    #     """阻止匹配贴图被直接修改"""
    #     if self.匹配贴图 != self.哈希匹配贴图:
    #         self.匹配贴图 = self.哈希匹配贴图
    匹配贴图: bpy.props.PointerProperty(
        name="匹配贴图",
        type=bpy.types.Image,
        # update=限制贴图修改  # 强制同步回哈希贴图
    )
    # 哈希匹配贴图: bpy.props.PointerProperty(
    #     name="哈希匹配贴图",
    #     type=bpy.types.Image,
    # )

    匹配节点组: bpy.props.PointerProperty(
        type=bpy.types.NodeTree,
    )
    # 匹配节点组: bpy.props.CollectionProperty(
    #     type=XiaoerAddonImageNodeTree,
    # )