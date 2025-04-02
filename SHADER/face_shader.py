from .texture.Diffuse import diffuse_texture

def face_shader(self,prefs,data_from,diffuse_images,alpha_images,material):
    output_node = (material.node_tree.nodes.get("材质输出") or material.node_tree.nodes.get("Material Output"))  # 找到材质输出节点
    MMDShaderDev = material.node_tree.nodes["mmd_shader"]
    if MMDShaderDev.inputs[12].default_value == 0:
        transparent_node = material.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')  # 新建透明节点
        transparent_node.location = (-200, 1600)  # 定位透明节点
        material.node_tree.links.new(
            transparent_node.outputs[0],  # 节点组的输出插槽
            output_node.inputs['Surface']  # 输出节点的输入插槽
        )
        self.report({"INFO"}, f'材质Material["{material.name}"]根据MMDShaderDev的alpha值为0设为透明')
        return  # 如果MMD节点组设置为透明，材质直接输出透明，然后进入下一个循环
    face_node_group = material.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    sdftex_node_group = material.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    found_face = False
    found_sdftex = False
    for node_group in data_from.node_groups:  # 设置材质节点组并输出材质
        if node_group.type == 'SHADER' and ("脸" in node_group.name or "face" in node_group.name):  # 搜索材质节点组
            self.report({"INFO"}, f'材质Material["{material.name}"]应用节点组:ShaderNodeNodeTree["{node_group.name}"]')
            face_node_group.node_tree = node_group  # 应用节点组
            face_node_group.location = (-200, 1500)  # 定位节点组
            found_face = True  # 记录已找到
        if node_group.type == 'SHADER' and node_group.name == "SDF.tex":
            sdftex_node_group.node_tree = node_group  # 获取节点组
            sdftex_node_group.location = (-800, 1500)  # 定位节点组
            found_sdftex = True  # 记录已找到
        # 当两个节点组都找到时，跳出循环
        if found_face and found_sdftex:
            break
    material.node_tree.links.new(
        face_node_group.outputs[0],  # 节点组的输出插槽
        output_node.inputs['Surface']  # 输出节点的输入插槽
    )
    if prefs.import_image:  # 如果开启了导入贴图
        node,original_image,diffuse_image = diffuse_texture(self,material,diffuse_images)  # 基础贴图
        if diffuse_image:
            self.report({"INFO"}, f'材质Material["{material.name}"]输入贴图:Texture["{diffuse_image.name}"]')
            image_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
            image_node.image = diffuse_image  # 应用贴图
            if alpha_images:
                if diffuse_image in alpha_images:
                    image_node.image.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
            image_node.location = (-500, 1500)  # 定位图像节点
            material.node_tree.links.new(
                image_node.outputs[0],  # 图像节点的输出插槽
                face_node_group.inputs[0]  # 输出节点的输入插槽
            )
        else:
            self.report({"WARNING"}, f'材质Material["{material.name}"]未找到匹配的基础贴图')
            if node:  # 薇塔的眼睛2材质没有基础贴图
                material.node_tree.links.new(
                    node.outputs[0],  # 图像节点的输出插槽
                    face_node_group.inputs[0]  # 输出节点的输入插槽
                )
