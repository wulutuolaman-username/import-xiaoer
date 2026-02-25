import bpy
import numpy as np
from ..偏好.偏好设置 import 小二偏好
global Image  #  1.0.1更新：不再直接导入PIL
try:
    from PIL import Image
except ImportError:
    Image = None
    pass

def 获取像素(self, 图像):
    # Blender 的 image.pixels 始终返回 RGBA 格式（即使没有 Alpha 通道，也会填充 1.0 或 255）。
    # 因此，reshape(高, 宽, 4) 是安全的，不会凭空增加通道，而是按 Blender 的默认数据格式解析。
    if 图像.pixels:
        临时图像 = 图像.copy()  # 必须使用副本，不能修改原数据
        临时图像.scale(512, 512)  # 缩放图像减少获取像素耗时，显著减少总用时
        # 起 = time.perf_counter()
        像素 = np.array(临时图像.pixels[:], dtype=np.float32)  # 耗时占比最高
        # 终 = time.perf_counter()
        # self.report({"INFO"}, f"{图像.name} 像素 = np.array(临时图像.pixels[:], dtype=np.float32)运行时间: {终 - 起:.6f} 秒")
        宽, 高 = 临时图像.size
        bpy.data.images.remove(临时图像)
        像素 = (像素 * 255).astype(np.uint8)
        像素 = 像素.reshape(高, 宽, 4)
        像素 = np.flipud(像素)  # 1.1.0垂直翻转图像（解决Blender的Y轴方向问题）
        if np.all(像素 == 像素[0, 0]):  # 1.1.0纯色贴图不做哈希运算
            self.report({"WARNING"}, f'“{图像.name}”为纯色贴图')
            return np.array([])  # 返回空数组，使 像素.any() 返回 False
        return 像素
    self.report({"WARNING"}, f'“{图像.name}”无像素')
    return np.array([])  # 返回空数组，使 像素.any() 返回 False

def 检查透明(偏好:小二偏好, 图像, 像素, 透明贴图):
    if 像素.ndim == 3 and 像素.shape[2] == 4:  # 确保是RGBA格式
        像素 = np.flipud(像素)  # 1.1.0再次垂直翻转图像（解决像素处理时翻转Y轴）
        新图 = Image.fromarray(像素, 'RGBA')
        # 应用透明遮罩必须相同分辨率
        缩放图像 = 新图.resize((偏好.检测透明分辨率, 偏好.检测透明分辨率), Image.NEAREST)  # type:ignore
        像素 = np.array(缩放图像)
        alpha = 像素[..., 3]  # 提取Alpha通道
        透明阈值 = 250
        if np.any(alpha < 透明阈值):  # 比not np.all(alpha==255)更高效
            y坐标, x坐标 = np.where(alpha < 透明阈值)  # 艾梅莉埃的体材质(alpha < 250)  # 长夜月不使用
            透明像素点 = {(int(x), int(y)) for x, y in zip(x坐标, y坐标)}
            # print(图像.name, '透明像素点：', 透明像素点)
            # print(len(透明像素点), type(len(透明像素点)), 偏好.检测透明分辨率 ** 2, type(偏好.检测透明分辨率 ** 2))
            完全透明 = 20
            # if np.count_nonzero(alpha < 完全透明) / 偏好.检测透明分辨率 ** 2 > 0.5:  # 如果基础贴图大面积透明不建议开启  # 菈乌玛头发贴图约一半透明  # 哥伦比娅头发贴图透明阈值需提高到20
            #     透明贴图[图像].append(None)
            #     透明贴图[图像].append(None)
            # else:
            y坐标, x坐标 = np.where(alpha < 完全透明)
            完全透明像素点 = {(int(x), int(y)) for x, y in zip(x坐标, y坐标)}
            if np.count_nonzero(alpha < 透明阈值) / 偏好.检测透明分辨率 ** 2 > 0.5:  # 黄泉贴图大面积半透明(alpha约为131)
                透明贴图[图像].append(完全透明像素点)
            else:
                透明贴图[图像].append(透明像素点)
            透明贴图[图像].append(完全透明像素点)
            # print(透明贴图)
            return True  # 1.1.0返回透明像素的坐标
    return False  # 无Alpha通道或完全不透明