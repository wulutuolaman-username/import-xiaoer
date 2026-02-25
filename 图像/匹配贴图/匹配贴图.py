import math, numpy as np
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from ...通用.信息 import *
from ...指针 import *

global Image, ImageFilter  #  1.0.1更新：不再直接导入PIL
try:
    from PIL import Image, ImageFilter
except ImportError:
    Image, ImageFilter = (None,) * 2
    pass

global imagehash
try:
    import imagehash
except ImportError:
    imagehash = None
    pass

global cv2
try:
    import cv2
except ImportError:
    cv2 = None
    pass

# 1.1.0多线程并行匹配贴图
# Blender API 阻塞点（无法在子线程并行）,需要全部图像转为PIL图像再进行纯python计算
# 1.2.0新增边缘算法解决像素算法爻光衣N贴图匹配错误的问题

哈希尺寸 = 32

global 算法

def 像素算法(原始名称, 像素):
    """ 爻光衣N贴图匹配失败 """
    try:
        # 生成RGB三个通道图像
        红图 = Image.fromarray(像素[..., 0], 'L')
        绿图 = Image.fromarray(像素[..., 1], 'L')
        蓝图 = Image.fromarray(像素[..., 2], 'L')
        # 分别生成哈希
        哈希R = imagehash.phash(红图, 哈希尺寸)
        哈希G = imagehash.phash(绿图, 哈希尺寸)
        哈希B = imagehash.phash(蓝图, 哈希尺寸)
        return 哈希R, 哈希G, 哈希B
    except Exception as e:
        输出错误(None, e, f"像素算法匹配' {原始名称} '出错")
        return (None,) * 3
# 1.2.0新增边缘算法
def 边缘算法(原始名称, 像素):
    try:
        if 像素.shape[2] == 4:  # RGBA
            灰度 = np.dot(像素[..., :3], [0.299, 0.587, 0.114])
        else:
            灰度 = np.dot(像素, [0.299, 0.587, 0.114])
        灰度 = 灰度.astype(np.uint8)

        # # Canny边缘检测  # 颜赤贴图匹配错误
        # 边缘 = cv2.Canny(灰度, 50, 150)
        # 边缘图 = Image.fromarray(边缘, 'L')
        # # 生成边缘哈希
        # 边缘哈希 = imagehash.phash(边缘图, 哈希尺寸)
        # return 边缘哈希

        # Sobel梯度  # Sobel 可以提取边缘
        梯度X = cv2.Sobel(灰度, cv2.CV_64F, 1, 0, ksize=3)
        梯度Y = cv2.Sobel(灰度, cv2.CV_64F, 0, 1, ksize=3)
        梯度 = np.sqrt(梯度X ** 2 + 梯度Y ** 2)
        梯度 = np.uint8(np.clip(梯度, 0, 255))
        梯度图 = Image.fromarray(梯度, 'L')
        梯度哈希 = imagehash.phash(梯度图, 哈希尺寸)
        return 梯度哈希
    except Exception as e:
        输出错误(None, e, f"边缘算法匹配' {原始名称} '出错")
        return None

def 匹配模型贴图(原始贴图, 原始名称):
    # try:
        # if 原始贴图 not in 匹配贴图:  # 跳过与导入贴图同名的贴图
        像素1 = np.array(原始贴图)
        尺寸 = 原始贴图.size
        透明 = 像素1[..., 3] == 0  # 仅检查第4个通道（A）
        像素1[透明] = [0, 0, 0, 0]  # 1.1.0应用透明遮罩

        if 算法 == '像素':
            return 原始贴图, 原始名称, 像素算法(原始名称, 像素1), 透明, 尺寸
        if 算法 == '边缘':
            return 原始贴图, 原始名称, 边缘算法(原始名称, 像素1), 透明, 尺寸

def 尝试匹配贴图(导入贴图, 导入名称, 原始名称, 透明, 尺寸):
    # try:
        # 应用透明遮罩必须相同分辨率
        缩放图像 = 导入贴图.copy().resize(尺寸, Image.NEAREST)  # type:ignore
        像素2 = np.array(缩放图像)
        像素2[透明] = [0, 0, 0, 0]  # 1.1.0应用透明遮罩

        if 算法 == '像素':
            return 导入贴图, 导入名称, 像素算法(原始名称, 像素2)
        if 算法 == '边缘':
            return 导入贴图, 导入名称, 边缘算法(原始名称, 像素2)

