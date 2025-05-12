# coding: utf-8

import bpy

def 获取法线贴图(游戏, 基础贴图):
###################################################################################################
    if 游戏 == "崩坏三":
        if "Color" in 基础贴图.name:
            名称 = 基础贴图.name.replace("Color", "Normal")
            if 名称 in bpy.data.images:
                return bpy.data.images[名称]
            else:
                return None
###################################################################################################
    if 游戏 == "原神":
        try:
            法线贴图 = bpy.data.images[基础贴图.name.replace("Diffuse", "Normalmap")]
            return 法线贴图
        except KeyError as e:
            if "not found" in str(e):
                pass  # 如果已经加载则跳过
            else:
                raise  # 其他错误继续抛出
###################################################################################################
    if 游戏 == "绝区零" or 游戏 == "鸣潮":
        if "_D" in 基础贴图.name:
            名称 = 基础贴图.name.replace("_D", "_N")
            if 名称 in bpy.data.images:
                return bpy.data.images[名称]
            else:
                return None
###################################################################################################