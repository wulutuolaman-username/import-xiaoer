def get_ultimate_connected_node(node):
    """ 递归追踪转接节点（Reroute），返回最终连接的节点 """
    if node.type == 'REROUTE':
        if node.inputs and node.inputs[0].is_linked:
            link = node.inputs[0].links[0]
            return get_ultimate_connected_node(link.from_node)
    return node

# 分类设置描边材质
def input_materials(self,node,materials):
    input_sockets = []  # 建立列表存储需要连接的接口
    for input in node.inputs:
        if input.type == 'BOOLEAN' and input.is_linked:  # 设置材质节点的布尔接口
            # self.report({"INFO"}, f"布尔接口:" + str(input))
            for link in input.links:
                connected_node = get_ultimate_connected_node(link.from_node)  # 跳过转接点找到相连节点
                if connected_node.type == 'GROUP':  # 确保相连的是节点组
                    for node_level_3 in sorted(connected_node.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 按位置从上到下
                        if any(node_level_3.name.startswith(suffix) for suffix in ["材质选择", "Material Selection"]):
                            # AttributeError: 'NodeSocketMaterial' object has no attribute 'material'
                            input_socket = next((s for s in node_level_3.inputs if s.name == 'Material'), None)
                            if not input_socket.default_value:  # 如果材质插槽为空
                                input_sockets.append(input_socket)
                    # self.report({"INFO"}, f"接口:" + str(input_sockets))
    # 使用 zip 将材质和接口一一对应
    for material, input_socket in zip(materials, input_sockets):
        input_socket.default_value = material  # 输入材质
        self.report({"INFO"}, f'GeometryNodeTree["{input_socket.node.id_data.name}"]输入材质:Material["{material.name}"]')