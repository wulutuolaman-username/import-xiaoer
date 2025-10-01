# coding: utf-8

import bpy
import os
import re
from ...通用.剪尾 import 剪去后缀
from ...通用.信息 import 报告信息
from ...图像.像素处理 import 获取像素
from ...图像.哈希计算 import 哈希图像
from .基础贴图 import 筛选基础贴图, 筛选鸣潮基础贴图

哈希缓存 = {}

def 获取光照贴图(self, 游戏, 基础贴图, 重新匹配=False):
    # global 哈希缓存  # 全局记录缓存
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
            # 优先严格匹配贴图名称
            新名 = 名称.replace("Color", 光照, 1)
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    贴图.小二预设模板.正则类型 = 光照
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            # 前缀, 部件 = re.match(r'^(.*)_([^_]+)_Color$', 名称).groups()
            for 贴图 in bpy.data.images:
                # 崩坏三宽松匹配检查路径是否相同
                if os.path.dirname(基础贴图.filepath) == os.path.dirname(贴图.filepath):
                    名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                    if f"{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(光照.lower()):
                        报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
                        贴图.小二预设模板.正则类型 = 光照
                        return 贴图
            # for 贴图 in bpy.data.images:
            #     名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
            #     if f"{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(光照.lower()):
            #         报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
            #         贴图.小二预设模板.正则类型 = 光照
            #         return 贴图
        # else:
        #     self.report({"WARNING"}, f'基础贴图["{基础贴图.name}"]名称后缀非（崩坏三）"Color"')
###################################################################################################
        if 游戏 == "原神":
            光照 = "Lightmap"
            # 优先严格匹配贴图名称
            新名 = 名称.replace(类型, 光照)
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    贴图.小二预设模板.正则类型 = 光照
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if f"{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(光照.lower()):
                    报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
                    贴图.小二预设模板.正则类型 = 光照
                    return 贴图
        # else:
        #     self.report({"WARNING"}, f'基础贴图["{名称}"]名称后缀非（原神）"Diffuse"')
###################################################################################################
        if 游戏 == "崩坏：星穹铁道":
            # 优先严格匹配贴图名称
            类型 = 类型.replace("_A", "")
            类型 = 类型.replace("Color", "LightMap")
            新名 = f"{前缀}_{部件}_{类型}"  # 1.1.0不再只匹配png
            # if 新名 not in bpy.data.images:  # 阿格莱雅人台
            #     新名 = f"{前缀}_{类型}"
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    贴图.小二预设模板.正则类型 = 类型
                    return 贴图
            新名 = f"{前缀}_{类型}"  # 阿格莱雅人台
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    贴图.小二预设模板.正则类型 = 类型
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if f"{部件.rstrip('_')}".lower() in 名.lower() and (名.lower().endswith(f"LightMap".lower()) or 名.lower().endswith(f"LightMap_L".lower())):
                    报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
                    贴图.小二预设模板.正则类型 = 类型
                    return 贴图
            # else:  # 可能不是角色贴图
            #     if 名称.endswith("Color"):
            #         # 优先严格匹配贴图名称
            #         新名 = 名称.replace("Color", "LightMap") + 扩展
            #         for 贴图 in bpy.data.images:
            #             if 贴图.name.lower() == 新名.lower():  # 忽略大小写
            #                 return 贴图
            #         # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            #         前缀, 部件 = re.match(r'^(.*)_([^_]+)_Color$', 名称).groups()
            #         for 贴图 in bpy.data.images:
            #             名, 类 = os.path.splitext(贴图.name)  # 分割文件名和扩展名
            #             if f"{部件.rstrip('_')}".lower() in 名.lower() and (名.lower().endswith(f"LightMap".lower()) or 名.lower().endswith(f"LightMap_L".lower())):
            #                 self.report({"INFO"}, f'基础贴图“{基础贴图.name}”宽松匹配找到可能的光照贴图“{贴图.name}')
            #                 return 贴图
                # else:
                #     self.report({"WARNING"}, f'基础贴图["{基础贴图.name}"]名称后缀非（崩坏：星穹铁道）"Color(_A)(_L)"')
###################################################################################################
        if 游戏 == "绝区零":
            新名 = f"{前缀}_{部件}_M"
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    return 贴图
        # else:
        #     self.report({"WARNING"}, f'基础贴图["{名称}"]名称后缀非（绝区零）"D"')
###################################################################################################
        if 游戏 == "鸣潮":
            # 优先严格匹配贴图名称
            光照类型 = ["HM", "ID", "VC", "M"]
            for 光照 in 光照类型:  # 1.1.0增加多个鸣潮贴图关键词检测
                for 贴图 in bpy.data.images:
                    新名 = f"{前缀}_{部件}_{光照}"
                    名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                    if 名.lower() == 新名.lower():  # 忽略大小写
                        贴图.小二预设模板.正则类型 = 光照
                        return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                for 光照 in 光照类型:
                    if f"{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(f"{光照}".lower()) :
                        报告信息(self, '正常', f'基础贴图“{名称}”宽松匹配找到可能的光照贴图“{贴图.name}')
                        贴图.小二预设模板.正则类型 = 光照
                        return 贴图
        # else:
        #     self.report({"WARNING"}, f'基础贴图["{名称}"]名称后缀非（鸣潮）' + " ".join(基.rstrip('_') for 基 in 基础))
        #     # 1.1.0没有找到对应的光照贴图，尝试重新匹配基础贴图
        #     if not 重新匹配:
        #         self.report({"WARNING"}, f'基础贴图["{基础贴图.name}"]未找到匹配的光照贴图，重新匹配近似的基础贴图')
        #         像素 = 获取像素(self, 基础贴图)
        #         哈希1 = 哈希图像(self, 基础贴图, 像素)
        #         if not 哈希缓存:  # 首次重新匹配计算哈希
        #             for 图像 in bpy.data.images:
        #                 if 筛选基础贴图(图像.name):
        #                     像素 = 获取像素(self, 图像)
        #                     哈希2 = 哈希图像(self, 基础贴图, 像素)
        #                     哈希缓存[哈希2] = 图像
        #         汉明距离 = {}  # 1.1.0匹配汉明距离最小的贴图
        #         for 哈希2 in 哈希缓存:
        #             图像 = 哈希缓存[哈希2]
        #             汉明距离[哈希1 - 哈希2] = 图像
        #             self.report({"INFO"}, f'基础贴图“{基础贴图.name}”与贴图“{图像.name}”汉明距离: {哈希1 - 哈希2}')
        #         最小值 = min(汉明距离)  # 1.1.0匹配汉明距离最小的贴图
        #         近似贴图 = 汉明距离[最小值]
        #         self.report({"INFO"}, f'基础贴图“{基础贴图.name}”近似的基础贴图“{近似贴图.name}”')
        #         return 获取光照贴图(self, 游戏, 近似贴图, 重新匹配=True)
###################################################################################################

###################################################################################################
    return None