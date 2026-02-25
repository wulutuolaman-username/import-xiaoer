import bpy  # noqa: F401
from ....属性.属性 import *
from ....指针 import *

名称 = "小二插件：材质节点组"

def 搜索材质节点组(材质:小二材质) -> 小二节点:
    材质节点组 = 材质.node_tree.nodes.get(名称, None)
    return 材质节点组

def 设置材质节点组(self:bpy.types.Operator, 材质:小二材质, 节点组, 材质节点组):
    材质节点组.node_tree = 节点组  # 应用材质节点组
    材质节点组.location = (-200, 1500)  # 定位材质节点组
    材质节点组.name = 名称
    self.report({"INFO"}, f'材质Material["{材质.name}"]输入节点组["{节点组.name}"]')

def 获取材质节点组(self:bpy.types.Operator, 游戏, 节点组列表, 材质:小二材质, 小二材质类型) -> 小二节点:
    节点树 = 材质.node_tree # type:小二着色节点树|bpy.types.ShaderNodeTree
    材质节点组 = 搜索材质节点组(材质)
    if not 材质节点组:
        材质节点组 = 节点树.新建节点.群组
    if not 材质节点组.node_tree or 材质.小二预设模板.材质分类 != 材质.小二预设模板.更新分类:
        for 节点组 in 节点组列表: # type:小二着色节点树  # 设置材质节点组
            if 节点组.判断类型.节点树.是着色节点树 and (  # 搜索材质节点组
                    节点组.name == f"{游戏}{材质.小二预设模板.材质分类}" or
                    (小二材质类型 in 节点组.name and "小二" in 节点组.name)
            ):
                # self.report({"INFO"}, f'材质Material["{材质.name}"]材质节点组ShaderNodeGroup["{节点组.name}"]')
                设置材质节点组(self, 材质, 节点组, 材质节点组)
                break  # 找到后立即退出循环，提高效率
    小二预设模板属性(材质节点组.小二预设模板, None, None, None, None)
    return 材质节点组