import os
import bpy
import numpy as np
from .匹配贴图 import 匹配模型贴图和导入贴图
from ..像素处理 import 检查透明
from ...着色.贴图.光照贴图 import 获取光照贴图

global Image  #  1.0.1更新：不再直接导入PIL
try:
    from PIL import Image
except ImportError:
    pass

分割贴图 = []

def 尝试匹配分割贴图(self, 偏好, 模型, 游戏, 模型贴图, 基础贴图, 原始贴图, 原始名称, 贴图路径, 透明贴图):
    for 贴图, 名称 in 模型贴图:
        if 名称 == 原始名称:
            目标贴图 = 贴图
            if not 分割贴图:
                for 贴图, 名称 in 基础贴图:
                    宽度, 高度 = 贴图.size
                    图像 = bpy.data.images[名称]
                    前缀 = 图像.小二预设模板.前缀
                    部件 = 图像.小二预设模板.部件
                    类型 = 图像.小二预设模板.类型
                    扩展 = os.path.splitext(名称)[1]
                    if 宽度 / 高度 == 2:
                        左图, 左名, 右图, 右名 = 分割贴图并导入(self, 贴图, 宽度, 高度, 前缀, 部件, 类型, 扩展, 名称, 贴图路径)
                        添加基础贴图(偏好, 模型, 左图, 左名, 分割贴图, 透明贴图)
                        添加基础贴图(偏好, 模型, 右图, 右名, 分割贴图, 透明贴图)

                        光照贴图 = 获取光照贴图(None, 游戏, 图像)
                        if 光照贴图:
                            贴图 = Image.open(光照贴图.filepath).convert("RGBA")
                            宽度, 高度 = 光照贴图.size
                            类型 = 光照贴图.小二预设模板.类型
                            if 宽度 / 高度 == 2:
                                分割贴图并导入(self, 贴图, 宽度, 高度, 前缀, 部件, 类型, 扩展, 光照贴图.name, 贴图路径)
                基础贴图.extend(分割贴图)
            if 分割贴图:
                return 匹配模型贴图和导入贴图(None, [(目标贴图, 原始名称)], 分割贴图)
            break
    return None, None

def 分割贴图并导入(self, 贴图, 宽度, 高度, 前缀, 部件, 类型, 扩展, 名称, 贴图路径):
    中点 = 宽度 / 2
    左图 = 贴图.crop((0, 0, 中点, 高度))
    右图 = 贴图.crop((中点, 0, 宽度, 高度))
    # 左名 = f"{前缀}_{部件}1_{类型}{扩展}"
    # 右名 = f"{前缀}_{部件}2_{类型}{扩展}"
    def 保存导入(图像, 编号):
        图名 = f"{前缀}_{部件}{编号}_{类型}{扩展}"
        路径 = os.path.join(贴图路径, 图名)
        图像.save(路径)
        导入贴图 = bpy.data.images.load(str(路径))
        # 导入完成后删除本地图像文件
        if os.path.exists(路径):
            导入贴图.pack()
            os.remove(路径)
        导入贴图.小二预设模板.正则前缀 = 前缀
        导入贴图.小二预设模板.正则部件 = 部件+编号
        导入贴图.小二预设模板.正则类型 = 类型
        return 图名
    左名 = 保存导入(左图, 编号='1')
    右名 = 保存导入(右图, 编号='2')
    # 左图路径 = os.path.join(贴图路径, 左名)
    # 右图路径 = os.path.join(贴图路径, 右名)
    # 左图.save(左图路径)
    # 右图.save(右图路径)
    # 导入左图 = bpy.data.images.load(os.path.join(贴图路径, 左名))
    # 导入右图 = bpy.data.images.load(os.path.join(贴图路径, 右名))
    self.report({"INFO"}, f"分割{名称}\n左图{左名}\n右图{右名}")
    return 左图, 左名, 右图, 右名

def 添加基础贴图(偏好, 模型, 图像, 名称, 分割贴图, 透明贴图):
    分割贴图.append((图像, 名称))
    像素 = np.array(图像)
    图像 = bpy.data.images[名称]
    选项 = 模型.小二预设模板.基础贴图.add()
    选项.贴图 = 图像
    检查透明(偏好, 图像, 像素, 透明贴图)