def 并行匹配全部贴图(模型贴图, 基础贴图):
    模型贴图匹配过程 = defaultdict(dict)  # 使用defaultdict自动初始化嵌套字典
    匹配贴图 = {}  # 记录原始贴图和导入贴图的匹配关系，后续引用此字典进行匹配
    with ThreadPoolExecutor(max_workers=len(模型贴图)) as 执行器1:
        匹配任务1 = [执行器1.submit(匹配模型贴图, 原始贴图, 原始名称) for 原始贴图, 原始名称 in 模型贴图]
        for 任务1 in 匹配任务1:
            汉明距离 = {}
            原始贴图, 原始名称, 哈希1, 透明, 尺寸 = 任务1.result()
            # 原始贴图, 原始名称, 哈希R1, 哈希G1, 哈希B1, 透明, 尺寸 = 任务1.result()
            with ThreadPoolExecutor(max_workers=len(基础贴图)) as 执行器2:
                匹配任务2 = [执行器2.submit(尝试匹配贴图, 导入贴图, 导入名称, 原始名称, 透明, 尺寸) for 导入贴图, 导入名称 in 基础贴图]
                for 任务2 in 匹配任务2:
                    导入贴图, 导入名称, 哈希2 = 任务2.result()
                    # 导入贴图, 导入名称, 哈希R2, 哈希G2, 哈希B2 = 任务2.result()
                    if 哈希1 and 哈希2:  # 4.2版本报错TypeError: unsupported operand type(s) for -: 'NoneType' and 'NoneType'
                    # if 哈希R1 and 哈希R2 and 哈希G1 and 哈希G2 and 哈希B1 and 哈希B2:  # 4.2版本报错TypeError: unsupported operand type(s) for -: 'NoneType' and 'NoneType'
                        # print(原始名称, 导入名称, 哈希R1 - 哈希R2, 哈希G1 - 哈希G2, 哈希B1 - 哈希B2)
                        距离相乘 = math.inf
                        if 算法 == '像素':
                            距离相乘 = (哈希1[0] - 哈希2[0]) * (哈希1[1] - 哈希2[1]) * (哈希1[2] - 哈希2[2])
                            # 距离相乘 = (哈希R1 - 哈希R2) * (哈希G1 - 哈希G2) * (哈希B1 - 哈希B2)
                        if 算法 == '边缘':
                            距离相乘 = 哈希1 - 哈希2
                        汉明距离[距离相乘] = 导入名称
                        if 距离相乘 < 模型贴图匹配过程[原始名称].get(导入名称, math.inf):  # 1.1.0防止大的覆盖小的
                            模型贴图匹配过程[原始名称][导入名称] = 距离相乘  # 使用字典嵌套存储所有匹配结果
                        print(原始名称, 导入名称, 距离相乘)
            最小距离 = min(汉明距离)
            print(f'{汉明距离}最小距离{最小距离}')
            导入名称 = 汉明距离[最小距离]
            模型贴图匹配过程[原始名称][导入名称] = 最小距离  # 1.1.0查找贴图文件夹深度检索
            匹配贴图[原始名称] = 导入名称
    return 匹配贴图, dict(模型贴图匹配过程)  # 转为普通字典返回

def 匹配模型贴图和导入贴图(模型: 小二物体 | None, 模型贴图, 基础贴图, 匹配方式='像素'):
    """ 默认通过像素算法匹配贴图 """
    if len(模型贴图) > 0 and len(基础贴图) > 0:  # 1.1.0选择模型路径没有需要哈希的导入贴图则跳过
        global 算法
        算法 = 匹配方式
        匹配贴图, 模型贴图匹配过程 = 并行匹配全部贴图(模型贴图, 基础贴图)
        if 模型 and len(模型贴图) > 1:  # 排除深度检索
            模型.小二预设模板.完成匹配贴图 = True
        return 匹配贴图, 模型贴图匹配过程
    return None, None