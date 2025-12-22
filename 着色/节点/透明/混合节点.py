from ....属性.属性 import 小二预设模板属性
from ....指针 import XiaoerNode

def 获取混合节点(材质, 名称='') -> XiaoerNode:
    混合节点 = 材质.node_tree.nodes.get(名称,'')  # type:XiaoerNode
    if not 混合节点:
        混合节点 = 材质.node_tree.nodes.new(type='ShaderNodeMixShader')  # 新建透明节点
        混合节点.name = 名称
        混合节点.location = (235, 1500)  # 定位透明节点
    小二预设模板属性(混合节点.小二预设模板, None, None, None, None)
    return 混合节点