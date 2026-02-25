import numpy as np

# 先在像素空间（你的“检测透明分辨率”）下得到面的多边形顶点。
# 在面的像素包围盒里生成所有像素中心（x+0.5,y+0.5）。
# 对每个像素中心构造单位像素方形的四个角点（中心±0.5），用 Sutherland–Hodgman 把“面多边形”裁剪到这个方形里，得到交集多边形。
# 用鞋带公式算交集多边形面积；面积>0 即该像素被覆盖（即便像素中心不在面内也能检出）。
# 由于 S–H 要求裁剪器是凸多边形，我们把“像素方形”作为裁剪器（它是凸的），而“被裁剪的多边形”用你的面 UV（可以是凸也可以是凹）。

def 相交面积(像素点, 面顶点):
    """
    批量计算多个像素（正方形）与一个多边形的相交面积。
    :输入 像素点: 形状 (N, 2) 的数组，每行是一个像素中心 [cx, cy]
    :输入 面顶点:     形状 (M, 2) 的数组，按顶点顺序给出面多边形的顶点
    :输出 相交面积:           形状 (N,) 的数组，每个像素与面相交的面积
    """
    # 像素正方形的四个顶点相对偏移
    偏移 = np.array([
        [-0.5, -0.5],
        [ 0.5, -0.5],
        [ 0.5,  0.5],
        [-0.5,  0.5]
    ], dtype=np.float64)

    # 生成每个像素的四个角顶点坐标 (N, 4, 2)
    像素方形 = 像素点[:, None, :] + 偏移[None, :, :]

    # 逐个像素裁剪求交多边形面积
    面积结果 = np.zeros(len(像素点), dtype=np.float64)
    for i in range(len(像素点)):
        # 取一个像素的四边形
        像素多边形 = 像素方形[i]
        # 裁剪
        交集多边形 = 多边形相交(面顶点, 像素多边形)  # 必须使用像素作为裁剪器
        if len(交集多边形) >= 3:  # 至少 3 个点才能构成多边形；否则面积为 0
            面积结果[i] = 多边形面积(交集多边形)
            # # 检查并分离成多个多边形
            # 多个多边形 = 分离多边形_检测重合边(交集多边形, 像素多边形)
            # for 多边形 in 多个多边形:
            #     if len(多边形) >= 3:
            #         面积结果[i] += 多边形面积(np.array(多边形))
    return 面积结果

def 分离多边形_检测重合边(多边形, 裁剪器):
    """
    检测交集多边形是否沿裁剪器（方形）的边被分割成多个区域，并拆分成多个多边形。
    :输入 多边形: np.array(N,2) 裁剪结果多边形顶点序列
    :输入 裁剪器: np.array(4,2) 像素方形的四个顶点
    :输出 列表，每个元素是一个子多边形顶点列表
    """
    子多边形列表 = []
    当前子多边形 = []

    # 获取裁剪器方形的四条边线（每条边用起点和终点表示）
    裁剪器边 = [(裁剪器[j], 裁剪器[(j + 1) % 4]) for j in range(4)]

    def 点在线段上(p, a, b, tol=1e-9):
        # 向量叉积是否接近 0（共线）
        if abs((b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])) > tol:
            return False
        # p 是否在 a,b 的包围盒内
        return (min(a[0], b[0]) - tol <= p[0] <= max(a[0], b[0]) + tol and
                min(a[1], b[1]) - tol <= p[1] <= max(a[1], b[1]) + tol)

    n = len(多边形)
    for idx in range(n):
        当前点 = 多边形[idx]
        下一点 = 多边形[(idx + 1) % n]

        当前子多边形.append(当前点)

        # 检查边是否与裁剪器某条边完全重合
        for 裁边起, 裁边终 in 裁剪器边:
            if 点在线段上(当前点, 裁边起, 裁边终) and 点在线段上(下一点, 裁边起, 裁边终):
                # 发现重合边 → 可能是多区域的分界
                子多边形列表.append(当前子多边形)
                当前子多边形 = []
                break

    if 当前子多边形:
        子多边形列表.append(当前子多边形)

    # 如果只有一个子多边形，直接返回
    if len(子多边形列表) == 1:
        return 子多边形列表

    # 否则，检查每个子多边形是否闭合，如果不闭合需要补上起点
    for poly in 子多边形列表:
        if not np.allclose(poly[0], poly[-1]):
            poly.append(poly[0])

    return 子多边形列表

