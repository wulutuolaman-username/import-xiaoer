# coding: utf-8

import bpy
import numpy as np

# 全局导入 imagehash
global imagehash
try:
    import imagehash
except ImportError:
    pass

global Image  #  1.01更新：不再直接导入PIL
try:
    from PIL import Image
except ImportError:
    pass

# 计算图像哈希值
def 哈希图像(图像):
    # 创建临时图像并缩放到目标尺寸
    临时图像 = 图像.copy()
    """将 Blender 图像转换为 PIL 图像（强制转为 RGB）"""
    像素 = np.array(临时图像.pixels[:], dtype=np.float32)
    宽, 高 = 临时图像.size
    像素 = (像素 * 255).astype(np.uint8)
    像素 = 像素.reshape(高, 宽, 4)
    # 去除 Alpha 通道（如果存在）
    有alpha = False
    if 像素.shape[2] == 4:
        像素 = 像素[:, :, :3]  # 仅保留 RGB 通道
        有alpha = True
    PIL图像 = Image.fromarray(像素, 'RGB').convert('L')  # 转换为 RGB 并生成灰度图像
    哈希 = imagehash.phash(PIL图像)
    # 释放临时图像
    bpy.data.images.remove(临时图像)
    return 哈希,有alpha