from .射线法 import 点在面内, 多点在面内
from .面积法 import 相交面积
from .判断透明 import 判断透明
from ...通用.信息 import 报告信息
import time
import datetime
import numpy as np
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# def 检测单个面(点, 面数据):
#     面顶点 = 面数据['UV坐标']
#     # 包围盒过滤
#     min_u = min(u for (u, v) in 面顶点)
#     max_u = max(u for (u, v) in 面顶点)
#     min_v = min(v for (u, v) in 面顶点)
#     max_v = max(v for (u, v) in 面顶点)
#     # 如果点落在包围盒外，则跳过射线测试
#     if (min_u <= 点[0] <= max_u and min_v <= 点[1] <= max_v):
#         # 面顶点排序 = sorted(面顶点.copy())
#         # if 面顶点排序 not in 材质面去重:
#         #     材质面去重.add(面顶点排序)
#         if 点在面内(点, 面顶点):
#             return True
#     return False
#
# def 像素块顶点在材质面内(点, 材质, 材质面):
#     # 材质面去重 = set()
#     # # 获取UV层
#     # UV图层 = 模型.data.uv_layers.active.data if 模型.data.uv_layers.active else None
#     # if not UV图层:
#     #     return None
#     # print(材质.name, f'材质面', len(材质面[材质]))
#     # for 面数据 in 材质面[材质]:
#         # 面顶点 = 面数据['UV坐标']
#     #     for 顶点 in 面.loop_indices:
#     #         UV坐标 = UV图层[顶点].uv
#     #         面顶点.append((UV坐标.x, UV坐标.y))
#
#     with ThreadPoolExecutor(max_workers=len(材质面[材质])) as executor:
#         futures = [executor.submit(检测单个面, 点, 面数据) for 面数据 in 材质面[材质]]
#         for future in as_completed(futures):
#             # print(datetime.datetime.now())
#             if future.result():
#                 return True
#         # return any(future.result() for future in as_completed(futures))
#     return False
材质面像素点 = defaultdict(set)
像素面索引 = defaultdict(set)
上次检测 = None

def 通过UV和像素检测透明材质(self, 偏好, 材质, 图像, 透明贴图, 材质面):
    if 透明贴图 and 图像 in 透明贴图:
        # 透明像素坐标 = 透明贴图[图像]
        透明像素点 = 透明贴图[图像][0]
        完全透明像素点 = 透明贴图[图像][1]
        # print(图像.name, 透明像素点)
        面数据 = 材质面[材质]
        # 材质面索引 = 材质面['索引']
        检测方式 = '射线法' if 偏好.射线法检测透明 else '面积法'
        if 透明像素点 and 面数据:
            def 处理每个面(面顶点):
                面索引 = 材质面['索引'][0][str(sorted(面顶点))]
                # self.report({"INFO"}, f'材质Material["{材质.name}"]\n 面顶点：{面顶点}\n 面索引：{面索引}')
                面顶点 = np.array(面顶点)
                面顶点 *= 偏好.检测透明分辨率  # 变成像素空间坐标

                min_u = int(np.floor(面顶点[:, 0].min()))
                max_u = int(np.ceil(面顶点[:, 0].max()))
                min_v = int(np.floor(面顶点[:, 1].min()))
                max_v = int(np.ceil(面顶点[:, 1].max()))

                # 准备像素中心点
                xv, yv = np.meshgrid(np.arange(min_u, max_u + 1), np.arange(min_v, max_v + 1))
                像素点 = np.stack([(xv + 0.5).ravel(), (yv + 0.5).ravel()], axis=-1)  # +0.5从像素左下角移到像素中心
                在内 = None
                if 偏好.射线法检测透明:
                    在内 = 多点在面内(像素点, 面顶点)
                if 偏好.面积法检测透明:
                    # —— 批量计算“像素方形 ∩ 面”的面积 —— #
                    面积数组 = 相交面积(像素点, 面顶点)
                    # —— 过滤面积>0 的像素，得到整数像素坐标集合 —— #
                    在内 = 面积数组 > 1e-12  # 数值阈值，避免浮点噪声
                # 提取被命中的原始整数像素坐标（用 .ravel() 展平）
                命中_x = xv.ravel()[在内]
                命中_y = yv.ravel()[在内]
                像素点 = set(zip(命中_x, 命中_y))  # 转为 set
                return 像素点, 面索引

            # 材质面像素点 = defaultdict(set)
            面像素点 = set()
            global 上次检测  # 声明要修改全局变量
            if 材质面像素点[材质] and 检测方式 == 上次检测:
                面像素点 = 材质面像素点[材质]
            else:
                上次检测 = 检测方式
                # print(材质, '材质面数量：', len(材质面顶点[材质]), datetime.datetime.now())
                起始 = time.perf_counter()
                with ThreadPoolExecutor(max_workers=len(面数据)) as 执行器:
                    匹配任务 = [执行器.submit(处理每个面, 面顶点) for 面顶点 in 面数据]
                    for 任务 in 匹配任务:
                        # 像素点, 面顶点 = 任务1.result()
                        像素点, 面索引 = 任务.result()
                        面像素点.update(像素点)
                        if 像素点:
                            for 点 in 像素点:
                                像素面索引[(int(点[0]),int(点[1]))].update(面索引)
                    材质面像素点[材质] = 面像素点
                    终止 = time.perf_counter()
                报告信息(self, '正常', f'🕐 材质Material["{材质.name}"]在检测透明前分析材质面UV区域像素用时：{终止 - 起始:.6f} 秒')
            # 报告信息(self, '正常', f'材质Material["{材质.name}"] 像素面索引：{像素面索引}')
            return 面像素点, 透明像素点, 完全透明像素点, 像素面索引
    return None, None, None, None

