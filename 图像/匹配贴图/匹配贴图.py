import math
import numpy as np
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from ...通用.信息 import 报告信息

global Image  #  1.0.1更新：不再直接导入PIL
try:
    from PIL import Image
except ImportError:
    pass

global imagehash
try:
    import imagehash
except ImportError:
    pass

哈希尺寸 = 32

def 匹配模型贴图(原始贴图, 原始名称):
    try:
        # if 原始贴图 not in 匹配贴图:  # 跳过与导入贴图同名的贴图
        像素1 = np.array(原始贴图)
        尺寸 = 原始贴图.size
        透明 = 像素1[..., 3] == 0  # 仅检查第4个通道（A）
        像素1[透明] = [0, 0, 0, 0]  # 1.1.0应用透明遮罩
        # 起 = time.perf_counter()
        # 生成RGB三个通道图像
        红图 = Image.fromarray(像素1[..., 0], 'L')
        绿图 = Image.fromarray(像素1[..., 1], 'L')
        蓝图 = Image.fromarray(像素1[..., 2], 'L')
        # 分别生成哈希
        哈希R1 = imagehash.phash(红图, 哈希尺寸)
        哈希G1 = imagehash.phash(绿图, 哈希尺寸)
        哈希B1 = imagehash.phash(蓝图, 哈希尺寸)
        # 终 = time.perf_counter()
        # self.report({"INFO"}, f"{终 - 起:.6f} 秒 {datetime.datetime.now()}")
        return 原始贴图, 原始名称, 哈希R1, 哈希G1, 哈希B1, 透明, 尺寸
    except Exception as e:
        报告信息(None, '异常', f"匹配' {原始名称} '出错: {e}")
        # self.report({"ERROR"}, f"匹配' {原始名称} '出错: {e}")
        return None, None, None, None, None, None, None


def 尝试匹配贴图(导入贴图, 导入名称, 原始名称, 透明, 尺寸):
    try:
        缩放图像 = 导入贴图.copy().resize(尺寸, Image.NEAREST)  # 应用透明遮罩必须相同分辨率
        像素2 = np.array(缩放图像)
        像素2[透明] = [0, 0, 0, 0]  # 1.1.0应用透明遮罩
        # # 图像遮罩2 = Image.fromarray(像素2, 'RGBA')
        # # 图像遮罩2.save(os.path.join(输出目录, f"{原始名称} 尝试匹配贴图 {导入名称}"))
        # 起 = time.perf_counter()
        # 生成RGB三个通道图像
        红图 = Image.fromarray(像素2[..., 0], 'L')
        绿图 = Image.fromarray(像素2[..., 1], 'L')
        蓝图 = Image.fromarray(像素2[..., 2], 'L')
        # 分别生成哈希
        哈希R2 = imagehash.phash(红图, 哈希尺寸)
        哈希G2 = imagehash.phash(绿图, 哈希尺寸)
        哈希B2 = imagehash.phash(蓝图, 哈希尺寸)
        # 终 = time.perf_counter()
        # self.report({"INFO"}, f"{终 - 起:.6f} 秒 {datetime.datetime.now()}")
        return 导入贴图, 导入名称, 哈希R2, 哈希G2, 哈希B2
    except Exception as e:
        报告信息(None, '异常', f"匹配' {导入名称} '出错: {e}")
        # self.report({"ERROR"}, f"匹配' {导入名称} '出错: {e}")
        return None, None, None, None, None


def 并行匹配全部贴图(模型贴图, 基础贴图):
    模型贴图匹配过程 = defaultdict(dict)  # 使用defaultdict自动初始化嵌套字典
    匹配贴图 = {}  # 记录原始贴图和导入贴图的匹配关系，后续引用此字典进行匹配
    with ThreadPoolExecutor(max_workers=len(模型贴图)) as 执行器1:
        匹配任务1 = [执行器1.submit(匹配模型贴图, 原始贴图, 原始名称) for 原始贴图, 原始名称 in 模型贴图]
        for 任务1 in 匹配任务1:
            汉明距离 = {}
            原始贴图, 原始名称, 哈希R1, 哈希G1, 哈希B1, 透明, 尺寸 = 任务1.result()
            with ThreadPoolExecutor(max_workers=len(基础贴图)) as 执行器2:
                匹配任务2 = [执行器2.submit(尝试匹配贴图, 导入贴图, 导入名称, 原始名称, 透明, 尺寸) for
                             导入贴图, 导入名称 in 基础贴图]
                for 任务2 in 匹配任务2:
                    导入贴图, 导入名称, 哈希R2, 哈希G2, 哈希B2 = 任务2.result()
                    if 哈希R1 and 哈希R2 and 哈希G1 and 哈希G2 and 哈希B1 and 哈希B2:  # 4.2版本报错TypeError: unsupported operand type(s) for -: 'NoneType' and 'NoneType'
                        距离相乘 = (哈希R1 - 哈希R2) * (哈希G1 - 哈希G2) * (哈希B1 - 哈希B2)
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

def 匹配模型贴图和导入贴图(模型, 模型贴图, 基础贴图):
    if len(模型贴图) > 0 and len(基础贴图) > 0:  # 1.1.0选择模型路径没有需要哈希的导入贴图则跳过
        # Blender API 阻塞点（无法在子线程并行）,需要全部图像转为PIL图像再进行纯python计算
        # 1.1.0多线程并行匹配贴图
        匹配贴图, 模型贴图匹配过程 = 并行匹配全部贴图(模型贴图, 基础贴图)
        if 模型 and len(模型贴图) > 1:  # 排除深度检索
            模型.小二预设模板.完成匹配贴图 = True
        return 匹配贴图, 模型贴图匹配过程
    return None, None