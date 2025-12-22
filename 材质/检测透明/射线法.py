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