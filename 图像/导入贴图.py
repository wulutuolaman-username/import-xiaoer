# coding: utf-8

import bpy
import os
import time
import datetime
import numpy as np
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from ..材质.获取材质 import 获取材质
from ..着色.贴图.基础贴图 import 筛选贴图, 筛选基础贴图
from ..图像.筛选贴图 import 确认贴图
from ..图像.像素处理 import 获取像素, 检查透明
from ..图像.匹配贴图.匹配贴图 import 匹配模型贴图和导入贴图
from ..图像.匹配贴图.分割贴图 import 尝试匹配分割贴图
from ..属性.模板 import 小二预设模板属性

global Image  #  1.0.1更新：不再直接导入PIL
try:
    from PIL import Image
except ImportError:
    pass

# global imagehash
# try:
#     import imagehash
# except ImportError:
#     pass

# 导入解包贴图，与模型贴图进行哈希匹配
def 导入贴图(self, 偏好, 模型, 贴图路径, 文件路径, 游戏, 角色):
    # 1.1.0改进为分别计算红、绿、蓝三通道距离
    贴图查重 = []  # blender
    模型贴图 = []  # PIL
    导入贴图 = []  # blender
    基础贴图 = []  # PIL
    # 匹配贴图 = {}  # 记录原始贴图和导入贴图的匹配关系，后续引用此字典进行匹配
    透明贴图 = defaultdict(list)  # 记录带有透明像素的贴图
    if 偏好.导入贴图:  # 如果开启了导入贴图
        if not 模型.小二预设模板.完成导入贴图:
            材质集合 = 获取材质(模型)
            # 输出目录 = r"E:\插件\我的插件\导入小二\导入小二-视频\1.1.0\贴图"
            # for 材质 in 模型.data.materials:  # 1.0.3修改
            for 材质 in 材质集合:
                图像, 图像节点 = 筛选贴图(self, 材质)
                if 图像 and 图像.pixels and 图像 not in 贴图查重:
                    贴图查重.append(图像)
                    小二预设模板属性(图像.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
                    # Blender API 阻塞点（无法在子线程并行）,需要全部图像转为PIL图像再进行纯python计算
                    贴图 = Image.open(图像.filepath).convert("RGBA")
                    # 贴图.save(os.path.join(输出目录, 图像.name))
                    像素 = np.array(贴图)
                    if np.all(像素 == 像素[0, 0]):  # 1.1.0纯色贴图不做哈希运算
                        self.report({"WARNING"}, f'“{图像.name}”为纯色贴图')
                    else:
                        if 筛选基础贴图(游戏, 图像):
                            选项 = 模型.小二预设模板.基础贴图.add()
                            选项.贴图 = 图像
                        elif not 图像.小二预设模板.匹配贴图:
                            模型贴图.append((贴图, 图像.name))
                            检查透明(偏好, 图像, 像素, 透明贴图)
                            # 透明像素 = 检查透明(像素)
                            # if 透明像素:
                            #     x坐标, y坐标 = 透明像素
                            #     透明贴图[图像] = (x坐标, y坐标)
            # 导入贴图
            self.report({"INFO"}, f"导入贴图" + str(贴图路径))
            # 遍历目录下的所有文件
            for 目录, 子目录, 文件列表 in os.walk(贴图路径):  # 1.1.0适配模型路径的情况
                for 图像 in 文件列表:
                    if 确认贴图(图像):
                        if 图像 in bpy.data.images:  # 1.1.0解包贴图已在模型中使用，则无须匹配直接后续使用
                            # self.report({"INFO"}, f"{图像} 已存在，无需导入")
                            贴图 = bpy.data.images[图像]
                            if 贴图 not in 导入贴图:
                                导入贴图.append(贴图)
                            if not 贴图.pixels:
                                贴图位置 = os.path.join(目录, 图像)  # 1.1.0强制字符串路径
                                self.report({"INFO"}, f"重新加载" + str(贴图位置))
                                贴图.filepath = str(贴图位置)  # 替换贴图
                                贴图.reload()  # 重新加载
                            if 筛选基础贴图(游戏, 贴图):
                                # 匹配贴图[贴图] = 贴图
                                贴图.小二预设模板.匹配贴图 = 贴图
                                #     self.report({"INFO"}, f"{图像} 已存在，无需导入")
                                # else:
                                #     导入贴图.append(贴图)
                                #     self.report({"INFO"}, f"{图像} 已替换重载")
                        else:
                            贴图位置 = os.path.join(目录, 图像)  # 1.1.0强制字符串路径
                            try:  # 导入图像到 Blender
                                图像 = bpy.data.images.load(str(贴图位置))
                                导入贴图.append(图像)
                                # self.report({"INFO"}, f"导入成功：" + str(imagename))
                            except Exception as e:
                                self.report({"ERROR"}, f"导入失败：{图像}\n{e}")
            if 导入贴图:
                for 图像 in 导入贴图:
                    小二预设模板属性(图像.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
                    选项 = 模型.小二预设模板.导入贴图.add()
                    选项.贴图 = 图像
                    # if "Ramp" in 图像.name:
                    #     self.report({"INFO"}, f"{模型.name}\n{图像.name} {图像.users}")
                    if 筛选基础贴图(游戏, 图像):
                        选项 = 模型.小二预设模板.基础贴图.add()
                        选项.贴图 = 图像
                        # Blender API 阻塞点（无法在子线程并行）,需要全部图像转为PIL图像再进行纯python计算
                        贴图 = Image.open(图像.filepath).convert("RGBA")
                        # 贴图.save(os.path.join(输出目录, 图像.name))
                        像素 = np.array(贴图)
                        基础贴图.append((贴图, 图像.name))
                        # 透明像素 = 检查透明(像素)
                        if 检查透明(偏好, 图像, 像素, 透明贴图):
                            图像.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
                            # x坐标, y坐标 = 透明像素
                            # 透明贴图[图像] = (x坐标, y坐标)
                模型.小二预设模板.完成导入贴图 = True

        if not 模型.小二预设模板.完成匹配贴图 and 模型贴图:
            if 模型.小二预设模板.完成导入贴图 and not 基础贴图:
                for 选项 in 模型.小二预设模板.基础贴图:
                    # 贴图 = bpy.data.images[图像]
                    图像 = 选项.贴图
                    # Blender API 阻塞点（无法在子线程并行）,需要全部图像转为PIL图像再进行纯python计算
                    贴图 = Image.open(图像.filepath).convert("RGBA")
                    # 贴图.save(os.path.join(输出目录, 图像.name))
                    基础贴图.append((贴图, 图像.name))
                    像素 = np.array(贴图)
                    检查透明(偏好, 图像, 像素, 透明贴图)
                    # 透明像素 = 检查透明(像素)
                    # if 透明像素:
                    #     x坐标, y坐标 = 透明像素
                    #     透明贴图[图像] = (x坐标, y坐标)

            起始 = time.perf_counter()
            # 模型贴图匹配过程 = defaultdict(dict)  # 使用defaultdict自动初始化嵌套字典
            #
            # if len(模型贴图) > 0 and len(基础贴图) > 0:  # 1.1.0选择模型路径没有需要哈希的导入贴图则跳过
            #     # Blender API 阻塞点（无法在子线程并行）,需要全部图像转为PIL图像再进行纯python计算
            #     # 1.1.0多线程并行匹配贴图
            #     哈希尺寸 = 32
            #     def 匹配模型贴图(原始贴图, 原始名称):
            #         try:
            #             # if 原始贴图 not in 匹配贴图:  # 跳过与导入贴图同名的贴图
            #             像素1 = np.array(原始贴图)
            #             尺寸 = 原始贴图.size
            #             透明 = 像素1[..., 3] == 0  # 仅检查第4个通道（A）
            #             像素1[透明] = [0, 0, 0, 0]  # 1.1.0应用透明遮罩
            #             # 起 = time.perf_counter()
            #             # 生成RGB三个通道图像
            #             红图 = Image.fromarray(像素1[..., 0], 'L')
            #             绿图 = Image.fromarray(像素1[..., 1], 'L')
            #             蓝图 = Image.fromarray(像素1[..., 2], 'L')
            #             # 分别生成哈希
            #             哈希R1 = imagehash.phash(红图, 哈希尺寸)
            #             哈希G1 = imagehash.phash(绿图, 哈希尺寸)
            #             哈希B1 = imagehash.phash(蓝图, 哈希尺寸)
            #             # 终 = time.perf_counter()
            #             # self.report({"INFO"}, f"{终 - 起:.6f} 秒 {datetime.datetime.now()}")
            #             return 原始贴图, 原始名称, 哈希R1, 哈希G1, 哈希B1, 透明, 尺寸
            #         except Exception as e:
            #             self.report({"ERROR"}, f"匹配' {原始名称} '出错: {e}")
            #             return None, None, None, None
            #     def 尝试匹配贴图(导入贴图, 导入名称, 原始名称, 透明, 尺寸):
            #         try:
            #             缩放图像 = 导入贴图.copy().resize(尺寸, Image.NEAREST)  # 应用透明遮罩必须相同分辨率
            #             像素2 = np.array(缩放图像)
            #             像素2[透明] = [0, 0, 0, 0]  # 1.1.0应用透明遮罩
            #             # # 图像遮罩2 = Image.fromarray(像素2, 'RGBA')
            #             # # 图像遮罩2.save(os.path.join(输出目录, f"{原始名称} 尝试匹配贴图 {导入名称}"))
            #             # 起 = time.perf_counter()
            #             # 生成RGB三个通道图像
            #             红图 = Image.fromarray(像素2[..., 0], 'L')
            #             绿图 = Image.fromarray(像素2[..., 1], 'L')
            #             蓝图 = Image.fromarray(像素2[..., 2], 'L')
            #             # 分别生成哈希
            #             哈希R2 = imagehash.phash(红图, 哈希尺寸)
            #             哈希G2 = imagehash.phash(绿图, 哈希尺寸)
            #             哈希B2 = imagehash.phash(蓝图, 哈希尺寸)
            #             # 终 = time.perf_counter()
            #             # self.report({"INFO"}, f"{终 - 起:.6f} 秒 {datetime.datetime.now()}")
            #             return 导入贴图, 导入名称, 哈希R2, 哈希G2, 哈希B2
            #         except Exception as e:
            #             self.report({"ERROR"}, f"匹配' {导入名称} '出错: {e}")
            #             return None, None
            #     def 并行匹配全部贴图(模型贴图, 基础贴图):
            #         模型贴图匹配过程 = defaultdict(dict)  # 使用defaultdict自动初始化嵌套字典
            #         with ThreadPoolExecutor(max_workers=len(模型贴图)) as 执行器1:
            #             匹配任务1 = [执行器1.submit(匹配模型贴图, 原始贴图, 原始名称) for 原始贴图, 原始名称 in 模型贴图]
            #             for 任务1 in 匹配任务1:
            #                 汉明距离 = {}
            #                 原始贴图, 原始名称, 哈希R1, 哈希G1, 哈希B1, 透明, 尺寸 = 任务1.result()
            #                 with ThreadPoolExecutor(max_workers=len(基础贴图)) as 执行器2:
            #                     匹配任务2 = [执行器2.submit(尝试匹配贴图, 导入贴图, 导入名称, 原始名称, 透明, 尺寸)  for 导入贴图, 导入名称 in 基础贴图]
            #                     for 任务2 in 匹配任务2:
            #                         导入贴图, 导入名称, 哈希R2, 哈希G2, 哈希B2 = 任务2.result()
            #                         汉明距离[(哈希R1 - 哈希R2)*(哈希G1 - 哈希G2)*(哈希B1 - 哈希B2)] = 导入名称
            #                         模型贴图匹配过程[原始名称][导入名称] = (哈希R1 - 哈希R2)*(哈希G1 - 哈希G2)*(哈希B1 - 哈希B2)  # 使用字典嵌套存储所有匹配结果
            #                 最小距离 = min(汉明距离)
            #                 导入名称 = 汉明距离[最小距离]
            #                 匹配贴图[原始名称] = 导入名称
            #         return 匹配贴图, dict(模型贴图匹配过程)  # 转为普通字典返回
            #     匹配贴图, 模型贴图匹配过程 = 并行匹配全部贴图(模型贴图, 基础贴图)
            # 模型.小二预设模板.完成匹配贴图 = True
            匹配贴图, 模型贴图匹配过程 = 匹配模型贴图和导入贴图(模型, 模型贴图, 基础贴图)
            if not 基础贴图:
                self.report({"ERROR"}, f"{贴图路径} 未找到 {角色} 基础解包贴图")
            if not 匹配贴图:
                self.report({"ERROR"}, f"{贴图路径} 未找到 {角色} 匹配贴图")
            def 距离合适(最小距离):  # 增加距离限制
                if 最小距离 < 1e8:
                    return True
                else:
                    return False
            if 模型贴图匹配过程:
                for 原始名称 in 模型贴图匹配过程:
                    导入名称 = 匹配贴图[原始名称]
                    原始贴图 = bpy.data.images[原始名称]
                    导入贴图 = bpy.data.images[导入名称]
                    # 距离合适 = 模型贴图匹配过程[原始名称][导入名称] < 距离阈值
                    self.report({"INFO"}, "".join(
                        f"{原始名称} 与 {导入名称} 汉明距离: {汉明距离}\n"
                        for 导入名称, 汉明距离 in sorted(模型贴图匹配过程[原始名称].items(), key=lambda x: x[1]))+
                        f"{原始名称} 匹配 {匹配贴图[原始名称]} （汉明距离最小）" if 距离合适(模型贴图匹配过程[原始名称][导入名称])
                        else "".join(
                        f"{原始名称} 与 {导入名称} 汉明距离: {汉明距离}\n"
                        for 导入名称, 汉明距离 in sorted(模型贴图匹配过程[原始名称].items(), key=lambda x: x[1]))+
                        f"{原始名称} 与 {匹配贴图[原始名称]} 最小距离过大，尝试重新匹配贴图" )
                    if 距离合适(模型贴图匹配过程[原始名称][导入名称]):
                        原始贴图.小二预设模板.匹配贴图 = 导入贴图
                    elif 原始贴图.size[0] / 原始贴图.size[1] == 1 and any(导入贴图.size[0] / 导入贴图.size[1] == 2 for 导入贴图, 导入名称 in 基础贴图):
                        匹配分割贴图, 模型贴图匹配分割贴图过程 = 尝试匹配分割贴图(self, 偏好, 模型, 游戏, 模型贴图, 基础贴图, 原始贴图, 原始名称, 贴图路径, 透明贴图)
                        if 匹配分割贴图 and 模型贴图匹配分割贴图过程:
                            导入名称 = 匹配分割贴图[原始名称]
                            导入贴图 = bpy.data.images[导入名称]
                            self.report({"INFO"}, "".join(
                                f"{原始名称} 与 {导入名称} 汉明距离: {汉明距离}\n"
                                for 导入名称, 汉明距离 in sorted(模型贴图匹配分割贴图过程[原始名称].items(), key=lambda x: x[1]))+
                                f"{原始名称} 匹配 {匹配分割贴图[原始名称]} （汉明距离最小）" if 距离合适(模型贴图匹配分割贴图过程[原始名称][导入名称])
                                else "".join(
                                f"{原始名称} 与 {导入名称} 汉明距离: {汉明距离}\n"
                                for 导入名称, 汉明距离 in sorted(模型贴图匹配分割贴图过程[原始名称].items(), key=lambda x: x[1]))+
                                f"{原始名称} 与 {匹配分割贴图[原始名称]} 最小距离过大")
                            if 距离合适(模型贴图匹配分割贴图过程[原始名称][导入名称]):
                                原始贴图.小二预设模板.匹配贴图 = 导入贴图
                        else:
                            self.report({"ERROR"}, f"未找到宽高比为2：1可分割的导入贴图")
                    else:
                        self.report({"ERROR"}, f"{原始名称}未找到匹配贴图")
                # if 偏好.基础贴图快速匹配:
                #     self.report({"INFO"}, f"已完成基础贴图快速匹配")
                # if 偏好.基础贴图精确匹配:
                #     self.report({"INFO"}, f"已完成基础贴图精确匹配")
                终止 = time.perf_counter()
                self.report({"INFO"}, f"🕐 匹配模型基础贴图与导入基础贴图用时：{终止 - 起始:.6f} 秒\n"
                                      f"贴图路径：{贴图路径}\n"      
                                      f"模型基础贴图数量{len(模型贴图)}：\n"+"\n".join(f"{原始名称}" for 原始贴图, 原始名称 in 模型贴图)+"\n"
                                      f"导入基础贴图数量{len(基础贴图)}：\n"+"\n".join(f"{导入名称}" for 导入贴图, 导入名称 in 基础贴图)
                                      )
    return 透明贴图