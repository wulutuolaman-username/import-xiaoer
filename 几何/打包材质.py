# coding: utf-8

import bpy, mathutils
from typing import List, cast
from ..属性.属性 import 小二预设模板属性
from ..指针 import XiaoerNode, XiaoerGeometryNodeTree

def 布尔节点(self:bpy.types.Operator, 组节点:bpy.types.Node | bpy.types.NodeGroup, 材质类:List[bpy.types.Material], 起点:mathutils.Vector=(-1000, 0)):
    """创建层级化布尔运算树结构"""
    # 创建材质选择节点列
    选择节点 = []
    x, y = 起点
    for i, 材质 in enumerate(材质类):
        材质选择节点 = cast(XiaoerNode, 组节点.node_tree.nodes.new('GeometryNodeMaterialSelection'))
        小二预设模板属性(材质选择节点.小二预设模板, None, None, None, None)
        材质选择节点.name = "小二插件：材质选择节点"
        # 使用类型断言告诉IDE这是NodeSocketMaterial
        材质输入接口 = cast(bpy.types.NodeSocketMaterial, 材质选择节点.inputs[0])
        材质输入接口.default_value = 材质
        材质选择节点.location = (x, y - i * 100)
        选择节点.append(材质选择节点)

    # 收集初始接口
    当前数量 = [(n.outputs[0], n.location) for n in 选择节点]

    # 逐层创建布尔节点
    while len(当前数量) > 1:
        更新数量 = []
        x += 200  # 每列间隔

        # 成对处理节点
        for i in range(0, len(当前数量), 2):  # 循环步长为 2
            if i + 1 >= len(当前数量):
                # 奇数情况直接传递
                更新数量.append(当前数量[i])
                continue

            # 创建布尔节点
            布尔节点 = cast(XiaoerNode, 组节点.node_tree.nodes.new('FunctionNodeBooleanMath'))
            小二预设模板属性(布尔节点.小二预设模板, None, None, None, None)
            布尔节点.name = "小二插件：布尔节点"
            布尔节点.operation = 'OR'
            布尔节点.location = (x, (当前数量[i][1].y + 当前数量[i + 1][1].y) / 2)

            # 连接前一层输出
            组节点.node_tree.links.new(当前数量[i][0], 布尔节点.inputs[0])
            组节点.node_tree.links.new(当前数量[i + 1][0], 布尔节点.inputs[1])

            更新数量.append((布尔节点.outputs[0], 布尔节点.location))

        当前数量 = 更新数量

    输出节点 = next((节点 for 节点 in 组节点.node_tree.nodes if 节点.type == 'GROUP_OUTPUT'),None)
    if 输出节点: # 1.1.0 已有输出节点，补充材质节点用
        布尔运算 = 输出节点.inputs[0].links[0].from_node
        布尔节点 = 组节点.node_tree.nodes.new('FunctionNodeBooleanMath')
        布尔节点.operation = 'OR'
        布尔节点.location = ((布尔运算.location.x + 输出节点.location.x)/2, (布尔运算.location.y + 输出节点.location.y)/2)
        组节点.node_tree.links.new(布尔运算.outputs[0], 布尔节点.inputs[0])
        if 当前数量:
            组节点.node_tree.links.new(当前数量[0][0], 布尔节点.inputs[1])
        组节点.node_tree.links.new(布尔节点.outputs[0], 输出节点.inputs[0])
    else: # 没有输出节点，新建节点组用
        输出节点 = 组节点.node_tree.nodes.new('NodeGroupOutput')# 创建输出节点
        if len(材质类) > 1:
            输出节点.location = (x + 200, 当前数量[0][1].y)
        if 当前数量:
            组节点.node_tree.links.new(当前数量[0][0], 输出节点.inputs[0])

def 打包材质(self, 节点组, 材质类):
    # 创建独立节点组容器
    新节点组 = bpy.data.node_groups.get("clothes")
    if not 新节点组:  # 1.1.0fbx模型分离
        新节点组 = bpy.data.node_groups.new("clothes", 'GeometryNodeTree')  # type: ignore
    # 使用类型断言告诉IDE这是GeometryNodeTree
    新节点组 = cast(XiaoerGeometryNodeTree, 新节点组)
    小二预设模板属性(新节点组.小二预设模板, None, None, None, None)
    # 添加输出接口（在容器上操作）
    if bpy.app.version >= (4, 0, 0):
        新节点组.interface.new_socket('布尔', in_out='OUTPUT', socket_type='NodeSocketBool')
    else:
        新节点组.outputs.new('NodeSocketBool', '布尔')

    # 创建节点组
    组节点: XiaoerNode = 节点组.nodes.new(type='GeometryNodeGroup')
    小二预设模板属性(组节点.小二预设模板, None, None, None, None)
    组节点.node_tree = 新节点组
    组节点.location = (-200,-200)

    # 清空现有节点
    组节点.node_tree.nodes.clear()

    # 生成布尔树结构
    布尔节点(self, 组节点, 材质类)