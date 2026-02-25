from ...指针 import *

def 获取材质输出节点(材质):
    节点树 = 材质.node_tree   # type:小二着色节点树
    for 节点 in 材质.node_tree.nodes:   # type:小二节点
        if 节点.判断类型.节点.着色.是材质输出 and 节点.is_active_output:  # type:ignore
            return 节点
    return 节点树.新建节点.材质输出