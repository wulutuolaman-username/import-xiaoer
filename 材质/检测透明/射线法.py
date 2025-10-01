def 点在面内(点, 面顶点):
    """判断点是否在2D多边形中（不包含边界）"""
    x, y = 点
    在内 = False
    顶点数量 = len(面顶点)
    for i in range(顶点数量):
        x0, y0 = 面顶点[i]
        x1, y1 = 面顶点[(i + 1) % 顶点数量]
        if ((y0 > y) != (y1 > y)) and \
           (x < (x1 - x0) * (y - y0) / (y1 - y0 + 1e-10) + x0):
            在内 = not 在内
    return 在内

import numpy as np

def 多点在面内(点集合, 面顶点):
    """ 返回数组 """
    x = 点集合[:, 0]
    y = 点集合[:, 1]
    顶点数量 = len(面顶点)
    在内 = np.zeros_like(x, dtype=bool) # 初始值是全False

    px = np.array([p[0] for p in 面顶点])
    py = np.array([p[1] for p in 面顶点])

    for i in range(顶点数量):
        j = (i + 1) % 顶点数量
        xi = px[i]
        yi = py[i]
        xj = px[j]
        yj = py[j]

        交集 = ((yi > y) != (yj > y)) & \
               (x < (xj - xi) * (y - yi) / (yj - yi + 1e-10) + xi)
        在内 ^= 交集

    return 在内  # shape (N,) 的 bool 数组