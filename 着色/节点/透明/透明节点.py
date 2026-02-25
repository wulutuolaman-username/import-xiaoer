from ....属性.属性 import *
from ....指针 import *

def 获取透明节点(材质, 名称='') -> 小二节点:
    节点树 = 材质.node_tree   # type:小二着色节点树
    透明节点 = 材质.node_tree.nodes.get(名称,'')  # type:小二节点
    if not 透明节点:
        透明节点 = 节点树.新建节点.透明  # 新建透明节点
        透明节点.name = 名称
        透明节点.location = (-200, 1600)  # 定位透明节点
    小二预设模板属性(透明节点.小二预设模板, None, None, None, None)
    return 透明节点