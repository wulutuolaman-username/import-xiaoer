# coding: utf-8

def 跳过转接点找到相连节点(节点):
    """ 递归追踪转接节点（Reroute），返回最终连接的节点 """
    if 节点.type == 'REROUTE':
        if 节点.inputs and 节点.inputs[0].is_linked:
            连接 = 节点.inputs[0].links[0]
            return 跳过转接点找到相连节点(连接.from_node)
    return 节点

# 分类设置描边材质
def 输入材质(self, 节点, 材质类):
    接口类 = []  # 建立列表存储需要连接的接口
    for 输入 in 节点.inputs:
        if 输入.type == 'BOOLEAN' and 输入.is_linked:  # 设置材质节点的布尔接口
            # self.report({"INFO"}, f"布尔接口:" + str(输入))
            for 连接 in 输入.links:
                相连节点 = 跳过转接点找到相连节点(连接.from_node)  # 跳过转接点找到相连节点
                if 相连节点.type == 'GROUP':  # 确保相连的是节点组
                    for 三级节点 in sorted(相连节点.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 按位置从上到下
                        if any(三级节点.name.startswith(suffix) for suffix in ["材质选择", "Material Selection"]):
                            # AttributeError: 'NodeSocketMaterial' object has no attribute 'material'
                            材质接口 = next((s for s in 三级节点.inputs if s.name == 'Material'), None)
                            if not 材质接口.default_value:  # 如果材质插槽为空
                                接口类.append(材质接口)
                    # self.report({"INFO"}, f"接口:" + str(接口))
    # 使用 zip 将材质和接口一一对应
    for 材质, 材质接口 in zip(材质类, 接口类):
        材质接口.default_value = 材质  # 输入材质
        self.report({"INFO"}, f'GeometryNodeTree["{材质接口.node.id_data.name}"]输入材质:Material["{材质.name}"]')