from ...属性.属性 import 小二预设模板属性
from ...指针 import *

def 清理无用节点(材质):
    for 节点 in 材质.node_tree.nodes: # type:小二节点
        if "小二插件" in 节点.name:
            if not 找到输出(节点):
                材质.node_tree.nodes.remove(节点)
                continue
            if not 节点.小二预设模板.使用插件:
                小二预设模板属性(节点.小二预设模板, None, None, None, None)
    # for 节点 in 材质.node_tree.nodes:
    #     if "小二插件" in 节点.name:
    #         if 节点.type == 'FRAME':  # 如果是 NodeFrame，检查其子节点
    #             if not any(n.parent == 节点 for n in 材质.node_tree.nodes):
    #                 材质.node_tree.nodes.remove(节点)

def 找到输出(节点):
    if 节点.outputs:
        # print(节点)
        for 输出 in 节点.outputs:
            if 输出.is_linked:
                for 连接 in 输出.links:
                    # print(节点, 连接.to_node)
                    节点 = 连接.to_node # type:小二节点
                    if 节点.判断类型.节点.着色.是材质输出 or 找到输出(节点):
                        # print(节点, 连接.to_node, True, '\n')
                        return True
                    # else:
                    #     if 找到输出(连接.to_node):
                    #     print(节点, 连接.to_node, False, '\n')
                    #         return True
    # print(节点, False, '\n')
    return False