import bpy  # noqa: F401
from typing import List
from ....指针 import *  # noqa: F401
from .材质节点组 import *
from ....属性.属性 import *

def 获取材质节点组(self:bpy.types.Operator, 节点组列表:List[小二着色节点树|小二几何节点树|小二合成节点树], 材质:小二材质):
    节点树 = 材质.node_tree # type:小二着色节点树|bpy.types.ShaderNodeTree
    调色节点组 = 搜索材质节点组(材质)
    if not 调色节点组:
        调色节点组 = 节点树.新建节点.群组
    if not 调色节点组.node_tree or 材质.小二预设模板.材质分类 != 材质.小二预设模板.更新分类:
        眼睫 = next((组 for 组 in 节点组列表 if 组.判断类型.节点树.是着色节点树  and 组.name == "眼睫"), None)
        调色 = next((组 for 组 in 节点组列表 if 组.判断类型.节点树.是着色节点树  and any(组.name.startswith(前缀) for 前缀 in ["调色", "校色"])), None)
        if 眼睫 and 材质.小二预设模板.初始分类 == '五官':
            设置材质节点组(self, 材质, 眼睫, 调色节点组)
        else:
            设置材质节点组(self, 材质, 调色, 调色节点组)
        # self.report({"INFO"}, f'材质Material["{材质.name}"]应用节点组:ShaderNodeNodeTree["{调色节点组.node_tree.name}"]')
    小二预设模板属性(调色节点组.小二预设模板, None, None, None, None)
    return 调色节点组