def 分离多边形_按重合段拆分(多边形, 裁剪器, tol=1e-9, round_decimals=9, 面积阈=1e-9):
    """
    将 Sutherland–Hodgman 的输出多边形（可能由多个子多边形通过桥接段串联）
    按与裁剪器（方形）边上“平行且有重合部分”的边线段端点进行拆分，
    最终尝试把序列拆成若干闭合的子多边形并返回它们（numpy 数组列表）。

    参数:
      多边形: np.array (N,2) 裁剪结果顶点序列（可以闭合或不闭合）
      裁剪器: np.array (4,2) 像素方形四个顶点（顺序任意，只需连通）
      tol: 浮点容许误差（判断共线、包含时用）
      round_decimals: 将坐标作为字典 key 时的四舍五入位数
      面积阈: 认为有效多边形所需最小面积（避免数值噪声）

    返回:
      子多边形列表: [np.array(Mi,2), ...] 每项是一个闭合（首尾相同或可闭合）的子多边形
    """

    # --- 规范化输入为numpy数组 & 去掉末尾与开头重复项方便处理 ---
    poly = np.asarray(多边形, dtype=np.float64).copy()
    if poly.shape[0] == 0:
        return []
    # 如果闭合（首尾相等），去掉最后一个重复点，方便按索引分段
    if poly.shape[0] > 1 and np.allclose(poly[0], poly[-1], atol=tol):
        poly = poly[:-1]

    # --- 生成裁剪器的四条边 (起点, 终点) 列表 ---
    clip = np.asarray(裁剪器, dtype=np.float64)
    clip_edges = [(clip[i], clip[(i+1) % len(clip)]) for i in range(len(clip))]

    # 存放每条裁剪器边对应的所有投影区间（列表），用于后续找覆盖>=2 的区间端点
    # 使用结构: projection_intervals[i] = list of (start, end) 在该边的投影轴上
    projection_intervals = []

    # --- 对每个裁剪器边，收集多边形中“几乎共线”的边段并投影为区间 ---
    # 这里限制只处理与裁剪器边方向近似平行的多边形边（水平或垂直情况）
    for edge_idx, (ca, cb) in enumerate(clip_edges):
        # 判断裁剪边方向：水平或垂直（裁剪器是方形时应当是）
        is_horizontal = abs(ca[1] - cb[1]) < tol
        is_vertical = abs(ca[0] - cb[0]) < tol
        intervals = []

        # 遍历 poly 的每条边，判断两端是否都在裁剪边所在直线上（共线）
        n = poly.shape[0]
        for i in range(n):
            p = poly[i]
            q = poly[(i+1) % n]
            # 点到直线的叉积检测共线性 (a->b) × (a->p) ≈ 0
            # 直接检查两端点到裁剪直线距离近似为零即可
            if is_horizontal:
                # 检查点 p,y 和 q,y 是否接近裁剪边 y
                y0 = ca[1]
                if abs(p[1] - y0) < tol and abs(q[1] - y0) < tol:
                    start = min(p[0], q[0])  # type:ignore
                    end = max(p[0], q[0])  # type:ignore
                    if end - start > tol:  # 非零长度
                        intervals.append((start, end))
            elif is_vertical:
                x0 = ca[0]
                if abs(p[0] - x0) < tol and abs(q[0] - x0) < tol:
                    start = min(p[1], q[1])  # type:ignore
                    end = max(p[1], q[1])  # type:ignore
                    if end - start > tol:
                        intervals.append((start, end))
            else:
                # 通常裁剪器是方形，这里不处理斜向裁剪边
                pass

        projection_intervals.append((is_horizontal, is_vertical, ca, cb, intervals))

    # --- 对每条裁剪器边的 intervals 查找 coverage>=2 的投影段端点（分割点） ---
    # 存放每条裁剪器边上需要切分的坐标值（x 或 y）
    split_positions_per_edge = [set() for _ in clip_edges]

    for idx, (is_h, is_v, ca, cb, intervals) in enumerate(projection_intervals):
        if not intervals:
            continue
        # 收集所有端点并排序
        endpoints = sorted({v for seg in intervals for v in seg})
        # 若只有一段端点，无法判断覆盖 >= 2
        if len(endpoints) < 2:
            continue
        # 构建相邻端点区间，检查中点的覆盖数量
        for a, b in zip(endpoints[:-1], endpoints[1:]):
            if b - a <= tol:
                continue
            mid = (a + b) / 2.0
            # count cover at mid
            cover = 0
            for s, e in intervals:
                if s - tol < mid < e + tol:
                    cover += 1
            # 如果该小段 coverage >= 2，记录其端点为实际分割点（将产生新的顶点）
            if cover >= 2:
                split_positions_per_edge[idx].add(a)
                split_positions_per_edge[idx].add(b)

    # --- 在每条原边上插入分割点，生成新的顶点序列（把重合端点显式化） ---
    new_pts = [tuple(np.round(poly[0], round_decimals))]  # 用 round 构造首点（避免浮点字典差异）
    n = poly.shape[0]
    for i in range(n):
        p = poly[i]
        q = poly[(i+1) % n]
        seg_pts = []

        # 对可能的每个裁剪器边，检查是否该多边形边与之共线并存在需要插入的 split positions
        for edge_idx, (is_h, is_v, ca, cb, intervals) in enumerate(projection_intervals):
            if is_h:
                y0 = ca[1]
                # 如果 p,q 均位于该水平线上（近似共线），考虑插点
                if abs(p[1] - y0) < tol and abs(q[1] - y0) < tol:
                    # 找到该边区间内需要插入的 x 值
                    s_min, s_max = min(p[0], q[0]), max(p[0], q[0])  # type:ignore
                    cand_xs = [x for x in split_positions_per_edge[edge_idx] if (s_min + tol) < x < (s_max - tol)]
                    # 计算沿边的参数 t 并按方向排序
                    if len(cand_xs) > 0:
                        if abs(q[0] - p[0]) < tol:
                            # 极端退化情况（非常短或数值问题），忽略
                            pass
                        else:
                            ts = [ (x - p[0]) / (q[0] - p[0]) for x in cand_xs ]
                            # 按 t 排序
                            for t, x in sorted(zip(ts, cand_xs), key=lambda it: it[0]):
                                if tol < t < 1 - tol:
                                    pt = p + t * (q - p)
                                    seg_pts.append(tuple(np.round(pt, round_decimals)))  # type:ignore
            elif is_v:
                x0 = ca[0]
                if abs(p[0] - x0) < tol and abs(q[0] - x0) < tol:
                    s_min, s_max = min(p[1], q[1]), max(p[1], q[1])  # type:ignore
                    cand_ys = [y for y in split_positions_per_edge[edge_idx] if (s_min + tol) < y < (s_max - tol)]
                    if len(cand_ys) > 0:
                        if abs(q[1] - p[1]) < tol:
                            pass
                        else:
                            ts = [ (y - p[1]) / (q[1] - p[1]) for y in cand_ys ]
                            for t, y in sorted(zip(ts, cand_ys), key=lambda it: it[0]):
                                if tol < t < 1 - tol:
                                    pt = p + t * (q - p)
                                    seg_pts.append(tuple(np.round(pt, round_decimals)))  # type:ignore

        # 将本段的插入点按从 p -> q 的方向去重排序后加入 new_pts（注意可能多个裁剪边贡献插点）
        # 首先按参数 t 排序（计算 t 的方式：若 q-p 沿 x 更显著则用 x 否则用 y）
        if seg_pts:
            # 从 p 到 q 的排序关键字：若 dx 大则按 x，否则按 y
            dx = abs(q[0] - p[0])
            dy = abs(q[1] - p[1])
            if dx >= dy:
                seg_pts_sorted = sorted(seg_pts, key=lambda pt: (pt[0] - p[0]) / (q[0] - p[0]) if abs(q[0]-p[0])>tol else 0.0)
            else:
                seg_pts_sorted = sorted(seg_pts, key=lambda pt: (pt[1] - p[1]) / (q[1] - p[1]) if abs(q[1]-p[1])>tol else 0.0)
            for spt in seg_pts_sorted:
                # 避免连续重复点
                if new_pts and np.allclose(np.array(new_pts[-1], dtype=float), np.array(spt, dtype=float), atol=10**(-round_decimals)):
                    continue
                new_pts.append(spt)

        # 最后加入 q（作为下条边的起点会重复，但稍后我们去重连续重复）
        q_t = tuple(np.round(q, round_decimals))
        if new_pts and np.allclose(np.array(new_pts[-1], dtype=float), np.array(q_t, dtype=float), atol=10**(-round_decimals)):
            # skip adding duplicate
            pass
        else:
            new_pts.append(q_t)

    # 去掉可能产生的连续重复点（数值相等或非常接近的）
    合并后 = []
    for pt in new_pts:
        if not 合并后 or (not np.allclose(np.array(合并后[-1]), np.array(pt), atol=10**(-round_decimals))):
            合并后.append(pt)
    新序列 = np.array(合并后, dtype=np.float64)

    # 如果首尾相同则删除尾部（便于索引逻辑）
    if 新序列.shape[0] > 1 and np.allclose(新序列[0], 新序列[-1], atol=tol):
        新序列 = 新序列[:-1]

    # --- 基于“重复顶点出现位置”来提取相邻重复区间作为候选子多边形 ---
    n2 = 新序列.shape[0]
    if n2 == 0:
        return []

    # 建立顶点->出现索引列表（使用四舍五入后的 tuple 作为 key，避免浮点精度问题）
    index_map = {}
    for i, p in enumerate(新序列):
        key = (round(float(p[0]), round_decimals), round(float(p[1]), round_decimals))
        index_map.setdefault(key, []).append(i)

    已使用 = [False] * n2
    子多边形集合 = []

    # 遍历每个出现超过一次的顶点，按相邻出现对提取闭合片段
    for key, occ in index_map.items():
        if len(occ) < 2:
            continue
        # 相邻对 (occ[k], occ[k+1]) 更倾向于产生最小的闭合片段
        for k in range(len(occ) - 1):
            i0 = occ[k]
            i1 = occ[k + 1]
            if i1 <= i0:
                continue
            # 若这段索引范围已被部分使用，则跳过（避免重复切分）
            if any(已使用[j] for j in range(i0, i1 + 1)):
                continue
            seg = 新序列[i0:i1 + 1]
            if seg.shape[0] >= 3:
                area = abs(_多边形有向面积(seg))
                if area > 面积阈:
                    子多边形集合.append(seg.copy())
                    for j in range(i0, i1 + 1):
                        已使用[j] = True

    # 最后把剩余未被覆盖的顶点尽量合并成一个环（如果能闭合并且面积足够大）
    # 找到所有未使用的索引，按顺序连成一段（可能需要加上从末尾到开头的环）
    未用索引 = [i for i, used in enumerate(已使用) if not used]
    if 未用索引:
        # 若这些索引构成连续区间（或一个循环片段），尝试提取之为一多边形
        # 找第一个未用索引 s, 然后按循环向前找到下一个未用索引，直到回到 s 或断开
        s = 未用索引[0]
        seq = []
        i = s
        while True:
            if not 已使用[i]:
                seq.append(tuple(新序列[i]))
                已使用[i] = True
            i = (i + 1) % n2
            if i == s:
                break
            # 如果走了一圈但都被标记，就结束
            if 已使用[i] and i == s:
                break
        seq_arr = np.array(seq, dtype=np.float64)
        if seq_arr.shape[0] >= 3 and abs(_多边形有向面积(seq_arr)) > 面积阈:
            子多边形集合.append(seq_arr)

    # 确保每个子多边形是闭合（首尾相同），并返回 np.array 列表
    结果 = []
    for p in 子多边形集合:
        if not np.allclose(p[0], p[-1], atol=tol):
            p = np.vstack([p, p[0]])
        结果.append(p)

    return 结果

