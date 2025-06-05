def 混合贴图(self, 偏好,材质, 图像节点, 贴图节点, 材质节点组, 材质输出节点):
    if 偏好.导入贴图 and 偏好.通过alpha混合贴图:
        贴图节点.location = (-840, 1600)
        映射范围 = 材质.node_tree.nodes.new(type='ShaderNodeMapRange')
        映射范围.location = (-550, 1440)
        混合颜色 = 材质.node_tree.nodes.new(type='ShaderNodeMix')
        混合颜色.location = (-375, 1500)
        混合颜色.data_type = 'RGBA'
        透明节点 = 材质.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')  # 新建透明节点
        透明节点.location = (-200, 1600)  # 定位透明节点
        混合节点 = 材质.node_tree.nodes.new(type='ShaderNodeMixShader')  # 新建混合节点
        混合节点.location = (250, 1500)  # 定位混合节点
        材质.node_tree.links.new(
            透明节点.outputs[0],  # 节点组的输出插槽
            混合节点.inputs[1]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            材质节点组.outputs[0],  # 节点组的输出插槽
            混合节点.inputs[2]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            混合节点.outputs[0],  # 节点组的输出插槽
            材质输出节点.inputs['Surface']  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            图像节点.outputs[1],  # 节点组的输出插槽
            映射范围.inputs[0]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            图像节点.outputs[1],  # 节点组的输出插槽
            映射范围.inputs[1]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            映射范围.outputs[0],  # 节点组的输出插槽
            混合颜色.inputs[0]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            图像节点.outputs[0],  # 节点组的输出插槽
            混合颜色.inputs[6]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            贴图节点.outputs[0],  # 节点组的输出插槽
            混合颜色.inputs[7]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            混合颜色.outputs[2],  # 图像节点的输出插槽
            材质节点组.inputs[0]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            图像节点.outputs[1],  # 节点组的输出插槽
            混合节点.inputs[0]  # 输出节点的输入插槽
        )
        框 = 材质.node_tree.nodes.new(type='NodeFrame')
        框.label = "小二插件：通过alpha混合贴图"
        框.location = (-600, 1500)  # 定位
        映射范围.parent = 框
        混合颜色.parent = 框
        self.report({"INFO"}, f'已完成：通过alpha混合贴图')
    else:
        材质.node_tree.links.new(
            材质节点组.outputs[0],  # 节点组的输出插槽
            材质输出节点.inputs['Surface']  # 输出节点的输入插槽
        )