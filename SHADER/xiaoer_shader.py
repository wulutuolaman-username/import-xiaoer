import bpy
import re
from .texture.Diffuse import diffuse_texture
from .texture.Lightmap import lightmap_texture
from .texture.Normalmap import normalmap_texture
from .texture_node_group.Lightmap_node_group import lightmap_texture_node_group
from .texture_node_group.Shadow_Ramp_node_group import ramp_texture_node
from .texture_node_group.my_texture_node_group import my_texture_node_group
from .texture_node_group.rename_node_group import rename_node_group

# 材质输入贴图
def xiaoer_shader(self, prefs, data_from, material, diffuse_images, alpha_images, diffuse_image_and_texture_node_group, material_type, xiaoer_material_type, texture_node_group_name, game, hair_materials, skin_materials, clothes_materials):
    output_node = (material.node_tree.nodes.get("材质输出") or material.node_tree.nodes.get("Material Output"))  # 找到材质输出节点
    # MMDShaderDev = material.node_tree.nodes["mmd_shader"]  # 设为透明需要在计算描边时删除该材质
    # if MMDShaderDev.inputs[12].default_value == 0:
    #     transparent_node = material.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')  # 新建透明节点
    #     transparent_node.location = (-200, 1600)  # 定位透明节点
    #     material.node_tree.links.new(
    #         transparent_node.outputs[0],  # 节点组的输出插槽
    #         output_node.inputs['Surface']  # 输出节点的输入插槽
    #     )
    #     self.report({"INFO"}, f'材质Material["{material.name}"]根据MMDShaderDev的alpha值为0设为透明"]')
    #     return  # 如果MMD节点组设置为透明，直接输出透明，然后进入下一个循环
    material_node_group = material.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    for node_group in data_from.node_groups:  # 设置材质节点组
        if node_group.type == 'SHADER' and (  # 搜索材质节点组
                node_group.name == f"{game}{material_type}" or
                # node_group.name.startswith(xiaoer_material_type) or
                (xiaoer_material_type in node_group.name and "小二" in node_group.name)
        ):
            material_node_group.node_tree = node_group  # 应用材质节点组
            material_node_group.location = (-200, 1500)  # 定位材质节点组
            material.node_tree.links.new(
                material_node_group.outputs[0],  # 材质节点组的输出插槽
                output_node.inputs['Surface']  # 材质输出节点的输入插槽
            )
            break  # 找到后立即退出循环，提高效率
    if prefs.import_image:  # 如果开启了导入贴图
        node,original_image,diffuse_image = diffuse_texture(self, material, diffuse_images)  # 基础贴图
        if not diffuse_image:
            # 如果没有匹配基础贴图，尝试根据材质分类指定基础贴图，出错概率较大
            if game != "鸣潮":
                if material in skin_materials or material in clothes_materials:
                    diffuse_image = next((dif_image for ori_image,dif_image in diffuse_images.items() if "Body" in dif_image.name),None)
                elif material in hair_materials:
                    diffuse_image = next((dif_image for ori_image,dif_image in diffuse_images.items() if "Hair" in dif_image.name),None)
                else:  # 如果没有检索到材质的匹配贴图，材质节点组连接原始贴图
                    material.node_tree.links.new(
                        node.outputs[0],  # 节点的输出插槽
                        material_node_group.inputs[0]  # 节点组的输入插槽
                    )
            if game == "鸣潮":
                if material in skin_materials or material in clothes_materials:
                    diffuse_image = next((dif_image for ori_image,dif_image in diffuse_images.items() if "Up" in dif_image.name),None)
                elif material in hair_materials:
                    diffuse_image = next((dif_image for ori_image,dif_image in diffuse_images.items() if "Hair" in dif_image.name),None)
                else:  # 如果没有检索到材质的匹配贴图，材质节点组连接原始贴图
                    material.node_tree.links.new(
                        node.outputs[0],  # 节点的输出插槽
                        material_node_group.inputs[0]  # 节点组的输入插槽
                    )
        if diffuse_image:  # 如果检索到材质的匹配贴图
            if material_node_group.node_tree.name == f"{game}{material_type}":  # 如果是我的中文名节点组模板
                my_texture_node_group(self, data_from, material, material_node_group, game, diffuse_image, diffuse_image_and_texture_node_group, texture_node_group_name, alpha_images)
                # # self.report({"INFO"}, f'调试{material_type}')
                # texture_node_group = material.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建贴图节点组
                # for node_group in data_from.node_groups:
                #     if node_group.type == 'SHADER' and node_group.name.endswith(texture_node_group_name):  # 搜索贴图节点组
                #         # self.report({"INFO"}, f'调试{texture_node_group_name}')
                #         texture_node_group.location = (-500, 1500)  # 定位贴图节点组
                #         if diffuse_image in diffuse_image_and_texture_node_group:  # 检查此类材质是否有多个基础色贴图
                #             texture_node_group.node_tree = diffuse_image_and_texture_node_group[diffuse_image]  # 直接应用贴图节点组
                #         elif diffuse_image not in diffuse_image_and_texture_node_group and node_group.users == 0:
                #             texture_node_group.node_tree = node_group  # 直接应用节点组
                #             diffuse_image_and_texture_node_group[diffuse_image] = texture_node_group.node_tree  # 存储贴图和贴图节点组对应信息
                #         elif diffuse_image not in diffuse_image_and_texture_node_group and node_group.users > 0:
                #             # 如果基础色贴图已使用，并且贴图节点组也已使用，但出现了新的材质贴图，说明该材质类型不止一个基础色贴图
                #             texture_node_group.node_tree = node_group.copy()  # 应用节点组副本
                #             diffuse_image_and_texture_node_group[diffuse_image] = texture_node_group.node_tree  # 存储贴图和贴图节点组对应信息
                #         self.report({"INFO"}, f'材质Material["{material.name}"]应用节点组:ShaderNodeNodeTree["{texture_node_group.node_tree.name}"]')
                #         for output in texture_node_group.outputs:
                #             if "基础" in output.name and not "Alpha" in output.name:
                #                 diffuse_output = output
                #             if "光照" in output.name and not "Alpha" in output.name:
                #                 lightmap_output = output
                #             if "法线" in output.name and not "Alpha" in output.name:
                #                 normal_output = output
                #             if "AO" in output.name and not "Alpha" in output.name:
                #                 AO_output = output
                #         for input in material_node_group.inputs:
                #             if "基础" in input.name and not "Alpha" in input.name:
                #                 diffuse_input = input
                #             if "光照" in input.name and not "Alpha" in input.name:
                #                 lightmap_input = input
                #             if "法线" in input.name and not "Alpha" in input.name:
                #                 normal_input = input
                #             if "AO" in input.name and not "Alpha" in input.name:
                #                 AO_input = input
                #         try:
                #             material.node_tree.links.new(diffuse_output, diffuse_input)  # 连接基础色
                #         except:
                #             pass
                #         try:
                #             material.node_tree.links.new(lightmap_output, lightmap_input)  # 连接光照
                #         except:
                #             pass
                #         try:
                #             material.node_tree.links.new(normal_output, normal_input)  # 连接法线
                #         except:
                #             pass
                #         try:
                #             material.node_tree.links.new(AO_output, AO_input)  # 连接AO
                #         except:
                #             pass
                #         output_node = (texture_node_group.node_tree.nodes.get("组输出") or texture_node_group.node_tree.nodes.get("Group Output"))  # 找到材质输出节点
                #         for input_socket in output_node.inputs:
                #             # self.report({"INFO"}, f"输出节点插槽: {input_socket.name}")
                #             if "基础" in input_socket.name and not "Alpha" in input_socket.name:
                #                 for link in input_socket.links:
                #                     image_node = link.from_node
                #                     if diffuse_image:  # 如果材质查找到匹配贴图
                #                         image_node.image = diffuse_image  # 输入基础贴图
                #                         if alpha_images:
                #                             if diffuse_image in alpha_images:
                #                                 image_node.image.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
                #                         self.report({"INFO"},f'材质Material["{material.name}"]输入基础贴图:Texture["{diffuse_image.name}"]')
                #                     else:
                #                         self.report({"WARNING"},f'材质Material["{material.name}"]未找到匹配的基础贴图')
            elif "小二" in material_node_group.node_tree.name:  # 小二的英文名节点组模板
                # self.report({"INFO"}, f'小二')
                if diffuse_image:  # 如果材质查找到匹配贴图
                    image_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
                    image_node.image = diffuse_image  # 应用贴图
                    if alpha_images:
                        if diffuse_image in alpha_images:
                            image_node.image.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
                    self.report({"INFO"}, f'材质Material["{material.name}"]输入基础贴图:Texture["{diffuse_image.name}"]')
                    image_node.location = (-500, 1500)  # 定位图像节点
                    # 光照贴图
                    lightmap_node_group = None  # 初始化
                    if diffuse_image in diffuse_image_and_texture_node_group:  # 检查贴图和材质节点组的使用情况
                        material_node_group.node_tree = diffuse_image_and_texture_node_group[diffuse_image]  # 字典匹配
                        # self.report({"INFO"},f'材质Material["{material.name}"]应用材质节点组:ShaderNodeNodeTree["{material_node_group.node_tree.name}"]')
                        lightmap_node_group = lightmap_texture_node_group(game, material_node_group) # 找到ligthmap节点组
                        # self.report({"INFO"}, f'材质Material["{material.name}"]应用光照贴图节点组{lightmap_node_group.node_tree.name}')
                    elif diffuse_image not in diffuse_image_and_texture_node_group and material_node_group.node_tree.users == 1:
                        # self.report({"INFO"},f'材质Material["{material.name}"]应用节点组:ShaderNodeNodeTree["{material_node_group.node_tree.name}"]')
                        diffuse_image_and_texture_node_group[diffuse_image] = material_node_group.node_tree  # 存储贴图和材质节点组对应信息
                        lightmap_node_group = lightmap_texture_node_group(game, material_node_group) # 找到ligthmap节点组
                        self.report({"INFO"},f'材质Material["{material.name}"]第一个应用光照贴图节点组{lightmap_node_group.node_tree.name}')
                    elif diffuse_image not in diffuse_image_and_texture_node_group and material_node_group.node_tree.users > 1:
                        material_node_group.node_tree = material_node_group.node_tree.copy()  # 应用节点组副本
                        rename_node_group(self,material_node_group.node_tree)  # 重命名材质节点组副本
                        self.report({"INFO"},f'材质Material["{material.name}"]创建材质节点组副本:ShaderNodeNodeTree["{material_node_group.node_tree.name}"]')
                        diffuse_image_and_texture_node_group[diffuse_image] = material_node_group.node_tree  # 存储贴图和材质节点组对应信息
                        lightmap_node_group = lightmap_texture_node_group(game, material_node_group)  # 找到ligthmap节点组
                        lightmap_node_group.node_tree = lightmap_node_group.node_tree.copy()  # 应用节点组副本
                        rename_node_group(self,lightmap_node_group.node_tree)  # 重命名光照贴图节点组副本
                        self.report({"INFO"}, f'材质Material["{material.name}"创建光照贴图节点组副本{lightmap_node_group.node_tree.name}')
                    lightmap_node = next((node for node in lightmap_node_group.node_tree.nodes if node.type == 'TEX_IMAGE'),None)  # 找到ligthmap贴图节点
                    lightmap_image = lightmap_texture(game,diffuse_image)
                    if lightmap_image:
                        lightmap_node.image = lightmap_image  # 应用光照贴图
                        self.report({"INFO"}, f'材质Material["{material.name}"]输入光照贴图:Texture["{lightmap_image.name}"]')
                        lightmap_image.colorspace_settings.name = 'Non-Color'  # 非彩色
                    # 法线贴图
                    Normalmap_image = normalmap_texture(game,diffuse_image)
                    # self.report({"INFO"}, f'材质Material["{material.name}"]调试Normalmap_image["{Normalmap_image}"]')
                    if Normalmap_image:
                        Normalmap_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
                        Normalmap_node.image = Normalmap_image  # 应用法线贴图
                        self.report({"INFO"},f'材质Material["{material.name}"]输入法线贴图:Texture["{Normalmap_image.name}"]')
                        Normalmap_node.location = (-500, 1000)
                        Normalmap_image.colorspace_settings.name = 'Non-Color'  # 非彩色
                        material.node_tree.links.new(  # 法线贴图颜色
                            Normalmap_node.outputs[0],  # 图像节点的输出插槽
                            material_node_group.inputs[2]  # 输出节点的输入插槽
                        )
                    # Ramp贴图
                    ramp_texture_node(self, game, material, material_node_group, diffuse_image)
                    # 节点相连
                    material.node_tree.links.new(  # 基础贴图颜色
                        image_node.outputs[0],  # 图像节点的输出插槽
                        material_node_group.inputs[0]  # 输出节点的输入插槽
                    )
                    if len(material_node_group.inputs) > 1 and "Alpha" in material_node_group.inputs[1].name:
                        material.node_tree.links.new(  # 基础贴图Alpha
                            image_node.outputs[1],  # 图像节点的输出插槽
                            material_node_group.inputs[1]  # 输出节点的输入插槽
                        )
                else:
                    self.report({"WARNING"}, f'材质Material["{material.name}"]未找到匹配的基础贴图')
                    if node:  # 薇塔的眼睛2材质没有基础贴图
                        material.node_tree.links.new(
                            node.outputs[0],  # 图像节点的输出插槽
                            material_node_group.inputs[0]  # 输出节点的输入插槽
                        )