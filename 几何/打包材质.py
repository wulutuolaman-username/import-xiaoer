# coding: utf-8

import bpy

def 布尔节点(组, 材质类, 起点=(-1000, 0)):
    """创建层级化布尔运算树结构"""
    # 创建材质选择节点列
    选择节点 = []
    x, y = 起点
    for i, 材质 in enumerate(材质类):
        材质选择节点 = 组.node_tree.nodes.new('GeometryNodeMaterialSelection')
        材质选择节点.inputs[0].default_value = 材质
        材质选择节点.location = (x, y - i * 100)
        选择节点.append(材质选择节点)

    # 收集初始接口
    当前数量 = [(n.outputs[0], n.location) for n in 选择节点]
    # column = 0
    # bool_nodes = []

    # 逐层创建布尔节点
    while len(当前数量) > 1:
        # column += 1
        更新数量 = []
        # bool_column = []
        x += 200  # 每列间隔

        # 成对处理节点
        for i in range(0, len(当前数量), 2):  # 循环步长为 2
            if i + 1 >= len(当前数量):
                # 奇数情况直接传递
                更新数量.append(当前数量[i])
                continue

            # 创建布尔节点
            布尔节点 = 组.node_tree.nodes.new('FunctionNodeBooleanMath')
            布尔节点.operation = 'OR'
            布尔节点.location = (x, (当前数量[i][1].y + 当前数量[i + 1][1].y) / 2)
            # bool_column.append(布尔节点)

            # 连接前一层输出
            组.node_tree.links.new(当前数量[i][0], 布尔节点.inputs[0])
            组.node_tree.links.new(当前数量[i + 1][0], 布尔节点.inputs[1])

            更新数量.append((布尔节点.outputs[0], 布尔节点.location))

        当前数量 = 更新数量
        # bool_nodes.extend(bool_column)

    # 创建输出节点
    输出节点 = 组.node_tree.nodes.new('NodeGroupOutput')
    输出节点.location = (x + 200, 当前数量[0][1].y)
    if 当前数量:
        组.node_tree.links.new(当前数量[0][0], 输出节点.inputs[0])

    # return {
    #     '选择节点': 选择节点,
    #     'bool_nodes': bool_nodes,
    #     'output_node': output_node
    # }

def 打包材质(节点组, 材质类):
    # 创建独立节点组容器
    新节点组 = bpy.data.node_groups.new("clothes", 'GeometryNodeTree')
    # 添加输出接口（在容器上操作）
    新节点组.outputs.new('NodeSocketBool', '布尔')

    # 创建节点组
    组 = 节点组.nodes.new(type='GeometryNodeGroup')
    组.node_tree = 新节点组
    组.location = (-200,-200)

    # 清空现有节点
    组.node_tree.nodes.clear()

    # 生成布尔树结构
    布尔节点(组, 材质类)
    # tree_data = 布尔节点(组, clothes_materials)

    # # 自动调整接口位置
    # for node in tree_data['选择节点']:
    #     node.location.y += len(clothes_materials) * 125  # 垂直居中





