import bpy
from ..general.Setting import Setting_blend
from ..image.import_and_match import import_and_match
from ..material.material_sort import material_sort
from ..GEOMETRY.GEOMETRY_modifier import GEOMETRY_modifier
from ..GEOMETRY.input_materials import input_materials
from ..GEOMETRY.pack_clothes_materials import setup_clothes_group
from ..SHADER.face_shader import face_shader
from ..SHADER.eye_mouth_shader import eye_mouth_shader
from ..SHADER.emotion_shader import emotion_shader
from ..SHADER.xiaoer_shader import xiaoer_shader
from ..general.bind_bone import bind_bone

def ganfan_xiaoer(self, prefs, model, file_path, image_path):
    # 设置辉光属性和色彩管理
    Setting_blend()

    # 追加预设文件的所有资产
    self.report({"INFO"}, f"开始加载预设模板" + str(file_path) + r"=================================================")
    with bpy.data.libraries.load(file_path) as (data_from, data_to):
        # 仅加载物体、材质和节点组
        data_to.objects = data_from.objects
        data_to.materials = data_from.materials
        data_to.node_groups = data_from.node_groups

    # 当前选中项
    active_item = prefs.game_templates[prefs.active_template_index]
    game = active_item.name  # 获取选中游戏名称

    # 计算贴图哈希和导入贴图，鸣潮可根据名称直接匹配无需哈希
    if prefs.import_image:  # 如果开启了自动匹配贴图
        diffuse_images,alpha_images = import_and_match(self, prefs, image_path)

    # 材质按名称分组，不一定分对
    eye_mouth_materials, emotion_materials, hair_materials, face_material, face_materials, skin_materials, clothes_materials = material_sort(model)
    self.report({"INFO"}, f"材质按名称分组结果----------------------------------------------------------------------------------")
    self.report({"INFO"}, f"眉、睫、眼、口、舌、齿等材质分组: " + " ".join(material.name for material in eye_mouth_materials))
    self.report({"INFO"}, f"表情材质分组: " + " ".join(material.name for material in emotion_materials))
    self.report({"INFO"}, f"头发材质分组: " + " ".join(material.name for material in hair_materials))
    # self.report({"INFO"}, f"脸材质: " + str(face_material.name))
    self.report({"INFO"}, f"脸材质分组: " + " ".join(material.name for material in face_materials))
    self.report({"INFO"}, f"皮肤材质分组: " + " ".join(material.name for material in skin_materials))
    self.report({"INFO"}, f"衣服材质分组: " + " ".join(material.name for material in clothes_materials))

    # 处理节点组
    self.report({"INFO"}, f"处理节点组------------------------------------------------------------------------------------------")
    for node_group in data_from.node_groups:
        # self.report({"INFO"}, f"正在遍历:" + str(node_group))
        if node_group.type == 'GEOMETRY' and node_group.users == 0:  # 未被使用的几何节点组
            GEOMETRY_modifier(model, node_group)  # 应用几何节点
        # 设置描边材质
        if node_group.type == 'GEOMETRY' and "实体化描边" in node_group.name:
            node_level_1 = node_group
            # self.report({"INFO"}, f"找到了:"+str(node_level_1))
            setup_clothes_group(node_group, clothes_materials)  # 打包衣服材质
            input_hair_materials = False
            input_skin_materials = False
            for node_level_2 in node_level_1.nodes:
                if node_level_2.type != 'GROUP':  # 确保节点不是节点数里的节点组，后续能够正确访问名称属性
                    if any(node_level_2.name.startswith(suffix) for suffix in ["删除几何体", "Delete Geometry"]):
                        self.report({"INFO"}, f"无描边材质 删除几何体")
                        input_materials(self, node_level_2, eye_mouth_materials)
                        input_materials(self, node_level_2, emotion_materials)
                        continue
                    if any(node_level_2.name.startswith(suffix) for suffix in ["设置材质", "Set Material"]):
                        # self.report({"INFO"}, f"设置材质节点名称:"+str(node_level_2))
                        material_node = node_level_2
                        # AttributeError: 'GeometryNodeSetMaterial' object has no attribute 'material'
                        input_socket = next((s for s in material_node.inputs if s.name == 'Material'), None)
                        if input_socket and input_socket.default_value:
                            # self.report({"INFO"}, f"接口:" + str(input_socket))
                            edge_material = input_socket.default_value  # 找到描边材质，根据描边材质名称输入模型材质
                            if "头发" in edge_material.name or "hair" in edge_material.name:
                                self.report({"INFO"}, f"描边材质 " + str(edge_material.name))
                                input_materials(self, node_level_2, hair_materials)
                                input_hair_materials = True
                                continue
                            if "皮肤" in edge_material.name or "skin" in edge_material.name:
                                self.report({"INFO"}, f"描边材质 " + str(edge_material.name))
                                input_materials(self, node_level_2, face_materials)
                                input_materials(self, node_level_2, skin_materials)
                                input_skin_materials = True
                                continue
                            if input_hair_materials and input_skin_materials:
                                break  # 如果材质都已输入，提前结束循环for node_level_2 in node_level_1.nodes:
        # 根据脸描边遮罩设置脸材质
        elif node_group.type == 'GEOMETRY' and "描边权重" in node_group.name:
            node_level_2 = node_group
            # self.report({"INFO"}, f"描边权重:" + str(node_group))
            for image_node in node_level_2.nodes:
                if image_node.name.startswith("Image Texture"):  # 查找图像纹理节点:
                    input_socket = next((s for s in image_node.inputs if s.name == 'Image'), None)
                    # self.report({"INFO"}, f"找到描边遮罩:" + str(input_socket.default_value))
                    if input_socket and input_socket.default_value:
                        # self.report({"INFO"}, f"图像接口:" + str(input_socket))
                        edge_image = input_socket.default_value
                        if "face" or "脸" in edge_image.name:
                            # self.report({"INFO"}, f"找到脸描边遮罩")
                            for output in image_node.outputs:
                                if output.is_linked:
                                    for link in output.links:
                                        switch_node = link.to_node
                                        # self.report({"INFO"}, f"切换节点"+str(switch_node))
                                        for input in switch_node.inputs:
                                            if input.type == 'BOOLEAN':
                                                if input.is_linked:
                                                    for link in input.links:
                                                        material_node = link.from_node
                                                        if material_node:
                                                            input_socket = next((s for s in material_node.inputs if s.name == 'Material'),None)
                                                            if input_socket:
                                                                input_socket.default_value = face_material
                                                                self.report({"INFO"},f'设置脸描边遮罩["{edge_image.name}"]脸材质["{face_material.name}"]')
                                                else:
                                                    # 如果切换节点没有连接材质，创建材质选择节点
                                                    material_node = node_level_2.nodes.new(type='GeometryNodeMaterialSelection')
                                                    material_node.location = (360, 360)  # 设置节点位置
                                                    material_input = next((s for s in material_node.inputs if s.name == 'Material'),None)
                                                    material_input.default_value = face_material
                                                    output = material_node.outputs['Selection']
                                                    node_level_2.links.new(output, input)  # 创建连接

    # 处理材质
    self.report({"INFO"}, f"处理材质--------------------------------------------------------------------------------------------")
    diffuse_image_and_texture_node_group = {}  # 记录基础色贴图和材质节点组的对应使用
    self.report({"INFO"}, f'脸材质')
    for material in face_materials:  # 脸材质
        face_shader(self, prefs, data_from, diffuse_images, alpha_images, material)
    self.report({"INFO"}, f'眉、睫、眼、口、舌、齿等材质')
    for material in eye_mouth_materials:  # 眉、睫、眼、口、舌、齿、表情等材质
        eye_mouth_shader(self, prefs, data_from, diffuse_images, material)
    self.report({"INFO"}, f'表情材质')
    for material in emotion_materials:
        material.blend_method = 'BLEND'  # 材质模式
        # material.show_transparent_back = False  # 不显示背面
        emotion_shader(self,prefs,data_from,diffuse_images,material)
    self.report({"INFO"}, f'头发材质')
    for material in hair_materials:
        xiaoer_shader(self, prefs, data_from, material, diffuse_images, alpha_images, diffuse_image_and_texture_node_group, "头发", "hair", "头发贴图", game, hair_materials, skin_materials, clothes_materials)
    self.report({"INFO"}, f'皮肤材质')
    for material in skin_materials:
        xiaoer_shader(self, prefs, data_from, material, diffuse_images, alpha_images, diffuse_image_and_texture_node_group, "皮肤", "clothes", "衣服贴图", game, hair_materials, skin_materials, clothes_materials)
    self.report({"INFO"}, f'衣服材质')
    for material in clothes_materials:
        xiaoer_shader(self, prefs, data_from, material, diffuse_images, alpha_images, diffuse_image_and_texture_node_group, "衣服", "clothes", "衣服贴图", game, hair_materials, skin_materials, clothes_materials)

    # 追加物体移入选中网格的集合
    if model.users_collection:  # 检查选中模型是否在集合中
        for obj in data_from.objects:
            model.users_collection[0].objects.link(obj)  # 将驱动物体移入新集合

    # 绑定头骨
    bind_bone(prefs, model)

