from ....指针 import *

名称 = "小二插件：基础贴图节点"

def 搜索基础贴图节点(材质:小二材质) -> 小二节点:
    基础贴图节点 = 材质.node_tree.nodes.get(名称, None)
    return 基础贴图节点

def 获取基础贴图节点(材质:小二材质) -> 小二节点:
    import bpy
    节点树 = 材质.node_tree # type:小二着色节点树|bpy.types.ShaderNodeTree
    基础贴图节点 = 搜索基础贴图节点(材质)
    if not 基础贴图节点:
        基础贴图节点 = 节点树.新建节点.图像  # 新建图像节点
        基础贴图节点.location = (-500, 1500)  # 定位图像节点
        基础贴图节点.name = 名称
    return 基础贴图节点