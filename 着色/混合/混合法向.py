import bpy

def 混合法向(self,偏好):
    if 偏好.导入贴图 and 偏好.通过点乘混合法向:
        虚拟灯光 = bpy.data.node_groups.get("虚拟灯光") or bpy.data.node_groups.get("虚拟日光")
        点乘 = 虚拟灯光.nodes.new('ShaderNodeVectorMath')
        点乘.operation = 'DOT_PRODUCT'
        点乘.location = (-1260, -100)
        负一 = 虚拟灯光.nodes.new('ShaderNodeVectorMath')
        负一.operation = 'MULTIPLY'
        负一.location = (-1150, -225)
        负一.inputs[0].default_value = (1, -1, 1)
        混合 = 虚拟灯光.nodes.new('ShaderNodeMix')
        混合.data_type = 'VECTOR'
        混合.location = (-1010, -50)
        框 = 虚拟灯光.nodes.new(type='NodeFrame')
        框.label = "小二插件：通过点乘混合法向"
        框.location = (-1200, -200)  # 定位
        点乘.parent = 框
        负一.parent = 框
        混合.parent = 框
        虚拟灯光.links.new(点乘.outputs[1], 混合.inputs[0])
        虚拟灯光.links.new(负一.outputs[0], 混合.inputs[4])
        for node in 虚拟灯光.nodes:
            # self.report({"INFO"}, f'{node.type}')
            if node.type == 'VECT_MATH':
                if node.operation == 'DOT_PRODUCT':
                    if node.name != 点乘.name:
                        日光点乘 = node
                        虚拟灯光.links.new(混合.outputs[1],日光点乘.inputs[1])
            if node.type == 'NEW_GEOMETRY':
                几何数据 = node
                虚拟灯光.links.new(几何数据.outputs[1],点乘.inputs[0])
            if node.type == 'GROUP':
                if node.node_tree.name.startswith("法线贴图转换"):
                    法向贴图转换 = node
                    法向贴图转换.location = (-1300, -400)
                    虚拟灯光.links.new(法向贴图转换.outputs[0],点乘.inputs[1])
                    虚拟灯光.links.new(法向贴图转换.outputs[0],负一.inputs[1])
                    虚拟灯光.links.new(法向贴图转换.outputs[0],混合.inputs[5])
        self.report({"INFO"}, f'已完成：通过点乘混合法向')