import bpy

def toutou_xiaoer(self, model):

    safe_objects = {model}
    # 找到几何节点修改器
    for mod in model.modifiers:
        if mod.type == 'NODES':
            # self.report({'INFO'}, f"几何节点: {mod}")
            for node in mod.node_group.nodes:
                # self.report({'INFO'}, f"遍历节点: {node.type}")
                if node.type == 'OBJECT_INFO' and node.inputs[0].default_value:
                    # self.report({'INFO'}, f"物体节点: {node}")
                    # 找到几何节点中引用的物体
                    safe_objects.add(node.inputs[0].default_value)

    # 清除选中模型以外的物体
    for obj in bpy.data.objects:
        if obj not in safe_objects:
            bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.outliner.orphans_purge(do_recursive=True)  # 递归清理孤立数据（循环直到没有孤立数据）

    # 清除世界
    for world in bpy.data.worlds:
        bpy.data.worlds.remove(world)

    if "Render Result" in bpy.data.images:
        bpy.data.images.remove(bpy.data.images["Render Result"])

    # 清除文本
    for text in bpy.data.texts:
        bpy.data.texts.remove(text)

    if "Dots Stroke" in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials["Dots Stroke"])
    # 材质添加伪用户
    for material in bpy.data.materials:
        if material.users == 0:
            material.use_fake_user = True

    # 清除笔刷
    for brush in bpy.data.brushes:
        bpy.data.brushes.remove(brush)

    # 清除线条样式
    for linestyle in bpy.data.linestyles:
        bpy.data.linestyles.remove(linestyle)

    # 清空网格数据
    bpy.data.meshes.remove(bpy.data.meshes[model.name.replace("_mesh","")])

    # 节点组添加伪用户
    for node_group in bpy.data.node_groups:
        if node_group.users == 0:
            node_group.use_fake_user = True

    # 清除调色板
    for Palette in bpy.data.palettes:
        bpy.data.palettes.remove(Palette)

    # 清除集合
    for collection in list(bpy.data.collections):
        for obj in list(collection.objects):
            collection.objects.unlink(obj)
        bpy.data.collections.remove(collection)

    # 打包外部数据
    bpy.ops.file.autopack_toggle()
