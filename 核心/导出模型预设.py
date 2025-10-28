# coding: utf-8

import bpy
import os

def 透透小二(self, 模型, 保存路径):

    保护 = {模型}
    骨架 = 模型.parent
    def 递归(骨架):
        if 骨架.小二预设模板.加载完成 or 骨架.小二预设模型.导入完成:
            if 骨架.小二预设模板.加载完成:
                骨架.小二预设模板.加载完成 = False
            if 骨架.小二预设模型.导入完成:
                骨架.小二预设模型.导入完成 = False
            for 物体 in 骨架.children:
                if 模型.type == 'MESH' and not 模型.rigid_body:  # 排除面部定位和刚体
                    保护.add(物体)
                elif 模型.children:
                    for 物体 in 模型.children:
                        递归(物体)
            if 骨架.parent:
                递归(骨架.parent)
    # if 骨架 and 骨架.type == 'ARMATURE' and len([物体 for 物体 in 骨架.children if 物体.type == 'MESH']) > 1:
    if 骨架:
        # for 物体 in 骨架.children:
        #     if 物体.type == 'MESH':  # 面部定位
        #         保护.add(物体)
        递归(骨架)
    附加 = set()
    # 找到几何节点修改器
    def 几何节点修改器(模型):
        for 修改器 in 模型.modifiers:
            if 修改器.type == 'NODES':
                # self.report({'INFO'}, f"几何节点: {mod}")
                if 修改器.node_group:
                    修改器.node_group.小二预设模板.应用修改器 = False
                    for 节点 in 修改器.node_group.nodes:
                        # self.report({'INFO'}, f"遍历节点: {node.type}")
                        if 节点.type == 'OBJECT_INFO' and 节点.inputs[0].default_value:
                            # self.report({'INFO'}, f"物体节点: {node}")
                            # 找到几何节点中引用的物体
                            附加.add(节点.inputs[0].default_value)
    for 物体 in 保护:
        if 物体.type == 'MESH':
            几何节点修改器(物体)
    保护.update(附加)
    # 清除选中模型以外的物体
    for 物体 in bpy.data.objects:
        if 物体 not in 保护:
            bpy.data.objects.remove(物体, do_unlink=True)

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
    # # 材质添加伪用户
    # for 材质 in bpy.data.materials:
    #     if 材质.users == 0:
    #         材质.use_fake_user = True

    # 清除笔刷
    for 笔刷 in bpy.data.brushes:
        bpy.data.brushes.remove(笔刷)

    # 清除线条样式
    for 线条 in bpy.data.linestyles:
        bpy.data.linestyles.remove(线条)

    # 清空网格数据
    网格数量 = len([物体 for 物体 in 保护 if 物体.type == 'MESH'])
    if 网格数量 == 1:
        bpy.data.meshes.remove(bpy.data.meshes[模型.name.replace("_mesh", "")])
    elif 网格数量 > 1:  # 1.1.0fbx模型分离
        for 物体 in 保护:
            if 物体.type == 'MESH':
                bpy.data.meshes.remove(bpy.data.meshes[物体.name.replace("_mesh", "")])

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

    # 1.1.0逐个打包生成贴图
    for 贴图 in bpy.data.images:
        try:
            # if 贴图:
            #     self.report({'INFO'}, f"={贴图.name} {贴图.source} {贴图.is_dirty}")
            if 贴图 and 贴图.source == 'FILE' and not 贴图.packed_file:
                绝对路径 = bpy.path.abspath(贴图.filepath)
                if os.path.exists(绝对路径):
                    try:
                        贴图.pack()
                    except Exception as e:
                        self.report({'ERROR'}, f"打包贴图{贴图.name}出现问题: {e}")
                else:
                    self.report({'ERROR'}, f"{贴图.name}找不到本地路径{绝对路径}")
                    bpy.data.images.remove(贴图)
            # if 贴图 and 贴图.source == 'GENERATED' and 贴图.is_dirty:
                # 贴图.update()  # 🔥 关键步骤
                贴图.pack()
        except ReferenceError:
            pass  # 跳过已删除的贴图
    try:
        bpy.ops.file.autopack_toggle()
    except Exception as e:
        self.report({'ERROR'}, f"自动打包出现问题: {e}")

    # 1.1.0最后保存
    # 执行保存操作
    bpy.ops.wm.save_as_mainfile(
        filepath=保存路径,
        check_existing=True,  # 检查文件存在
        copy=True  # 保持原文件不受影响
    )
    self.report({"OPERATOR"}, f"导出预设: {保存路径}")