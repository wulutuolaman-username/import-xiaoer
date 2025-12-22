# coding: utf-8

import os, bpy
from typing import Tuple
from ...通用.信息 import 报告信息
from ...指针 import XiaoerImage

def 获取Ramp贴图(self, 游戏, 基础贴图:XiaoerImage) -> XiaoerImage|None|Tuple[XiaoerImage|None, XiaoerImage|None]:
    if 基础贴图.小二预设模板.类型:
        前缀 = 基础贴图.小二预设模板.前缀
        部件 = 基础贴图.小二预设模板.部件
        类型 = 基础贴图.小二预设模板.类型
        名称, 扩展 = os.path.splitext(os.path.basename(基础贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
###################################################################################################
        if 游戏 == "原神":
            Ramp = "Shadow_Ramp"
            # 优先严格匹配贴图名称
            新名 = 名称.replace(类型, Ramp)
            # 报告信息(self, '正常', f'基础贴图“{名称}”尝试搜索ramp贴图“{新名}')
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if f"_{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(Ramp.lower()):
                    报告信息(self, '正常', f'基础贴图“{基础贴图.name}”宽松匹配找到可能的ramp贴图“{贴图.name}')
                    return 贴图
            if 部件 and 部件[-1].isdigit():
                部件 = 部件[:-1]
            for 贴图 in bpy.data.images:  # type:XiaoerImage
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                # 如果基础贴图部件为Body1、Body2，而ramp贴图部件为Body，去掉部件的数字
                if f"_{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(Ramp.lower()):
                    报告信息(self, '正常', f'基础贴图“{基础贴图.name}”宽松匹配找到可能的ramp贴图“{贴图.name}')
                    return 贴图
            return None
###################################################################################################
        if 游戏 == "崩坏：星穹铁道":
            def 崩铁Ramp(冷, 暖):
                冷图 = None
                暖图 = None
                # 报告信息(self, '正常', f"{暖}\n{冷}")
                for 贴图 in bpy.data.images:  # type:XiaoerImage
                    名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                    # if "Ramp" in 名:
                    #     报告信息(self, '正常', f"{名} {名 == 冷} {名 == 暖}")
                    if 名 == 冷:
                        冷图 = 贴图
                    if 名 == 暖:
                        暖图 = 贴图
                return 冷图, 暖图

            # 定义所有可能的查找模式
            查找模式 = [
                # (前缀, 部件) 的格式
                (前缀, 部件),  # 第一次尝试：完整名称
                (前缀, 部件[:-1] if 部件 and 部件[-1].isdigit() else None),  # 去掉末尾数字
                (前缀, None),  # 只有前缀  # 萨姆
                (前缀[:-3] if 前缀 and len(前缀) >= 3 and 前缀[-3] == '_' and 前缀[-2].isdigit() else None, None) # 忆灵
                # 去掉前缀末尾数字
            ]

            for 当前前缀, 当前部件 in 查找模式:
                if not 当前前缀:  # 跳过无效的前缀
                    continue

                if 当前部件:
                    冷 = f"{当前前缀}_{当前部件}_Cool_Ramp"
                    暖 = f"{当前前缀}_{当前部件}_Warm_Ramp"
                else:
                    冷 = f"{当前前缀}_Cool_Ramp"
                    暖 = f"{当前前缀}_Warm_Ramp"

                冷图, 暖图 = 崩铁Ramp(冷, 暖)
                # 报告信息(self, '正常', f"{冷图}\n{暖图}")
                if 冷图 or 暖图:
                    return 冷图, 暖图
                else:
                    if 当前部件:
                        暖 = f"{当前前缀}_{当前部件}_Ramp"
                    else:
                        暖 = f"{当前前缀}_Ramp"
                    冷图, 暖图 = 崩铁Ramp(冷, 暖)
                    if 冷图 or 暖图:
                        return 冷图, 暖图
            return None, None
###################################################################################################
