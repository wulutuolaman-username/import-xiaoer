import bpy
import os
from ..SHADER.texture.Diffuse import is_diffuse
from ..image.hash import get_image_hash

# 导入解包贴图，于原神贴图进行哈希匹配
def import_and_match(self,prefs,image_path):
    original_images = []  # 记录原始贴图信息
    alpha_images = []  # 记录带有alpha通道的贴图
    if prefs.auto_match_image:
        for image in bpy.data.images:
            # self.report({"INFO"}, f'记录原始贴图“{image.name}”')
            original_images.append(image)
        # 生成原始贴图的哈希值
        original_hashes = {}
        for img in original_images:
            if is_diffuse(img.name):
                hash_1 ,has_alpha = get_image_hash(img)
                if hash_1:
                    # self.report({"INFO"}, f'成功哈希“{img.name}”')
                    original_hashes[hash_1] = img
                if has_alpha:  # 如果存在alpha通道
                    alpha_images.append(img)
    # 导入贴图
    self.report({"INFO"}, f"导入贴图" + str(image_path))
    imported_images = []
    # 遍历目录下的所有文件
    for imagename in os.listdir(image_path):
        if is_diffuse(imagename):
            imagepath = os.path.join(image_path, imagename)
            # 导入图像到 Blender
            try:
                image = bpy.data.images.load(imagepath)
                imported_images.append(image)
                # self.report({"INFO"}, f"导入成功：" + str(imagename))
            except Exception as e:
                self.report({"WARNING"}, f"导入失败：" + str(imagename))
    if prefs.auto_match_image:  # 如果开启了自动匹配贴图
        diffuse_images = {}  # 记录原始贴图和解包贴图的匹配信息，后续引用此字典进行匹配
        for img in imported_images:
            if (  # 筛选基础贴图
                    "_Color" in img.name or  # 崩坏基础贴图
                    "_Diffuse" in img.name or # 原神基础贴图
                    "_D" in img.name  # 绝区零、鸣潮基础贴图
            ):
                # get_image_hash(img, self)
                hash_2 ,has_alpha = get_image_hash(img)
                if hash_2 :
                    for hash_1 in original_hashes:
                        if hash_1 - hash_2 <= prefs.Hamming_distance:  # 汉明距离^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                            # self.report({"INFO"}, f'成功哈希“{img.name}”')
                            original_image = original_hashes[hash_1]
                            self.report({"INFO"}, f'原始贴图“{original_image.name}”匹配贴图“{img.name}”')
                            diffuse_images[original_image] = img  # 记录原始贴图和解包贴图的匹配信息，后续引用此字典进行匹配
                if has_alpha:  # 如果存在alpha通道
                    alpha_images.append(img)
        for img in original_images:
            if img not in diffuse_images:  # 如果原始贴图没有匹配到解包贴图
                try:  # 尝试复制已有的匹配
                    original_name = img.name.replace("+","")
                    original_image = bpy.data.images[original_name]
                    diffuse_image =  diffuse_images[original_image]
                    self.report({"INFO"}, f'原始贴图“{img.name}”匹配贴图“{diffuse_image.name}”')
                    diffuse_images[img] = diffuse_image  # 记录原始贴图和解包贴图的匹配信息，后续引用此字典进行匹配
                except:
                    pass
        # self.report({"INFO"}, f"alpha_images:\n" + "\n".join(image.name for image in alpha_images))
        return diffuse_images,alpha_images
    else:  # 如果关闭了自动匹配贴图
        return None,None