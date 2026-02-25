from ....属性.属性 import *
from ....指针 import *

def 获取区域节点(材质, 信息='') -> 小二节点:
    节点树 = 材质.node_tree   # type:小二着色节点树
    区域节点 = 材质.node_tree.nodes.get(信息,'')  # type:小二节点
    if not 区域节点:
        区域节点 = 节点树.新建节点.帧
        区域节点.location = (-205, 1610)
        区域节点.label = 信息
        区域节点.name = 信息
    小二预设模板属性(区域节点.小二预设模板, None, None, None, None)
    return 区域节点