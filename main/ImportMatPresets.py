import bpy
from ..general.Setting import Setting_blend
from ..GEOMETRY.GEOMETRY_modifier import GEOMETRY_modifier
from ..general.clean import clean_material_image
from ..image.asset_image import check_material_image_name
from ..general.bind_bone import bind_bone

def chaofei_xiaoer(prefs,model,file_path,file_name,self):
    self.report({"INFO"}, f"导入预设" + str(file_path))
    # 追加预设文件的所有资产
    with bpy.data.libraries.load(file_path) as (data_from, data_to):
        for attr in dir(data_to):
            setattr(data_to, attr, getattr(data_from, attr))

    # 设置辉光属性和色彩管理
    Setting_blend()

    # 应用几何节点
    for node_group in data_from.node_groups:
        if node_group.type == 'GEOMETRY' and node_group.users == 0:  # 未被使用的几何节点组
            GEOMETRY_modifier(model, node_group)  # 应用几何节点
            if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
                for node_level_1 in node_group.nodes:
                    if node_level_1.type == 'GROUP':
                        for node_level_2 in node_level_1.node_tree.nodes:
                            if node_level_2.type == 'GROUP':
                                for image_node in node_level_2.node_tree.nodes:
                                    if image_node.name.startswith("Image Texture"):  # 查找图像纹理节点:
                                        input_socket = next((s for s in image_node.inputs if s.name == 'Image'), None)
                                        if input_socket and input_socket.default_value:
                                            edge_image = input_socket.default_value
                                            edge_image.name = f"{edge_image.name}_{file_name}"  # 描边遮罩重命名
        if node_group.name.startswith("MMDTexUV") or node_group.name.startswith("MMDShaderDev"):
            continue  # 如果是MMD固有节点组，无需后续重命名
        if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
            node_group.name = f"{node_group.name}_{file_name}"  # 节点组重命名

    if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
        # 将模型相关物体移入独立集合
        new_collection = bpy.data.collections.new(file_name)  # 新建独立集合
        bpy.context.scene.collection.children.link(new_collection)  # 关联到场景集合
        for coll in model.parent.parent.users_collection:
            coll.objects.unlink(model.parent.parent)  # 祖父级空物体移出旧集合
        new_collection.objects.link(model.parent.parent)  # 祖父级空物体移入新集合
        for child_1 in model.parent.parent.children:
            for coll in child_1.users_collection:
                coll.objects.unlink(child_1)  # 祖父级空物体的子级全部移出旧集合
            new_collection.objects.link(child_1)  # 祖父级空物体的子级全部移入新集合
            if child_1.name.startswith(file_name):  # 如果是刚体和关节的父级空物体
                pass
            else:
                if child_1.name[-3:].isdigit():  # 如果有副本后缀
                    child_1.name = child_1.name[:-4]  # 剪去后缀
                if model.name.replace("_mesh","") not in child_1.name:
                    child_1.name = f"{child_1.name}_{file_name}"  # 祖父级空物体的子级物体重命名
            for child_2 in child_1.children:
                for coll in child_2.users_collection:
                    if child_2.name[-3:].isdigit():  # 如果有副本后缀
                        child_2.name = child_2.name[:-4]  # 剪去后缀
                        child_2.name = f"{child_2.name}_{file_name}"  # 祖父级空物体的孙级物体重命名
                    coll.objects.unlink(child_2)  # 祖父级空物体的孙级全部移出旧集合
                new_collection.objects.link(child_2)  # 祖父级空物体的孙级全部移入新集合
                if child_2 is not model:
                    child_2.name = f"{child_2.name}_{file_name}"  # 祖父级空物体的孙级物体重命名

    # 追加物体移入选中网格的集合
    if model.users_collection:  # 检查选中模型是否在集合中
        for obj in data_from.objects:
            model.users_collection[0].objects.link(obj)  # 将驱动物体移入新集合

    # 替换网格材质
    for i, old_material in enumerate(model.data.materials):  # 在网格中遍历旧材质
        if old_material:
            for material in data_from.materials:  # 在追加材质中遍历新材质
                new_name = material.name
                if material and material.name[-3:].isdigit():  # 追加材质可能有后缀.001
                    new_name = material.name[:-4]
                new_material = material  # 获取新材质
                if old_material.name == new_name or  old_material.name[:-4] == new_name: # 匹配材质名称
                    model.data.materials[i] = new_material  # 替换材质
                    new_material.name = new_name  # 应用材质原名称
                    if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
                        new_material.name = f"{new_material.name}_{file_name}"  # 网格材质重命名
    # 替换MMD变形材质
    for morph in model.parent.parent.mmd_root.material_morphs:
        for data in morph.data:
            if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
                data.material = f"{data.material[:-4]}_{file_name}"  # 应用材质原名称后，旧材质名称出现后缀，通过减去后缀名称替换MMD变形材质
            else:
                data.material = data.material[:-4]  # 应用材质原名称后，旧材质名称出现后缀，通过减去后缀名称替换MMD变形材质
    bpy.ops.outliner.orphans_purge()  # 清除孤立数据

    # 材质图像重命名
    renamed_image = set()
    def rename_material_image(prefs, node, file_name):
        if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
            image = node.image
            if image not in renamed_image:
                renamed_image.add(image)
                if check_material_image_name(image):
                    pass
                else:
                    image.name = f"{image.name}_{file_name}"  # 材质图像重命名

    # 清理材质图像
    for material in model.data.materials:
        if material.node_tree:
            for node_level_1 in material.node_tree.nodes:
                if node_level_1.type == 'TEX_IMAGE':
                    clean_material_image(node_level_1)
                    rename_material_image(prefs, node_level_1, file_name)
                if node_level_1.type == 'GROUP':
                    for node_level_2 in node_level_1.node_tree.nodes:
                        if node_level_2.type == 'TEX_IMAGE':
                            clean_material_image(node_level_2)
                            rename_material_image(prefs, node_level_2, file_name)
                        if node_level_2.type == 'GROUP':
                            for node_level_3 in node_level_2.node_tree.nodes:
                                if node_level_3.type == 'TEX_IMAGE':
                                    clean_material_image(node_level_3)
                                    rename_material_image(prefs, node_level_3, file_name)
                                if node_level_3.type == 'GROUP':
                                    for node_level_4 in node_level_3.node_tree.nodes:
                                        if node_level_4.type == 'TEX_IMAGE':
                                            clean_material_image(node_level_4)
                                            rename_material_image(prefs, node_level_4, file_name)
                                        if node_level_4.type == 'GROUP':
                                            for node_level_5 in node_level_4.node_tree.nodes:
                                                if node_level_5.type == 'TEX_IMAGE':
                                                    clean_material_image(node_level_5)
                                                    rename_material_image(prefs, node_level_5, file_name)
                    # 清理MMD固有节点组
                    if node_level_1.node_tree.name.startswith("MMDTexUV") or node_level_1.node_tree.name.startswith("MMDShaderDev"):
                        if node_level_1.node_tree.name[-3:].isdigit():
                            new_name = node_level_1.node_tree.name[:-4]
                            new_node_group = bpy.data.node_groups.get(new_name)
                            if new_node_group:
                                node_level_1.node_tree = new_node_group
                            else:
                                node_level_1.node_tree.name = new_name
    bpy.ops.outliner.orphans_purge()  # 清除孤立数据

    # 绑定头骨
    bind_bone(prefs, model)  # 必须在关联集合后

    if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
        for material in data_from.materials:
            if material.name not in model.data.materials:
                material.name = f"{material.name}_{file_name}"  # 描边材质重命名
        # for image in data_from.images:
        #     if check_material_image_name(image):
        #         continue
        #     image.name = f"{image.name}_{file_name}"  # 图像重命名  # 在清理材质图像时改变了属性，所以不可用
        for obj in data_from.objects:
            obj.name = f"{obj.name}_{file_name}"  # 驱动物体重命名
            if obj.type == "LIGHT":
                obj.data.name = f"{obj.data.name}_{file_name}"  # 虚拟灯光数据块重命名
        if model.data.shape_keys:
            if model.data.shape_keys.name[-3:].isdigit():
                model.data.shape_keys.name = model.data.shape_keys.name[:-4]
            model.data.shape_keys.name = f"{model.data.shape_keys.name}_{file_name}"  # 形态键重命名