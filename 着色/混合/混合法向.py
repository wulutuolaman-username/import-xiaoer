import bpy

def 混合法向(偏好):
    虚拟灯光 = bpy.data.node_groups.get("虚拟灯光") or bpy.data.node_groups.get("虚拟日光", "")
    if 虚拟灯光:
        if 偏好.导入贴图 and 偏好.通过点乘混合法向:
            点乘 = 虚拟灯光.nodes.new('ShaderNodeVectorMath')
            点乘.operation = 'DOT_PRODUCT'
            点乘.location = (-1260, -100)
            点乘.name = "小二插件：通过点乘混合法向"
            负一 = 虚拟灯光.nodes.new('ShaderNodeVectorMath')
            负一.operation = 'MULTIPLY'
            负一.location = (-1150, -225)
            负一.inputs[0].default_value = (1, -1, 1)
            负一.name = "小二插件：通过点乘混合法向"
            混合 = 虚拟灯光.nodes.new('ShaderNodeMix')
            混合.data_type = 'VECTOR'
            混合.location = (-1010, -50)
            混合.name = "小二插件：通过点乘混合法向"
            框 = 虚拟灯光.nodes.new(type='NodeFrame')
            框.label = "小二插件：通过点乘混合法向"
            框.location = (-1200, -200)  # 定位
            框.name = "小二插件：通过点乘混合法向"
            点乘.parent = 框
            负一.parent = 框
            混合.parent = 框
            虚拟灯光.links.new(点乘.outputs[1], 混合.inputs[0])
            虚拟灯光.links.new(负一.outputs[0], 混合.inputs[4])
            for 节点 in 虚拟灯光.nodes:
                # self.report({"INFO"}, f'{node.type}')
                if 节点.type == 'VECT_MATH':
                    if 节点.operation == 'DOT_PRODUCT':
                        if 节点.name != 点乘.name:
                            日光点乘 = 节点
                            虚拟灯光.links.new(混合.outputs[1],日光点乘.inputs[1])
                if 节点.type == 'NEW_GEOMETRY':
                    几何数据 = 节点
                    虚拟灯光.links.new(几何数据.outputs[1],点乘.inputs[0])
                if 节点.type == 'GROUP':
                    if 节点.node_tree.name.startswith("法线贴图转换"):
                        法线贴图转换 = 节点
                        法线贴图转换.location = (-1300, -400)
                        虚拟灯光.links.new(法线贴图转换.outputs[0], 点乘.inputs[1])
                        虚拟灯光.links.new(法线贴图转换.outputs[0], 负一.inputs[1])
                        虚拟灯光.links.new(法线贴图转换.outputs[0], 混合.inputs[5])
            # self.report({"INFO"}, f'已完成：通过点乘混合法向')
        if not 偏好.通过点乘混合法向:
            for 节点 in 虚拟灯光.nodes:
                if 节点.name == "小二插件：通过点乘混合法向":
                    虚拟灯光.nodes.remove(节点)
            法线贴图转换 = next((节点 for 节点 in 虚拟灯光.nodes
                           if 节点.type == 'GROUP'
                           and 节点.node_tree.name.startswith("法线贴图转换")) ,None)
            点乘 = next((节点 for 节点 in 虚拟灯光.nodes if 节点.type == 'VECT_MATH' and 节点.operation == 'DOT_PRODUCT') ,None)
            if 法线贴图转换 and 点乘:
                虚拟灯光.links.new(法线贴图转换.outputs[0], 点乘.inputs[1])
    # else:
    #     self.report({"ERROR"}, f'未找到名为虚拟灯光或虚拟日光的节点组')