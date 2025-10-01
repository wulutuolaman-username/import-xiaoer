# coding: utf-8

import numpy as np

# 全局导入 imagehash
global imagehash
try:
    # import imagehash
    from imagehash import ImageHash
except ImportError:
    pass

global Image  #  1.0.1更新：不再直接导入PIL
try:
    from PIL import Image
except ImportError:
    pass

# 计算图像哈希值
def 哈希图像(self, 图像, 像素, 哈希尺寸=32, 高频因子=4):
    # # type: (Image.Image, int, int) -> ImageHash
    # """
    # Perceptual Hash computation.
    #
    # Implementation follows https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    #
    # @image must be a PIL instance.
    # """
    # if 哈希尺寸 < 2:
    #     raise ValueError('Hash size must be greater than or equal to 2')
    #
    # import scipy.fftpack
    #
    # try:
    #     ANTIALIAS = Image.Resampling.LANCZOS
    # except AttributeError:
    #     # deprecated in pillow 10
    #     # https://pillow.readthedocs.io/en/stable/deprecations.html
    #     ANTIALIAS = Image.ANTIALIAS
    #
    # img_size = 哈希尺寸 * 高频因子
    # 图像 = 图像.resize((img_size, img_size), ANTIALIAS)
    # 像素 = np.asarray(图像)
    # dct = scipy.fftpack.dct(scipy.fftpack.dct(像素, axis=0), axis=1)
    # dctlowfreq = dct[:哈希尺寸, :哈希尺寸]
    # med = np.median(dctlowfreq)
    # diff = dctlowfreq > med
    # return ImageHash(diff)
    try:
        """将 Blender 图像转换为 PIL 图像（强制转为 RGB）"""
        if 像素.shape[2] == 4:  # RGBA格式
            像素 = 像素[..., :3]  # 1.1.0取前三个通道(RGB)
        PIL图像 = Image.fromarray(像素, 'RGB')  # 转换为 RGB
        哈希 = imagehash.phash(PIL图像, 哈希尺寸)
        if 哈希:
            return 哈希
        else:
            self.report({"WARNING"}, f'{图像.name}哈希计算为空值')
    except:
        self.report({"WARNING"}, f'{图像.name}哈希失败')
        return None