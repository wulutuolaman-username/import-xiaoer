def 获取材质输出节点(材质):
    for 节点 in 材质.node_tree.nodes:
        if 节点.type == 'OUTPUT_MATERIAL' and 节点.is_active_output:
            return 节点
    return 材质.node_tree.nodes.new(type='ShaderNodeOutputMaterial')