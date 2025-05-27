# coding: utf-8

import bpy

def 透透小二(self, 模型):

    保护 = {模型}
    # 找到几何节点修改器
    for 修改器 in 模型.modifiers:
        if 修改器.type == 'NODES':
            # self.report({'INFO'}, f"几何节点: {mod}")
            for 节点 in 修改器.node_group.nodes:
                # self.report({'INFO'}, f"遍历节点: {node.type}")
                if 节点.type == 'OBJECT_INFO' and 节点.inputs[0].default_value:
                    # self.report({'INFO'}, f"物体节点: {node}")
                    # 找到几何节点中引用的物体
                    保护.add(节点.inputs[0].default_value)

    # 清除选中模型以外的物体
    for 物 in bpy.data.objects:
        if 物 not in 保护:
            bpy.data.objects.remove(物, do_unlink=True)

    bpy.ops.outliner.orphans_purge(do_recursive=True)  # 递归清理孤立数据（循环直到没有孤立数据）

    # 清除世界
    for 世界 in bpy.data.worlds:
        bpy.data.worlds.remove(世界)

    if "Render Result" in bpy.data.images:
        bpy.data.images.remove(bpy.data.images["Render Result"])

    # 清除文本
    for 文本 in bpy.data.texts:
        bpy.data.texts.remove(文本)

    if "Dots Stroke" in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials["Dots Stroke"])
    # 材质添加伪用户
    for 材质 in bpy.data.materials:
        if 材质.users == 0:
            材质.use_fake_user = True

    # 清除笔刷
    for 笔刷 in bpy.data.brushes:
        bpy.data.brushes.remove(笔刷)

    # 清除线条样式
    for 线条 in bpy.data.linestyles:
        bpy.data.linestyles.remove(线条)

    # 清空网格数据
    bpy.data.meshes.remove(bpy.data.meshes[模型.name.replace("_mesh", "")])

    # 节点组添加伪用户
    for 节点组 in bpy.data.node_groups:
        if 节点组.users == 0:
            节点组.use_fake_user = True
    # 1.0.8材质添加伪用户
    for 材质 in bpy.data.materials:
        if 材质.users == 0:
            材质.use_fake_user = True

    # 清除调色板
    for 调色板 in bpy.data.palettes:
        bpy.data.palettes.remove(调色板)

    # 清除集合
    for 集合 in list(bpy.data.collections):
        for 物 in list(集合.objects):
            集合.objects.unlink(物)
        bpy.data.collections.remove(集合)

    # 打包外部数据
    bpy.ops.file.autopack_toggle()