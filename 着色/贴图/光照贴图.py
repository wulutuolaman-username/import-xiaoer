# coding: utf-8

import os, bpy
from ...通用.剪尾 import 剪去后缀
from ...通用.信息 import 报告信息
from ...指针 import XiaoerImage

def 获取光照贴图(self, 游戏, 基础贴图:XiaoerImage) -> XiaoerImage | None:
    贴图: XiaoerImage
    if 基础贴图.小二预设模板.类型:
        前缀 = 基础贴图.小二预设模板.前缀
        部件 = 基础贴图.小二预设模板.部件
        类型 = 基础贴图.小二预设模板.类型
        名称, 后缀 = 剪去后缀(基础贴图.name)
        if 后缀:  # 如果有副本后缀
            基础贴图.name = 名称
        名称, 扩展 = os.path.splitext(os.path.basename(基础贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
###################################################################################################
        if 游戏 == "崩坏三":
            光照 = "LightMap"
            新名 = 名称.replace("Color", 光照, 1)
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    贴图.小二预设模板.正则类型 = 光照
                    return 贴图
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                if os.path.dirname(基础贴图.filepath) == os.path.dirname(贴图.filepath):  # 崩坏三宽松匹配检查路径是否相同
                    名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                    if f"{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(光照.lower()):
                        报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
                        贴图.小二预设模板.正则类型 = 光照
                        return 贴图
###################################################################################################
        if 游戏 == "原神":
            光照 = "Lightmap"
            # 优先严格匹配贴图名称
            新名 = 名称.replace(类型, 光照)
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    贴图.小二预设模板.正则类型 = 光照
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if f"{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(光照.lower()):
                    报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
                    贴图.小二预设模板.正则类型 = 光照
                    return 贴图
###################################################################################################
        if 游戏 == "崩坏：星穹铁道":
            # 优先严格匹配贴图名称
            类型 = 类型.replace("_A", "")
            类型 = 类型.replace("Color", "LightMap")
            新名 = f"{前缀}_{部件}_{类型}"  # 1.1.0不再只匹配png
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    贴图.小二预设模板.正则类型 = 类型
                    return 贴图
            新名 = f"{前缀}_{类型}"  # 阿格莱雅人台
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    贴图.小二预设模板.正则类型 = 类型
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if f"{部件.rstrip('_')}".lower() in 名.lower() and (名.lower().endswith(f"LightMap".lower()) or 名.lower().endswith(f"LightMap_L".lower())):
                    报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
                    贴图.小二预设模板.正则类型 = 类型
                    return 贴图
###################################################################################################
        if 游戏 == "绝区零":
            新名 = f"{前缀}_{部件}_M"
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    return 贴图
###################################################################################################
        if 游戏 == "鸣潮":
            # 优先严格匹配贴图名称
            光照类型 = ["HM", "ID", "VC", "M"]# 1.1.0增加多个鸣潮贴图关键词检测
            for 光照 in 光照类型:
                for 贴图 in bpy.data.images:  # type:XiaoerImage
                    新名 = f"{前缀}_{部件}_{光照}"
                    名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                    if 名.lower() == 新名.lower():  # 忽略大小写
                        贴图.小二预设模板.正则类型 = 光照
                        return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                for 光照 in 光照类型:
                    if f"{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(f"{光照}".lower()) :
                        报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
                        贴图.小二预设模板.正则类型 = 光照
                        return 贴图
###################################################################################################

###################################################################################################
    return None