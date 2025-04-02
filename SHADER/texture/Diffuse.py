def is_diffuse(image_name):
    return any(keyword in image_name for keyword in ['.png', '.jpg', '.jpeg', '.tga', '.exr', '.tif', '.tiff'])

def diffuse_texture(self,material,diffuse_images):
    original_image = None  # 先初始化
    diffuse_image = None  # 先初始化
    for node in material.node_tree.nodes:
        if node.type == 'TEX_IMAGE' and is_diffuse(node.image.name):
            original_image = node.image  # 获取原始贴图
            try:
                if diffuse_images:  # 如果开启了匹配贴图
                    diffuse_image = diffuse_images[original_image]  # 匹配基础色贴图
                else: diffuse_image = original_image  # 如果没有开启匹配贴图，那就直接使用原始贴图
            except:
                self.report({"WARNING"},f'材质Material["{material.name}"]获取匹配贴图调试点检测到错误，若正常输入贴图请忽略此条警告信息')
            return node,original_image,diffuse_image
    if not original_image:  # 薇塔的眼睛2材质没有基础贴图
        return None,None,None