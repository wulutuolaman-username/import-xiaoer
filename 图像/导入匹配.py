# coding: utf-8

import bpy
import os
from ..着色.贴图.基础贴图 import 筛选贴图, 筛选基础贴图
from ..图像.哈希 import 哈希图像

# 导入解包贴图，于原神贴图进行哈希匹配
def 导入匹配(self, 偏好, 模型, 贴图路径):
    模型贴图 = []  # 记录原始贴图信息
    alpha贴图 = []  # 记录带有alpha通道的贴图
    原始哈希 = {}
    if 偏好.匹配基础贴图:
        for 材质 in 模型.data.materials:  # 1.0.3修改
            for 图像节点 in 材质.node_tree.nodes:
                if 图像节点.type == 'TEX_IMAGE':
                    图像 = 图像节点.image
                    if 图像 not in 模型贴图 and 筛选贴图(图像.name):
                        # self.report({"INFO"}, f'记录原始贴图“{image.name}”')
                        模型贴图.append(图像)
        # 生成原始贴图的哈希值
        for 图像 in 模型贴图:
            哈希1 ,有alpha = 哈希图像(图像)
            if 哈希1:
                # self.report({"INFO"}, f'成功哈希“{img.name}”')
                原始哈希[图像] = 哈希1
            if 有alpha:  # 如果存在alpha通道
                alpha贴图.append(图像)
    # 导入贴图
    self.report({"INFO"}, f"导入贴图" + str(贴图路径))
    导入贴图 = []
    # 遍历目录下的所有文件
    for 图像名 in os.listdir(贴图路径):
        if 筛选贴图(图像名):
            贴图位置 = os.path.join(贴图路径, 图像名)
            # 导入图像到 Blender
            try:
                图像 = bpy.data.images.load(贴图位置)
                导入贴图.append(图像)
                # self.report({"INFO"}, f"导入成功：" + str(imagename))
            except Exception as e:
                self.report({"WARNING"}, f"导入失败：" + str(图像名))
    if 偏好.匹配基础贴图:  # 如果开启了自动匹配贴图
        匹配贴图 = {}  # 记录原始贴图和解包贴图的匹配信息，后续引用此字典进行匹配
        导入哈希 = {}
        for 图像 in 导入贴图:
            if 筛选基础贴图(图像.name):
                # get_image_hash(img, self)
                哈希2 ,有alpha = 哈希图像(图像)
                if 哈希2 :
                    导入哈希[哈希2] = 图像
                if 有alpha:  # 如果存在alpha通道
                    alpha贴图.append(图像)
        for 原始贴图 in 模型贴图:
            哈希1 = 原始哈希[原始贴图]
            for 哈希2 in 导入哈希:
                导入贴图 = 导入哈希[哈希2]
                self.report({"INFO"}, f'原始贴图“{原始贴图.name}”与导入贴图“{导入贴图.name}”汉明距离: {哈希1 - 哈希2}')
                if 哈希1 - 哈希2 <= 偏好.汉明距离:  # 汉明距离^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    # self.report({"INFO"}, f'成功哈希“{img.name}”')
                    self.report({"INFO"}, f'原始贴图“{原始贴图.name}”匹配贴图“{导入贴图.name}”')
                    匹配贴图[原始贴图] = 导入贴图  # 记录原始贴图和解包贴图的匹配信息，后续引用此字典进行匹配
            if 原始贴图 not in 匹配贴图:  # 如果原始贴图没有匹配到解包贴图
                try:  # 尝试复制已有的匹配
                    原始名称 = 原始贴图.name.replace("+", "")
                    相近贴图 = bpy.data.images[原始名称]
                    基础贴图 = 匹配贴图[相近贴图]
                    self.report({"INFO"}, f'原始贴图“{原始贴图.name}”匹配贴图“{基础贴图.name}”')
                    匹配贴图[原始贴图] = 基础贴图  # 记录原始贴图和解包贴图的匹配信息，后续引用此字典进行匹配
                except:
                    self.report({"WARNING"}, f'原始贴图“{原始贴图.name}”未找到匹配贴图')
                    pass
        # self.report({"INFO"}, f"alpha贴图:\n" + "\n".join(image.name for image in alpha贴图))
        return 匹配贴图,alpha贴图
    else:  # 如果关闭了自动匹配贴图
        return None,None