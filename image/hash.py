import bpy
import numpy as np

# 全局导入 imagehash
global imagehash
try:
    import imagehash
except ImportError:
    pass

try:
    from PIL import Image
except ImportError:
    pass

# 计算图像哈希值
def get_image_hash(bpy_image):
    # 创建临时图像并缩放到目标尺寸
    temp_image = bpy_image.copy()
    """将 Blender 图像转换为 PIL 图像（强制转为 RGB）"""
    pixels = np.array(temp_image.pixels[:], dtype=np.float32)
    width, height = temp_image.size
    pixels = (pixels * 255).astype(np.uint8)
    pixels = pixels.reshape(height, width, 4)
    # 去除 Alpha 通道（如果存在）
    has_alpha = False
    if pixels.shape[2] == 4:
        pixels = pixels[:, :, :3]  # 仅保留 RGB 通道
        has_alpha = True
    pil_image = Image.fromarray(pixels, 'RGB').convert('L')  # 转换为 RGB 并生成灰度图像
    hash_val = imagehash.phash(pil_image)
    # 释放临时图像
    bpy.data.images.remove(temp_image)
    return hash_val,has_alpha