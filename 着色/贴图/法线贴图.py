# coding: utf-8

import bpy
import os
import re
from ...通用.信息 import 报告信息
from .基础贴图 import 筛选鸣潮基础贴图

def 获取法线贴图(self, 游戏, 基础贴图):
    if 基础贴图.小二预设模板.类型:
        前缀 = 基础贴图.小二预设模板.前缀
        部件 = 基础贴图.小二预设模板.部件
        类型 = 基础贴图.小二预设模板.类型
        名称, 扩展 = os.path.splitext(os.path.basename(基础贴图.filepath))  # 分割文件名和扩展名
###################################################################################################
        if 游戏 == "崩坏三":
            法线 = "Normal"
            # 优先严格匹配贴图名称
            新名 = 名称.replace("Color", 法线, 1)
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:
                # 崩坏三宽松匹配检查路径是否相同
                if os.path.dirname(基础贴图.filepath) == os.path.dirname(贴图.filepath):
                    名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                    if f"_{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(法线.lower()):
                        报告信息(self, '正常', f'基础贴图“{基础贴图.name}”宽松匹配找到可能的法线贴图“{贴图.name}')
                        return 贴图
###################################################################################################
        if 游戏 == "原神":
            法线 = "Normalmap"
            # 优先严格匹配贴图名称
            新名 = 名称.replace(类型, 法线)
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if f"_{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith(法线.lower()):
                    报告信息(self, '正常', f'基础贴图“{基础贴图.name}”宽松匹配找到可能的法线贴图“{贴图.name}')
                    return 贴图
###################################################################################################
        if 游戏 == "绝区零":
            新名 = f"{前缀}_{部件}_N"
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    return 贴图
###################################################################################################
        if 游戏 == "鸣潮":
            # 优先严格匹配贴图名称
            新名 = f"{前缀}_{部件}_N"
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if 名.lower() == 新名.lower():  # 忽略大小写
                    return 贴图
            # 1.1.0宽松匹配：只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图
            for 贴图 in bpy.data.images:
                名, 类 = os.path.splitext(os.path.basename(贴图.filepath))  # 分割文件名和扩展名  # 防止名称长度限制
                if f"{部件.rstrip('_')}".lower() in 名.lower() and 名.lower().endswith("_N".lower()) :
                    报告信息(self, '正常', f'基础贴图“{基础贴图.name}”宽松匹配找到可能的法线贴图“{贴图.name}')
                    return 贴图
###################################################################################################
    return None
