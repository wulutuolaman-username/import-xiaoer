def 搜索基础贴图节点(材质):
    基础贴图节点 = 材质.node_tree.nodes.get("小二插件：基础贴图节点", None)
    return 基础贴图节点

def 获取基础贴图节点(材质):
    基础贴图节点 = 搜索基础贴图节点(材质)
    if not 基础贴图节点:
        基础贴图节点 = 材质.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
        基础贴图节点.location = (-500, 1500)  # 定位图像节点
        基础贴图节点.name = "小二插件：基础贴图节点"
    return 基础贴图节点