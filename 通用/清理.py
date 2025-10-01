# coding: utf-8

import bpy
from .剪尾 import 剪去后缀
from ..图像.筛选贴图 import 筛选图像

# 清理材质图像
def 清理贴图(self, 图像, 节点, 数据源, 类型=''):
    if 图像 and 筛选图像(图像):  # 1.0.3更新  # 1.1.0必须是通用贴图或解包贴图
        名称, 后缀 = 剪去后缀(图像.name)  # 检查最后 4 个字符
        if 后缀:
            新图 = bpy.data.images.get(名称)
            # 1.1.0分类处理
            if 类型 == 'SHADER':
                # if 新图 and 新图.pixels and 新图.name in 数据源.images:  # 1.1.0必须是预设文件里的贴图
                if 新图 and 新图.pixels:
                    # self.report({'INFO'}, f"{节点}\n{图像.name}替换为{新图.name}")
                    节点.image = 新图
                    if 图像.alpha_mode == 'CHANNEL_PACKED':
                        新图.alpha_mode = 'CHANNEL_PACKED'
                else:
                    # self.report({'INFO'}, f"{节点}\n{图像.name}重命名为{名称}")
                    图像.name = 名称
            if 类型 == 'GEOMETRY':
                输入接口 = next((s for s in 节点.inputs if s.name == 'Image'), None)
                if 输入接口 and 输入接口.default_value:
                    if 新图 and 新图.pixels:
                        # self.report({'INFO'}, f"{节点}\n{图像.name}替换为{新图.name}")
                        输入接口.default_value = 新图  # 描边遮罩
                    else:
                        # self.report({'INFO'}, f"{节点}\n{图像.name}重命名为{名称}")
                        图像.name = 名称

    # bpy.ops.outliner.orphans_purge()  # 清除孤立数据

# 整理MMD刚体材质
def 清理MMD刚体材质():
    for i, 刚体材质 in enumerate(bpy.data.materials):
        if 刚体材质.name.startswith("mmd_tools_rigid_"):
            名称, 后缀 = 剪去后缀(刚体材质.name)
            if 后缀:
                材质 = bpy.data.materials.get(名称)
                if 材质:
                    bpy.data.materials[i] = 材质
                else:
                    刚体材质.name = 名称

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