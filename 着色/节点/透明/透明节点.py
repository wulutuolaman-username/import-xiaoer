from ....属性.模板 import 小二预设模板属性

def 获取透明节点(材质, 名称=''):
    透明节点 = 材质.node_tree.nodes.get(名称,'')
    if not 透明节点:
        透明节点 = 材质.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')  # 新建透明节点
        透明节点.name = 名称
        透明节点.location = (-200, 1600)  # 定位透明节点
    小二预设模板属性(透明节点.小二预设模板, None, None, None, None)
    return 透明节点