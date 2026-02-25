# coding: utf-8

import os, re, bpy  # noqa: F401
from typing import Tuple
from ...通用.信息 import 报告信息
from ...指针 import *

def 过滤贴图(图像名称):
    """ 过滤掉模型贴图中的非基础色贴图 """
    名称, 扩展 = os.path.splitext(图像名称)
    排除贴图 = ["黑"]
    排除关键词 = ["焰", "hi.", "spa", "sph", "xing", "声痕"]
    排除前缀 = ["bq", "mc", "sh", "sp", "emo", "stk", "表情", "gold", "toon", "spa_h", "hair_s"]
    return (
            not any(词 == 名称 for 词 in 排除贴图) and
            not any(词 in 名称 for 词 in 排除关键词) and
            not any(名称.startswith(前) for 前 in 排除前缀) and
            not (名称.isdigit())  # 不能只包含数字
            )

def 筛选贴图(self, 材质:小二材质) -> Tuple[小二贴图 | None, 小二节点 | None]:
    """ 找到材质中的基础贴图节点 """
    # 1.1.0更改贴图匹配逻辑，增强筛选过滤
    if 材质.node_tree:
        for 节点 in 材质.node_tree.nodes:  # type:小二节点
            if 节点.判断类型.节点.是群组:
                if 节点.inputs:
                    接口 = 节点.inputs[0]  # type:小二对象|bpy.types.NodeSocket
                    if 接口.判断类型.接口.是颜色 and 接口.is_linked:
                        节点 = 接口.links[0].from_node  # type:小二节点
                        if 节点.判断类型.节点.着色.是图像:
                            贴图 = 节点.image  # type:ignore
                            if 贴图:
                                return 贴图, 节点
        for 节点 in sorted(材质.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # type:小二节点
            # self.report({"INFO"}, f'材质Material["{材质.name}"]图像节点["{图像节点.name}"]类型["{图像节点.type}')
            if 节点.判断类型.节点.着色.是图像:
                # self.report({"INFO"}, f'材质Material["{材质.name}"]图像节点{图像节点.name}')
                贴图 = 节点.image  # type:ignore
                if 贴图:
                    # self.report({"INFO"}, f'材质Material["{材质.name}"]可能贴图{原始贴图.name}')
                    名称 = 贴图.name.lower()  # 统一小写
                    if 过滤贴图(名称):
                        # self.report({"INFO"}, f'材质Material["{材质.name}"]原始贴图{原始贴图.name}')
                        return 贴图, 节点
                    return None, 节点
        报告信息(self, '异常', f'材质Material["{材质.name}"]未找到图像节点 type == "TEX_IMAGE"')
    return None, None

def 筛选基础贴图(游戏, 图像:小二贴图) -> bool:
    """ 筛选出解包贴图中的基础贴图 """
    # 1.0.3迁移：筛选基础贴图  # 1.1.0加强筛选
    分解 = None
    名称 = os.path.splitext(os.path.basename(图像.filepath))[0]  # 防止名称长度限制
    if 游戏 == "崩坏三":  # 崩坏三基础贴图
        # noinspection RegExpUnnecessaryNonCapturingGroup
        分解 = re.match(r'^(.+(?=_Body)|.+(?=_Hair)|.+(?=_Face)|.+(?=_Weapon)|.+(?:Texture(?!_Color))|.+\d\d_\d\d(?:_[A-Z]{1,2})?|.+C\d(?:_[A-Z][A-Z])?|.+(?:_[A-Z1-9][A-Za-z])|[^_\n]+(?:_[^_\n]+)?)(?!_C\d)(?!_\d_)(?!_Color.+)(?<![^_\n]\d\d)_'
                              r'((?:[^_\n]+)?(?:_[^_\n]+)*)_?'
                              r'(?<!Color_)(?<!Texture_)(?<!LightMap_)(Texture_Color(?!Mask)(?!mask).*|Color(?!Mask)(?!mask).*)$', 名称)
    if 游戏 == "原神":  # 原神基础贴图
        分解 = re.match(r'^(.+_Tex|.+(?!_Diffuse))_([^_\n]*)_?(Diffuse)$', 名称)
    if 游戏 == "崩坏：星穹铁道":  # 崩坏：星穹铁道基础贴图
        分解 = re.match(r'^((?!Eff)(?:[^_\n]+_){2,3}[A-Z0-9]\d)_(?:([^\n]+)_)?(Color(?:_[A-Z])*)$', 名称)
    if 游戏 == "绝区零":  # 绝区零基础贴图
        分解 = re.match(r'^(.+(?=_Body)|.+(?=_Hair)|.+(?=_Face)|.+(?=_Weapon)|.+(?!_Map)|.+(?!_\d))_(?!\d)(.+)_(D)$', 名称)
    if 游戏 == "鸣潮":  # 鸣潮基础贴图
        分解 = re.match(r'^((?:(?:T_)?(?:[^_\n]+0011|[^_\n]+(?=[A-Z][a-z]+\d*)))?|.*)_?'
                              r'(.+)(?<!spa)(?<!toon)(?<!Star)(?<!Nosi)(?<!Noise)_'
                              r'(Cloth|D|LD|Metal|skin)$', 名称)
    if 分解:
        前缀, 部件, 类型 = 分解.groups()
        if 类型:
            if 前缀:
                图像.小二预设模板.正则前缀 = 前缀
            if 部件:
                图像.小二预设模板.正则部件 = 部件
            图像.小二预设模板.正则类型 = 类型
            return True
    return False

鸣潮基础贴图 = ["_Cloth", "_D", "_LD", "_Metal", "_skin"]  # 1.1.0增加多个鸣潮贴图关键词检测
def 筛选鸣潮基础贴图(名称):
    for 基 in 鸣潮基础贴图:
        if 名称.endswith(基):
            return 基, 鸣潮基础贴图
    return None, 鸣潮基础贴图

def 匹配基础贴图(self, 材质:小二材质, 游戏) ->  Tuple[小二节点 | None, 小二贴图 | None]:
    """ 获取材质的原始贴图节点和原始贴图匹配的基础贴图 """
    原始贴图, 图像节点 = 筛选贴图(self, 材质)  # 获取原始贴图
    # 1.0.3改进
    if not 原始贴图:
        if 图像节点:
            return 图像节点, None
        else:
            报告信息(self, '异常', f'材质Material["{材质.name}"]无图像节点')
            return None, None  # 薇塔的眼睛2材质没有基础贴图
    if 筛选基础贴图(游戏, 原始贴图):
        # 报告信息(self, '异常', f'材质Material["{材质.name}"] 1')
        基础贴图 = 原始贴图
    elif 材质.小二预设模板.基础贴图 and 材质.小二预设模板.完成匹配基础贴图:
        # 报告信息(self, '异常', f'材质Material["{材质.name}"] 2')
        # 报告信息(self, '异常', f'材质Material["{材质.name}"] {材质.小二预设模板.基础贴图} {材质.小二预设模板.完成匹配基础贴图}')
        基础贴图 = 材质.小二预设模板.基础贴图
    else:
        # 报告信息(self, '异常', f'材质Material["{材质.name}"] 3')
        基础贴图 = 原始贴图.小二预设模板.匹配贴图  # 匹配基础色贴图
    if 基础贴图:
        材质.小二预设模板.基础贴图 = 基础贴图
        材质.小二预设模板.完成匹配基础贴图 = True
    else:
        基础贴图 = 原始贴图  # 如果没有匹配贴图，那就直接使用原始贴图
        if not 筛选基础贴图(游戏, 基础贴图):
            if not 过滤贴图(基础贴图.name):
                报告信息(self, '异常', f'材质Material["{材质.name}"]的模型贴图{原始贴图.name}未找到匹配的基础贴图')
    return 图像节点, 基础贴图