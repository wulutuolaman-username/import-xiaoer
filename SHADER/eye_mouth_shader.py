from .texture.Diffuse import diffuse_texture

def eye_mouth_shader(self,prefs,data_from,diffuse_images,material):
    correct_color_node_group = material.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    node_group = next((ng for ng in data_from.node_groups if ng.name == "眼睫"), None)
    if not node_group:
        for node_group in data_from.node_groups:  # 设置材质节点组并输出材质
            if node_group.type == 'SHADER' and any(node_group.name.startswith(suffix) for suffix in ["调色", "校色"]):  # 搜索材质节点组
                correct_color_node_group.node_tree = node_group  # 应用节点组
    else:
        correct_color_node_group.node_tree = node_group  # 应用节点组
    self.report({"INFO"}, f'材质Material["{material.name}"]应用节点组:ShaderNodeNodeTree["{correct_color_node_group.node_tree.name}"]')
    correct_color_node_group.location = (-200, 1500)  # 定位节点组
    output_node = (material.node_tree.nodes.get("材质输出") or material.node_tree.nodes.get("Material Output"))  # 找到材质输出节点
    alpha = material.node_tree.nodes["mmd_shader"].inputs[12].default_value
    if alpha < 1:
        transparent_node = material.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')  # 新建透明节点
        transparent_node.location = (-200, 1600)  # 定位透明节点
        mix_node = material.node_tree.nodes.new(type='ShaderNodeMixShader')  # 新建混合节点
        mix_node.location = (250, 1500)  # 定位混合节点
        mix_node.inputs[0].default_value = alpha
        material.node_tree.links.new(
            transparent_node.outputs[0],  # 节点组的输出插槽
            mix_node.inputs[1]  # 输出节点的输入插槽
        )
        material.node_tree.links.new(
            correct_color_node_group.outputs[0],  # 节点组的输出插槽
            mix_node.inputs[2]  # 输出节点的输入插槽
        )
        material.blend_method = 'BLEND'  # 材质模式
        self.report({"INFO"}, f'材质Material["{material.name}"]根据MMDShaderDev的alpha设置透明')
        # material.node_tree.links.new(
        #     mix_node.outputs[0],  # 节点的输出插槽
        #     output_node.inputs['Surface']  # 输出节点的输入插槽
        # )
    else:  # 材质节点组直接输出
        material.node_tree.links.new(
            correct_color_node_group.outputs[0],  # 节点组的输出插槽
            output_node.inputs['Surface']  # 输出节点的输入插槽
        )
    if prefs.import_image:  # 如果开启了导入贴图
        node, original_image, diffuse_image = diffuse_texture(self, material, diffuse_images)  # 基础贴图
        if diffuse_image:
            self.report({"INFO"}, f'材质Material["{material.name}"]输入贴图:Texture["{diffuse_image.name}"]')
            image_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
            image_node.image = diffuse_image  # 应用贴图
            image_node.location = (-500, 1500)  # 定位图像节点
            material.node_tree.links.new(
                image_node.outputs[0],  # 图像节点的输出插槽
                correct_color_node_group.inputs[0]  # 输出节点的输入插槽
            )
        else:
            self.report({"WARNING"}, f'材质Material["{material.name}"]未找到匹配的基础贴图')
            if node:  # 薇塔的眼睛2材质没有基础贴图
                material.node_tree.links.new(
                    node.outputs[0],  # 图像节点的输出插槽
                    correct_color_node_group.inputs[0]  # 输出节点的输入插槽
                )