def _多边形有向面积(poly):
    """返回带符号的有向面积（shoelace formula）；poly 为 (n,2) numpy 数组"""
    x = poly[:, 0]
    y = poly[:, 1]
    return 0.5 * np.dot(x, np.roll(y, -1)) - 0.5 * np.dot(y, np.roll(x, -1))

def 多边形相交(被裁剪多边形, 裁剪多边形):
    """
    Sutherland–Hodgman 多边形裁剪算法：
    依次用“裁剪多边形”的每一条边去裁剪“被裁剪多边形”，
    最终输出两者的交集多边形顶点序列（可能为空）。
    """
    输出多边形 = 被裁剪多边形               # 初始输出就是输入的被裁剪多边形
    for i in range(len(裁剪多边形)):        # 逐条遍历裁剪多边形的边
        裁剪边起点 = 裁剪多边形[i]           # 当前裁剪边的起点
        裁剪边终点 = 裁剪多边形[(i + 1) % len(裁剪多边形)]  # 当前裁剪边的终点（首尾相连）
        输入多边形 = 输出多边形              # 上一轮的输出作为这一轮的输入
        新输出多边形 = []                   # 本轮裁剪产生的新输出顶点列表

        # 如果输入为空（没有 any True），直接停止后续裁剪
        if not 输入多边形.any():
            break

        上一点 = 输入多边形[-1]              # 取输入多边形的“上一个顶点”（循环起点）
        for 当前点 in 输入多边形:            # 逐顶点扫描输入多边形
            # 情况 1：当前点在裁剪半平面内
            if _在内(当前点, 裁剪边起点, 裁剪边终点):
                # 若上一点不在内，则边 (上一点->当前点) 与裁剪边有交点，先加入交点
                if not _在内(上一点, 裁剪边起点, 裁剪边终点):
                    新输出多边形.append(_交点(上一点, 当前点, 裁剪边起点, 裁剪边终点))
                # 再把当前点加入输出
                新输出多边形.append(当前点)
            # 情况 2：当前点在外，但上一点在内，则 (上一点->当前点) 与裁剪边有交点，加入交点
            elif _在内(上一点, 裁剪边起点, 裁剪边终点):
                新输出多边形.append(_交点(上一点, 当前点, 裁剪边起点, 裁剪边终点))
            # 更新“上一点”为当前点，继续扫描下一条边
            上一点 = 当前点

        # 把本轮收集到的输出顶点转成 NumPy 数组，供下一轮使用
        输出多边形 = np.array(新输出多边形)

    return 输出多边形

