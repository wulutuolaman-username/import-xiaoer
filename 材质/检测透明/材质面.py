import bpy
import bmesh
import numpy as np
import time
import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from .射线法 import 点在面内
from ...通用.信息 import 报告信息

# 1.1.0检测透明材质
def 获取材质面(self, 偏好, 模型, 手动检测=False):
    UV图层 = 模型.data.uv_layers.active
    if not UV图层:
        self.report({"ERROR"}, f"{模型.name}未找到活动UV图层")
        return None
    UV图层.name = "UVMap"  # 统一活动UV图层名称，以便几何节点正确访问
    if not 模型.data.materials:
        self.report({"ERROR"}, f"{模型.name}没有材质")
        return None
    if 偏好.检测透明材质 or 手动检测:
        bm = bmesh.new()
        bm.from_mesh(模型.data)
        UV图层 = bm.loops.layers.uv.active
        材质面 = defaultdict(list)
        材质面去重 = defaultdict(list)
        # 材质面索引 = defaultdict(list)
        材质面索引 = defaultdict(set)
        for 面 in bm.faces:
            材质索引 = 面.material_index
            材质 = 模型.data.materials[材质索引]
            # if 材质.小二预设模板.材质分类 in ['五官', '头发', '皮肤', '衣服']:
                # 预处理UV坐标
                # 面数据 = {
                #     # '面对象': 面,
                #     'UV坐标': []
                # }
            面顶点 = [(loop[UV图层].uv.x, loop[UV图层].uv.y) for loop in 面.loops]
            # for 循环 in 面.loops:
            #     UV坐标 = 循环[UV图层].uv
            #     # x = UV坐标.x % 1  # 规范化到[0,1]
            #     # y = UV坐标.y % 1  # 规范化到[0,1]
            #     # 面数据['UV坐标'].append((x, y))
            #     面顶点.append((UV坐标.x, UV坐标.y))
            if all(x // 1 != 0 or y // 1 != 0 for x, y in 面顶点):  # 黄泉的裤材质最顶上的点超过1
                x_偏移, y_偏移 = zip(*((x // 1, y // 1) for x, y in 面顶点))
                计数 = {}
                for x_ in x_偏移:
                    for y_ in y_偏移:
                        面内 = sum(1 for x, y in 面顶点 if 0 <= x - x_ < 1 and 0 <= y - y_ < 1)
                        计数[面内] = (x_, y_)
                x_偏移, y_偏移 = 计数[max(计数)]
                面顶点 = [(loop[UV图层].uv.x - x_偏移, loop[UV图层].uv.y - y_偏移) for loop in 面.loops]
                # for x, y in 面顶点:
                #     x -= x_偏移
                #     y -= y_偏移
            # 报告信息(self, '正常', f'🕐 材质Material["{材质.name}"] 面顶点：{面顶点}')
            # 面顶点 = 面数据['UV坐标']
            # 面顶点 = np.array(面顶点)
            # 面顶点 *= 偏好.检测透明分辨率  # 变成像素空间坐标
            # 材质面[材质].add(面顶点)
            # 材质面索引[str(np.array(sorted(面顶点)))].append(面.index)
            材质面索引[str(sorted(面顶点))].add(面.index)
            if sorted(面顶点) not in 材质面去重[材质]:
                材质面去重[材质].append(sorted(面顶点))
                # 面顶点 = np.array(面顶点)
                # 面顶点 *= 偏好.检测透明分辨率  # 变成像素空间坐标
                材质面[材质].append(面顶点)
            # 材质面[材质].append(set(zip(np.round(面顶点[:, 0]), np.round(面顶点[:, 1]))))
        材质面['索引'].append(材质面索引)
        # 材质面['bm'].append(bm)
        # def 处理每个材质(材质):
        #     return 材质
        #
        # def 处理每个面(面顶点):
        #     # 面顶点 = 面数据['UV坐标']
        #     # uvs = np.array(面顶点)
        #     # uvs_px = uvs * 偏好.检测透明分辨率  # 变成像素空间坐标
        #     # 包围盒过滤
        #     min_u = int(np.floor(面顶点[:, 0].min()))
        #     max_u = int(np.ceil (面顶点[:, 0].max()))
        #     min_v = int(np.floor(面顶点[:, 1].min()))
        #     max_v = int(np.ceil (面顶点[:, 1].max()))
        #     # print(min_u, max_u, min_v, max_v, datetime.datetime.now())
        #     像素点 = set()
        #     for x in range(min_u, max_u + 1):
        #         for y in range(min_v, max_v + 1):
        #             像素点.add((x, y))
        #     return 像素点, 面顶点
        #
        # def 处理每个点(x, y, 面像素点, 面顶点):
        #     if 点在面内((x + 0.5, y + 0.5), 面顶点):  # 将像素中心作为测试点
        #         面像素点.add((x, y))
        #     return True
        #
        # 材质面像素点 = defaultdict(set)
        # with ThreadPoolExecutor(max_workers=len(材质面顶点)) as 执行器1:
        #     匹配任务1 = [执行器1.submit(处理每个材质, 材质) for 材质 in 材质面顶点]
        #     for 任务1 in 匹配任务1:
        #         起始 = time.perf_counter()
        #         材质 = 任务1.result()
        #         面像素点 = set()
        #         # print(材质, '材质面数量：', len(材质面顶点[材质]), datetime.datetime.now())
        #         with ThreadPoolExecutor(max_workers=len(材质面顶点[材质])) as 执行器2:
        #             匹配任务2 = [执行器2.submit(处理每个面, 面顶点) for 面顶点 in 材质面顶点[材质]]
        #             for 任务2 in 匹配任务2:
        #                 像素点, 面顶点 = 任务2.result()
        #                 # print(材质, '像素点数量：', len(像素点), datetime.datetime.now())
        #                 # print(材质, '面顶点：', 面顶点, '\n', '像素点：', 像素点, datetime.datetime.now())
        #                 with ThreadPoolExecutor(max_workers=len(像素点)) as 执行器3:
        #                 # with ProcessPoolExecutor(max_workers=60) as 执行器3:
        #                     匹配任务3 = [执行器3.submit(处理每个点, x, y, 面像素点, 面顶点) for (x, y) in 像素点]
        #                     if all(任务3.result() for 任务3 in 匹配任务3):
        #                     # if all(任务3.result() for 任务3 in as_completed(匹配任务3)):
        #                         材质面像素点[材质] = 面像素点
        #                         # print(材质, '面像素点数量：', len(面像素点), datetime.datetime.now())
        #                         # print(材质, '面像素点：', 面像素点, '\n', datetime.datetime.now())
        #         终止 = time.perf_counter()
        #         报告信息(self, '正常', f'材质Material["{材质}"]在检测透明前分析材质面UV区域像素用时：{终止 - 起始:.6f} 秒 材质面数量：{len(材质面顶点[材质])}')

        # 材质面 = defaultdict(set)
        # if 材质面像素点:
        #     for 材质 in 材质面像素点:
        #         面像素点 = 材质面像素点[材质]
        #         材质面[bpy.data.materials[材质]] = 面像素点
        return 材质面
    return None