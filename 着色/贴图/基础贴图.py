# coding: utf-8

def 筛选贴图(图像名称):
    return any(keyword in 图像名称 for keyword in ['.png', '.jpg', '.jpeg', '.tga', '.exr', '.tif', '.tiff'])

def 筛选基础贴图(图像名称):
    return (  # 1.0.3迁移：筛选基础贴图
            "_Color" in 图像名称 or  # 崩坏基础贴图
            "_Diffuse" in 图像名称 or  # 原神基础贴图
            "_D" in 图像名称  # 绝区零、鸣潮基础贴图
    )

def 匹配基础贴图(self, 材质, 匹配贴图):
    for 图像节点 in 材质.node_tree.nodes:
        if 图像节点.type == 'TEX_IMAGE' and 筛选贴图(图像节点.image.name):
            原始贴图 = 图像节点.image  # 获取原始贴图
            # 1.03改进
            if not 原始贴图 or 原始贴图 not in 匹配贴图:  # 薇塔的眼睛2材质没有基础贴图
                return 图像节点, None
            # try:
            if 匹配贴图 and 原始贴图 in 匹配贴图:  # 如果开启了匹配贴图
                基础贴图 = 匹配贴图[原始贴图]  # 匹配基础色贴图
                if not 基础贴图:
                    基础贴图 = 原始贴图  # 如果没有开启匹配贴图，那就直接使用原始贴图
                    self.report({"WARNING"}, f'材质Material["{材质.name}"]没有匹配贴图')
                return 图像节点, 基础贴图
            # except:
                # self.report({"WARNING"},f'材质Material["{材质.name}"]获取匹配贴图调试点检测到错误，若正常输入贴图请忽略此条警告信息')
                # return 图像节点, 基础贴图
    return None, None  # 薇塔的眼睛2材质没有基础贴图
