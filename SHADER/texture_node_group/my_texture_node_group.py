from .rename_node_group import rename_node_group
from ..texture.Lightmap import lightmap_texture
from ..texture.Normalmap import normalmap_texture
from ..texture.AO import AO_texture

def my_texture_node_group(self,data_from,material,material_node_group,game,diffuse_image,diffuse_image_and_texture_node_group,texture_node_group_name,alpha_images):
    texture_node_group = material.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建贴图节点组
    for node_group in data_from.node_groups:
        if node_group.type == 'SHADER' and f"{texture_node_group_name}" in node_group.name:  # 搜索贴图节点组
            # self.report({"INFO"}, f'调试{texture_node_group_name}')
            texture_node_group.location = (-500, 1500)  # 定位贴图节点组
            if diffuse_image in diffuse_image_and_texture_node_group:  # 检查此类材质是否有多个基础色贴图
                texture_node_group.node_tree = diffuse_image_and_texture_node_group[diffuse_image]  # 直接应用贴图节点组
            elif diffuse_image not in diffuse_image_and_texture_node_group and node_group.users == 0:
                texture_node_group.node_tree = node_group  # 直接应用节点组
                diffuse_image_and_texture_node_group[diffuse_image] = texture_node_group.node_tree  # 存储贴图和贴图节点组对应信息
            elif diffuse_image not in diffuse_image_and_texture_node_group and node_group.users > 0:
                # 如果基础色贴图已使用，并且贴图节点组也已使用，但出现了新的材质贴图，说明该材质类型不止一个基础色贴图
                texture_node_group.node_tree = node_group.copy()  # 应用节点组副本
                # self.report({"INFO"},f'节点组["{texture_node_group.node_tree.name}"]')
                rename_node_group(self, texture_node_group.node_tree)  # 重命名贴图节点组副本
                # self.report({"INFO"}, f'重命名["{texture_node_group.node_tree.name}"]')
                diffuse_image_and_texture_node_group[diffuse_image] = texture_node_group.node_tree  # 存储贴图和贴图节点组对应信息
            self.report({"INFO"},f'材质Material["{material.name}"]应用节点组:ShaderNodeNodeTree["{texture_node_group.node_tree.name}"]')
            for output in texture_node_group.outputs:
                if "基础" in output.name and not "Alpha" in output.name:
                    diffuse_output = output
                if "光照" in output.name and not "Alpha" in output.name:
                    lightmap_output = output
                if "法线" in output.name and not "Alpha" in output.name:
                    normal_output = output
                if "AO" in output.name and not "Alpha" in output.name:
                    AO_output = output
            for input in material_node_group.inputs:
                if "基础" in input.name and not "Alpha" in input.name:
                    diffuse_input = input
                if "光照" in input.name and not "Alpha" in input.name:
                    lightmap_input = input
                if "法线" in input.name and not "Alpha" in input.name:
                    normal_input = input
                if "AO" in input.name and not "Alpha" in input.name:
                    AO_input = input
            try:
                material.node_tree.links.new(diffuse_output, diffuse_input)  # 连接基础色
            except:
                pass
            try:
                material.node_tree.links.new(lightmap_output, lightmap_input)  # 连接光照
            except:
                pass
            try:
                material.node_tree.links.new(normal_output, normal_input)  # 连接法线
            except:
                pass
            try:
                material.node_tree.links.new(AO_output, AO_input)  # 连接AO
            except:
                pass
            output_node = (texture_node_group.node_tree.nodes.get("组输出") or texture_node_group.node_tree.nodes.get(
                "Group Output"))  # 找到材质输出节点
            if diffuse_image:  # 如果材质查找到匹配贴图
                for input_socket in output_node.inputs:
                    # self.report({"INFO"}, f"输出节点插槽: {input_socket.name}")
                    if "基础" in input_socket.name and not "Alpha" in input_socket.name:
                        for link in input_socket.links:
                            image_node = link.from_node
                            image_node.image = diffuse_image  # 输入基础贴图
                            if alpha_images:
                                if diffuse_image in alpha_images:
                                    image_node.image.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
                            self.report({"INFO"},f'材质Material["{material.name}"]输入基础贴图:Texture["{diffuse_image.name}"]')
                    if "光照" in input_socket.name and not "Alpha" in input_socket.name:
                        for link in input_socket.links:
                            lightmap_image_node = link.from_node
                            lightmap_image = lightmap_texture(game, diffuse_image)
                            if lightmap_image:
                                lightmap_image_node.image = lightmap_image  # 输入基础贴图
                                lightmap_image.colorspace_settings.name = 'Non-Color'  # 非彩色
                                self.report({"INFO"},f'材质Material["{material.name}"]输入光照贴图:Texture["{lightmap_image.name}"]')
                            else:
                                self.report({"WARNING"}, f'材质Material["{material.name}"]未找到匹配的光照贴图')
                    if "法线" in input_socket.name and not "Alpha" in input_socket.name:
                        for link in input_socket.links:
                            normalmap_image_node = link.from_node
                            normalmap_image = normalmap_texture(game, diffuse_image)
                            if normalmap_image:
                                normalmap_image_node.image = normalmap_image  # 输入基础贴图
                                normalmap_image.colorspace_settings.name = 'Non-Color'  # 非彩色
                                self.report({"INFO"},f'材质Material["{material.name}"]输入法线贴图:Texture["{normalmap_image.name}"]')
                            else:
                                self.report({"WARNING"}, f'材质Material["{material.name}"]未找到匹配的法线贴图')
                    if "AO" in input_socket.name and not "Alpha" in input_socket.name:
                        for link in input_socket.links:
                            AO_image_node = link.from_node
                            AO_image = AO_texture(game, diffuse_image)
                            if AO_image:
                                AO_image_node.image = AO_image  # 输入基础贴图
                                AO_image.colorspace_settings.name = 'Non-Color'  # 非彩色
                                self.report({"INFO"},f'材质Material["{material.name}"]输入AO贴图:Texture["{AO_image.name}"]')
                            else:
                                self.report({"WARNING"}, f'材质Material["{material.name}"]未找到匹配的AO贴图')
            else:  # 如果材质没有匹配贴图
                self.report({"WARNING"}, f'材质Material["{material.name}"]未找到匹配的基础贴图')