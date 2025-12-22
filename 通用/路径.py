import os, bpy
from ..着色.贴图.基础贴图 import 筛选贴图
# from ..通用.剪尾 import 剪去后缀

def 获取模型路径(self, 模型):
    if 模型.parent and 模型.parent.parent and 模型.parent.parent.get("import_folder"):  # mmd_tools导入的模型
        return 模型.parent.parent["import_folder"]  # mmd_tools导入模型具有此属性
    else:
        for 材质 in 模型.data.materials:
            原始贴图, 图像节点 = 筛选贴图(self, 材质)
            if 原始贴图 and 原始贴图.source == 'FILE':
                if 原始贴图.filepath:
                    图像路径 = bpy.path.abspath(原始贴图.filepath)  # 转为绝对路径
                    if os.path.exists(图像路径):
                        模型路径 = os.path.dirname(图像路径)
                        if 验证(模型, 模型路径):
                            return 模型路径
                        模型路径 = os.path.dirname(模型路径)# 上一级路径
                        if 验证(模型, 模型路径):
                            return 模型路径
    return None

def 验证(模型, 模型路径):
    for 文件名 in os.listdir(模型路径):
        if 文件名.endswith('.fbx'):
            # if 模型.parent and 模型.parent.type == 'ARMATURE':
            #     名称, 后缀 = 剪去后缀(模型.parent.name)
            #     if 文件名.startswith(名称):
            #         return True
            #     if 模型.parent.parent and 模型.parent.parent.type == 'EMPTY':
            #         名称, 后缀 = 剪去后缀(模型.parent.parent.name)
            #         if 文件名.startswith(名称):
                        return True
        if 文件名.endswith('.pmx'):
            # if 模型.parent and 模型.parent.parent and 模型.parent.parent.type == 'EMPTY':
            #     名称, 后缀 = 剪去后缀(模型.parent.parent.name)
            #     if 文件名.startswith(名称):
                    return True
    return False