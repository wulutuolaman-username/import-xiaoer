import bpy

def create_bool_tree(group, materials, start_pos=(-1000, 0)):
    """创建层级化布尔运算树结构"""
    # 创建材质选择节点列
    select_nodes = []
    x, y = start_pos
    for i, mat in enumerate(materials):
        node = group.node_tree.nodes.new('GeometryNodeMaterialSelection')
        node.inputs[0].default_value = mat
        node.location = (x, y - i * 100)
        select_nodes.append(node)

    # 收集初始接口
    current_level = [(n.outputs[0], n.location) for n in select_nodes]
    column = 0
    bool_nodes = []

    # 逐层创建布尔节点
    while len(current_level) > 1:
        column += 1
        new_level = []
        bool_column = []
        x += 200  # 每列间隔

        # 成对处理节点
        for i in range(0, len(current_level), 2):
            if i + 1 >= len(current_level):
                # 奇数情况直接传递
                new_level.append(current_level[i])
                continue

            # 创建布尔节点
            bool_node = group.node_tree.nodes.new('FunctionNodeBooleanMath')
            bool_node.operation = 'OR'
            bool_node.location = (x, (current_level[i][1].y + current_level[i + 1][1].y) / 2)
            bool_column.append(bool_node)

            # 连接前一层输出
            group.node_tree.links.new(current_level[i][0], bool_node.inputs[0])
            group.node_tree.links.new(current_level[i + 1][0], bool_node.inputs[1])

            new_level.append((bool_node.outputs[0], bool_node.location))

        current_level = new_level
        bool_nodes.extend(bool_column)

    # 创建输出节点
    output_node = group.node_tree.nodes.new('NodeGroupOutput')
    output_node.location = (x + 200, current_level[0][1].y)
    if current_level:
        group.node_tree.links.new(current_level[0][0], output_node.inputs[0])

    return {
        'select_nodes': select_nodes,
        'bool_nodes': bool_nodes,
        'output_node': output_node
    }


def setup_clothes_group(node_group,clothes_materials):
    # 创建独立节点组容器
    clothes_node_tree = bpy.data.node_groups.new("clothes", 'GeometryNodeTree')
    # 添加输出接口（在容器上操作）
    clothes_node_tree.outputs.new('NodeSocketBool', '布尔')

    # 创建节点组
    group = node_group.nodes.new(type='GeometryNodeGroup')
    group.node_tree = clothes_node_tree
    group.location = (-200,-200)

    # 清空现有节点
    group.node_tree.nodes.clear()

    # 生成布尔树结构
    tree_data = create_bool_tree(group, clothes_materials)

    # # 自动调整接口位置
    # for node in tree_data['select_nodes']:
    #     node.location.y += len(clothes_materials) * 125  # 垂直居中





