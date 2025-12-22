import os, bpy, tempfile
from typing import cast
from .处理文件 import 处理文件
from ..图像.筛选贴图 import 确认贴图
from ..图像.导入贴图 import 匹配阈值
from ..通用.剪尾 import 剪去后缀
from ..材质.材质分类 import 材质分类
from ..着色.贴图.基础贴图 import 筛选贴图, 筛选基础贴图
from ..图像.匹配贴图.匹配贴图 import 匹配模型贴图和导入贴图
from ..指针 import XiaoerImage

global Image  #  1.0.1更新：不再直接导入PIL
try:
    from PIL import Image
except ImportError:
    Image = None
    pass

排除集合 = set()

def 深度检索(self:bpy.types.Operator, 模型, 候选路径, 游戏=None):

    self.report({"INFO"}, f"{模型.name}初步搜索结果如下，即将进行深度检索进一步确认\n"+"\n".join(
        f"{路径}" for 路径 in 候选路径))

    # 材质分类，获取头发贴图和衣服贴图
    五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质 = 材质分类(模型)
    def 获取特定贴图(头发材质, 衣服材质):
        头发贴图 = set()
        图像集合 = set()
        for 材质 in 头发材质:
            原始贴图, 图像节点 = 筛选贴图(None, 材质)
            头发贴图.add(原始贴图)
        for 材质 in 衣服材质:
            图像, 节点 = 筛选贴图(None, 材质)
            if 图像:
                if 图像 not in 头发贴图 and not 图像.name in ["发", "髪", "髮"]:   # 刻晴「霓裾翩跹」Hair贴图实为黑丝贴图
                    图像集合.add(图像)
        return 图像集合
    图像集合 = 获取特定贴图(头发材质, 衣服材质)  # 获取非头发的模型贴图
    # self.report({"INFO"}, f"图像集合{图像集合}")
    # self.report({"INFO"}, f"排除集合{排除集合}")
    源图 = next((图像 for 图像 in 图像集合 if 图像.name not in 排除集合), None)
    if 源图 and 源图.filepath and os.path.exists(源图.filepath):
        贴图 = Image.open(源图.filepath).convert("RGBA")
        图名 = 源图.name
        print(f'模型贴图 {图名}')
        模型贴图 = [(贴图, 图名)]
        基础贴图 = [] # (PIL图像, 对应路径)
        for 路径 in 候选路径:
            # self.report({"INFO"}, 路径)
            if os.path.isfile(路径) and 路径.endswith('.blend'):
                临时目录 = tempfile.gettempdir()
                with bpy.data.libraries.load(路径) as (数据源, 数据流):
                    数据流.images = 数据源.images
                    数据流.objects = 数据源.objects
                    数据流.materials = 数据源.materials
                    数据流.node_groups = 数据源.node_groups
                材质集合 = set()
                for 材质 in 数据源.materials:
                    材质集合.add(材质)
                五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质 = 材质分类(模型, 材质集合)
                图像集合 = 获取特定贴图(脸部材质, 衣服材质+皮肤材质+头发材质)   # 刻晴「霓裾翩跹」Hair贴图实为黑丝贴图  # 获取非脸部的模型贴图
                for 图像 in 图像集合:
                # for 图像 in 数据源.images:
                #     # 数据流.images = [图像]
                #     if "Body" in 图像.name and 非头发贴图:
                #     名称 = os.path.splitext(os.path.basename(图像.filepath))[0]  # 防止名称长度限制
                    名称, 后缀 = 剪去后缀(图像.name)
                    if os.path.splitext(名称)[0] not in ['衣']:
                        try:
                            print(f'预设贴图 {名称}')
                            保存路径 = os.path.join(临时目录, 名称)
                            图像.filepath_raw = 保存路径
                            图像.file_format = 'PNG'
                            图像.save()
                            贴图 = Image.open(图像.filepath).convert("RGBA")
                            基础贴图.append((贴图, 路径))
                            os.remove(保存路径)
                        except:
                            print(f'预设贴图 {名称} 无法读取')
                for 物体 in 数据源.objects:
                    bpy.data.objects.remove(物体)
                for 材质 in 数据源.materials:
                    bpy.data.materials.remove(材质)
                for 节点组 in 数据源.node_groups:
                    bpy.data.node_groups.remove(节点组)
                for 图像 in 数据源.images:
                    bpy.data.images.remove(图像)
            if os.path.isdir(路径):
                for 目录, 子目录, 文件列表 in os.walk(路径):  # 1.1.0适配模型路径的情况
                    for 文件 in 文件列表:
                        # if "Hair" not in 文件 and 确认贴图(文件):
                        if 确认贴图(文件):   # 刻晴「霓裾翩跹」Hair贴图实为黑丝贴图
                            # 名称 = os.path.splitext(图像)[0]
                            图像路径 = os.path.join(目录, 文件)
                            图像 = cast(XiaoerImage, bpy.data.images.load(str(图像路径)))
                            if 筛选基础贴图(游戏, 图像):
                                贴图 = Image.open(图像路径).convert("RGBA")
                                基础贴图.append((贴图, 路径))
                            bpy.data.images.remove(图像)
        if 基础贴图:
            匹配路径, 模型贴图匹配过程 = 匹配模型贴图和导入贴图(模型, 模型贴图, 基础贴图)
            # for 原始名称 in 模型贴图匹配过程:
            #     self.report({"INFO"}, "".join(
            #         f"{原始名称} 与 {导入名称} 汉明距离: {汉明距离}\n"
            #         for 导入名称, 汉明距离 in 模型贴图匹配过程[原始名称].items())+
            #         # for 导入名称, 汉明距离 in sorted(模型贴图匹配过程[原始名称].items(), key=lambda x: x[1]))+
            #         f"深度检索最终结果： {匹配路径[原始名称]} （汉明距离最小）")
            print(模型贴图匹配过程)
            # # 初始化最小值和计数器
            # 最小距离 = float('inf')  # 初始化为无穷大
            # # 匹配数量 = 0
            最短名称 = float('inf')  # 初始化为无穷大
            # 最佳路径 = None  # 使用有效名称最短的路径
            最佳路径 = 匹配路径[图名]
            最小距离 = 模型贴图匹配过程[图名][最佳路径]
            # self.report({"INFO"}, f"最佳路径{最佳路径} 最小距离{最小距离}")
            print(最佳路径, 最小距离)
            # 遍历所有可能的匹配对
            for 原始名称 in 模型贴图匹配过程:
                for 导入名称, 汉明距离 in 模型贴图匹配过程[原始名称].items():
                    # print(导入名称, 汉明距离, 汉明距离 == 最小距离, 汉明距离 == 最小距离 < 匹配阈值)
                    if 汉明距离 == 最小距离 < 匹配阈值:
                        if os.path.isfile(导入名称) and 导入名称.endswith('.blend'):
                            文件 = os.path.basename(导入名称)
                            角色 = 处理文件(文件)
                            print(角色, f'当前最短名称{最短名称}')
                            if len(角色) < 最短名称:  # 优先匹配有效名称最短的路径
                                最短名称 = len(角色)
                                最佳路径 = 导入名称
                                # print(最佳路径, '最小距离',最小距离, '最短名称',最短名称)
                        if os.path.isdir(导入名称):
                            角色 = os.path.basename(os.path.normpath(导入名称))
                            替换 = str.maketrans('', '', '0123456789')  # 创建翻译表，删除数字
                            角色 = 角色.translate(替换)  # 移除数字
                            角色 = 角色.replace("_", "")
                            if len(角色) < 最短名称:  # 优先匹配有效名称最短的路径
                                # self.report({"INFO"}, f"更新最佳路径{导入名称} 最小距离{最小距离}")
                                最短名称 = len(角色)
                                最佳路径 = 导入名称
            if 最佳路径:
                if 最小距离 < 匹配阈值:
                    # if 匹配数量 == 1:
                    #     路径 = 匹配路径[图名]
                    # else:  # 优先匹配有效名称最短的路径
                    #     路径 = 最佳路径
                    路径 = 最佳路径
                    # self.report({"INFO"}, f"最佳路径{最佳路径} 最小距离{最小距离} 匹配")
                    # self.report({"INFO"}, f"路径{路径} {os.path.isfile(路径)} {路径.endswith('.blend')}")
                    # print(最佳路径, 最小距离)
                    if os.path.isfile(路径) and 路径.endswith('.blend'):
                        文件 = os.path.basename(路径)
                        角色 = 处理文件(文件)
                        return 路径, 角色
                    if os.path.isdir(路径):
                        角色 = os.path.basename(os.path.normpath(路径))
                        return 路径, 角色
                else:
                    self.report({"WARNING"}, f"{最佳路径} 检测结果误差太大")
            排除集合.add(源图.name)
            return 深度检索(self, 模型, 候选路径, 游戏)
    self.report({"ERROR"}, "未检测到正确结果")
    return None, None