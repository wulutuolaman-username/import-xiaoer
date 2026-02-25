from .射线法 import 多点在面内
from .面积法 import 相交面积
from .判断透明 import 判断透明
from ...通用.信息 import 报告信息
import bpy, time, numpy as np
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from ...偏好.偏好设置 import 小二偏好
from ...指针 import *

# 用集合分别收集材质面在UV上的点坐标和贴图透明像素在UV上的点坐标，最后通过两个集合的交集判断透明
材质面像素点 = defaultdict(set)
像素面索引 = defaultdict(set)
上次检测 = None

def 通过UV和像素检测透明材质(self:bpy.types.Operator, 偏好:小二偏好, 材质, 图像, 透明贴图, 材质面):
    if 透明贴图 and 图像 in 透明贴图:
        透明像素点 = 透明贴图[图像][0]  # alpha < 250
        完全透明像素点 = 透明贴图[图像][1]  # alpha < 20
        # print(图像.name, 透明像素点)
        面数据 = 材质面[材质]
        if 透明像素点 and 面数据:
            def 处理每个面(面顶点):
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
                if 偏好.检测方式 == '射线':
                    在内 = 多点在面内(像素点, 面顶点)
                if 偏好.检测方式 == '面积':
                    # —— 批量计算“像素方形 ∩ 面”的面积 —— #
                    面积数组 = 相交面积(像素点, 面顶点)
                    # —— 过滤面积>0 的像素，得到整数像素坐标集合 —— #
                    在内 = 面积数组 > 1e-12  # 数值阈值，避免浮点噪声
                # 提取被命中的原始整数像素坐标（用 .ravel() 展平）
                命中_x = xv.ravel()[在内]
                命中_y = yv.ravel()[在内]
                像素点 = set(zip(命中_x, 命中_y))  # 转为 set
                return 像素点

            面像素点 = set()
            global 上次检测  # 声明要修改全局变量
            if 材质面像素点[材质] and 上次检测 == 偏好.检测方式:
                面像素点 = 材质面像素点[材质]
            else:
                上次检测 = 偏好.检测方式
                # print(材质, '材质面数量：', len(材质面顶点[材质]), datetime.datetime.now())
                起始 = time.perf_counter()
                with ThreadPoolExecutor(max_workers=len(面数据)) as 执行器:
                    匹配任务 = [执行器.submit(处理每个面, 面顶点) for 面顶点 in 面数据]
                    for 任务 in 匹配任务:
                        像素点 = 任务.result()
                        面像素点.update(像素点)
                    材质面像素点[材质] = 面像素点
                    终止 = time.perf_counter()
                报告信息(self, '正常', f'🕐 材质Material["{材质.name}"]在检测透明前分析材质面UV区域像素用时：{终止 - 起始:.6f} 秒')
            return 面像素点, 透明像素点, 完全透明像素点
    return None, None, None

def 材质UV包含透明像素(self:bpy.types.Operator, 偏好:小二偏好, 模型, 材质:小二材质, 图像, 透明贴图, 材质面):
    if 偏好.检测透明材质:
        材质.小二预设模板.使用检测透明材质 = True
        面像素点, 透明像素点, 完全透明像素点 = 通过UV和像素检测透明材质(self, 偏好, 材质, 图像, 透明贴图, 材质面)
        if 透明像素点 and 面像素点:
            if 判断透明(self, 材质, 图像, 面像素点, 透明像素点, 完全透明像素点):
                材质.小二预设模板.检测结果 = True
                return True
    return False