def _在内(点, 边点1, 边点2):
    """
    判断“点”是否在由有向边 (边点1->边点2) 左侧（左侧表示在“内侧”），
    通过 2D 叉积正负判断： (边点2-边点1) × (点-边点1) > 0 视为在内。
    """
    return (边点2[0] - 边点1[0]) * (点[1] - 边点1[1]) > (边点2[1] - 边点1[1]) * (点[0] - 边点1[0])

def _交点(线段起点, 线段终点, 边点1, 边点2):
    """
    计算线段 (线段起点->线段终点) 与裁剪边 (边点1->边点2) 的交点（两直线相交点）。
    采用行列式/叉积形式的参数方程求交：
      直线1: P = 线段起点 + t*(线段终点-线段起点)
      直线2: Q = 边点1   + u*(边点2  -边点1)
    令 P==Q 解得交点坐标；当两直线平行(n3==0)时，返回线段终点（与原实现一致）。
    """
    向量_剪边 = np.array([边点1[0] - 边点2[0], 边点1[1] - 边点2[1]])         # dc = p1 - p2
    向量_线段 = np.array([线段起点[0] - 线段终点[0], 线段起点[1] - 线段终点[1]]) # dp = s - e
    面积项1 = 边点1[0] * 边点2[1] - 边点1[1] * 边点2[0]                      # n1 = cross(p1,p2) 的标量形式
    面积项2 = 线段起点[0] * 线段终点[1] - 线段起点[1] * 线段终点[0]            # n2 = cross(s,e)
    分母 = 向量_剪边[0] * 向量_线段[1] - 向量_剪边[1] * 向量_线段[0]            # n3 = cross(dc,dp)

    if 分母 == 0:                          # 平行或重合（没有唯一交点）
        return 线段终点                    # 与原逻辑一致：直接返回“终点”

    # 交点坐标的显式解（来源于两直线的代数解）
    x = (面积项1 * 向量_线段[0] - 面积项2 * 向量_剪边[0]) / 分母
    y = (面积项1 * 向量_线段[1] - 面积项2 * 向量_剪边[1]) / 分母
    return np.array([x, y])

def 多边形面积(多边形):
    """
    用“鞋带公式”(shoelace) 计算简单多边形面积。
    面积 = 0.5 * |Σ(x_i * y_{i+1} - y_i * x_{i+1})|
    """
    x = 多边形[:, 0]                                  # 取所有 x 坐标
    y = 多边形[:, 1]                                  # 取所有 y 坐标
    # 通过点积实现 Σ(x_i*y_{i+1}) 与 Σ(y_i*x_{i+1})，并做绝对值与 0.5 系数
    return 0.5 * np.abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