def 材质UV包含透明像素(self, 偏好, 模型, 材质, 图像, 透明贴图, 材质面):
    if 偏好.检测透明材质:
        # 面像素点 = 材质面[材质]
        # print(材质.name, 面像素点)
        # print(材质.name, 图像.name, f'透明像素坐标', len(透明像素坐标))
        # if 透明像素坐标:
        材质.小二预设模板.使用检测透明材质 = True
        面像素点, 透明像素点, 完全透明像素点, 像素面索引 = 通过UV和像素检测透明材质(self, 偏好, 材质, 图像, 透明贴图, 材质面)
        if 透明像素点 and 面像素点:
            # 报告信息(self, '正常', f'🕐{type(透明像素点)} {type(完全透明像素点)} {type(面像素点)}')
            # print('面像素点', 面像素点)
            # print(type(透明像素点), type(完全透明像素点), type(面像素点))
            # 透明占比 = len(透明像素点 & 面像素点) / len(面像素点)
            # 报告信息(self, '正常', f'{图像.name}透明像素数量{len(透明像素点)}\n材质Material["{材质.name}"]面像素数量{len(面像素点)} 其中透明像素数量{len(透明像素点 & 面像素点)}\n透明占比 {透明占比:.3%}')
            # if 透明像素点 & 面像素点 and not 面像素点 < 完全透明像素点: # 材质面区域存在透明像素，并且材质非完全透明
            if 判断透明(self, 材质, 图像, 面像素点, 透明像素点, 完全透明像素点):
                # 菈乌玛头发贴图同时存在透明和不透明，
                ## 材质Material["Alpha"] 透明占比 59.162% 树叶 透明材质
                ## 材质Material["饰"] 透明占比 73.272% 月之轮 非透明材质
                # if 透明占比 < 0.6:
                    材质.小二预设模板.检测结果 = True
                    return True
            # 起始 = time.perf_counter()
            # x坐标, y坐标 = 透明像素坐标
            # 宽, 高 = 图像.size
            # 报告信息(self, '正常', f'材质Material["{材质}"]材质面数量{len(材质面[材质])} {图像.name}透明像素数量{len(x坐标)}')
            # for x, y in zip(x坐标, y坐标):
            #     点 = (float(x + 0.5) / 宽, float(y + 0.5) / 高)
            #     print(材质.name, f'材质面数量',len(材质面[材质]), 图像.name, f'透明像素数量',len(x坐标), f'检测点',点)
            #     if 像素块顶点在材质面内(点, 模型, 材质, 材质面):
            #         终止 = time.perf_counter()
            #         报告信息(self, '正常', f'🕐 材质Material["{材质.name}"]通过{UV图层.name}和{图像.name}检测透明用时：{终止 - 起始:.6f} 秒')
            #         return True
            # 点 = (x / 宽, y / 高)
            # if 像素块顶点在材质面内(点, 材质, 材质面):
            #     return True
            # 点 = ((x + 1) / 宽, y / 高)
            # if 像素块顶点在材质面内(点, 材质, 材质面):
            #     return True
            # 点 = (x / 宽, (y + 1) / 高)
            # if 像素块顶点在材质面内(点, 材质, 材质面):
            #     return True
            # 点 = ((x + 1)/ 宽, (y + 1) / 高)
            # if 像素块顶点在材质面内(点, 材质, 材质面):
            #     return True
            # 生成待检测UV点
            # UV点 = [((x + 0.5) / 512, (y + 0.5) / 512) for x, y in zip(x坐标, y坐标)]
            # print(材质, f'材质面数量', len(材质面[材质]), f'透明像素数量', len(UV点))
            # 多线程检测
            # with ThreadPoolExecutor(max_workers=len(UV点)) as executor:
            #     futures = {executor.submit(像素块顶点在材质面内, 点, 材质, 材质面): 点 for 点 in UV点}
            #     for future in as_completed(futures):
            #         if future.result():
            #             终止 = time.perf_counter()
            #             print(f'🕐 材质Material["{材质}"]检测透明用时：{终止 - 起始:.6f} 秒')
            #             return True
            # #     return any(future.result() for future in as_completed(futures))
            # 终止 = time.perf_counter()
            # print(f'🕐 材质Material["{材质}"]检测透明用时：{终止 - 起始:.6f} 秒')
            # 报告信息(self, '正常', f'🕐 材质Material["{材质.name}"]通过{UV图层.name}和{图像.name}像素检测透明用时：{终止 - 起始:.6f} 秒')
    return False