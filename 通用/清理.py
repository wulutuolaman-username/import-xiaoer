# coding: utf-8

import bpy

# 清理材质图像
def 清理贴图(节点):
    图像 = 节点.image
    # 检查最后 4 个字符
    if 图像:  #1.0.3更新
        后缀 = 图像.name[-4:]
        if 后缀[0] == '.' and 后缀[1:].isdigit():
            新名 = 图像.name[:-4]
            新图 = bpy.data.images.get(新名)
            if 新图:
                节点.image = 新图
            else:
                节点.image.name = 新名
        # bpy.ops.outliner.orphans_purge()  # 清除孤立数据

# 整理MMD刚体材质
def 清理MMD刚体材质():
    for i, 刚体材质 in enumerate(bpy.data.materials):
        if 刚体材质.name.startswith("mmd_tools_rigid_"):
            if 刚体材质.name[-3:].isdigit():
                新名 = 刚体材质.name[:-4]
                新材质 = bpy.data.materials.get(新名)
                if 新材质:
                    bpy.data.materials[i] = 新材质

# # 整理MMD固有节点组
# def 清理MMD节点组():
#     for i, MMD节点组 in enumerate(bpy.data.node_groups):
#         if MMD节点组.name.startswith("MMDTexUV") or MMD节点组.name.startswith("MMDShaderDev"):
#             if MMD节点组.name[-3:].isdigit():
#                 新名 = MMD节点组.name[:-4]
#                 MMD节点组.name = 新名
#                 # 新节点组 = bpy.data.node_groups.get(新名)
#                 # if 新节点组:
#                 #     MMD节点组.name = 新节点组