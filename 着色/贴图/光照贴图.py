# coding: utf-8

import bpy
import re

def 获取光照贴图(游戏, 基础贴图):
    if 基础贴图.name[-3:].isdigit():  # 如果有副本后缀
        基础贴图.name = 基础贴图.name[:-4]
###################################################################################################
    if 游戏 == "崩坏三":
        if "Color" in 基础贴图.name:
            名称 = 基础贴图.name.replace("Color", "LightMap")
            for 贴图 in bpy.data.images:
                if 贴图.name.lower() == 名称.lower():  # 忽略大小写
                    return 贴图
###################################################################################################
    if 游戏 == "原神":
        if "Diffuse" in 基础贴图.name:
            贴图 = bpy.data.images[基础贴图.name.replace("Diffuse", "Lightmap")]
            return 贴图
        else:
            return None
###################################################################################################
    if 游戏 == "崩坏：星穹铁道":
        # 新正则表达式结构说明：
        # ^(.*_\d{2})_       -> 前缀包含两位数字 (如 Avatar_Fugue_00)
        # ([^_]+)            -> 部件类型 (Body/Hair/Tail等)
        # _Color(.*)\.png$   -> Color及其后缀
        分解 = re.match(r'^(.*_\d{2})_([^_]+)_Color(.*)\.png$', 基础贴图.name)
        if 分解:
            前缀, 部件, 后缀 = 分解.groups()
            # 处理LightMap后缀：仅当Color后缀以_L结尾时保留
            分割 = [p for p in 后缀.split('_') if p]  # 以 _ 分割后缀字符串，并去掉空字符串项
            末尾 = 分割[-1] if 分割 else ''
            名尾 = f"_{末尾}" if 末尾 == 'L' else ''
            名称 = f"{前缀}_{部件}_LightMap{名尾}.png"
            for 贴图 in bpy.data.images:
                if 贴图.name.lower() == 名称.lower():  # 忽略大小写
                    return 贴图
        else:  # 可能不是角色贴图
            if "Color" in 基础贴图.name:
                名称 = 基础贴图.name.replace("Color", "LightMap")
                for 贴图 in bpy.data.images:
                    if 贴图.name.lower() == 名称.lower():  # 忽略大小写
                        return 贴图
            else:
                return None
###################################################################################################
    if 游戏 == "绝区零":
        if "_D" in 基础贴图.name:
            贴图 = bpy.data.images[基础贴图.name.replace("_D", "_M")]
            return 贴图
        else:
            return None
###################################################################################################
    if 游戏 == "鸣潮":
        if "_D" in 基础贴图.name:
            # 从前截到_D，从后截到.png
            分解 = re.compile(r"^(.*_D).*?(\.png)$").search(基础贴图.name)
            if 分解:
                基础名称 = 分解.group(1) + 分解.group(2)
                贴图 = (
                        bpy.data.images.get(基础名称.replace("_D", "_HM")) or
                        bpy.data.images.get(基础名称.replace("_D", "_ID")) or
                        bpy.data.images.get(基础名称.replace("_D", "_VC")) or
                        bpy.data.images.get(基础名称.replace("_D", "_M"))
                                  )
                return 贴图
            else:
                return None
###################################################################################################
