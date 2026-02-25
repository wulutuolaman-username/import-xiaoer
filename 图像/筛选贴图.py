# coding: utf-8

import os
from ..通用.剪尾 import 剪去后缀

def 筛选图像(图像):
    """ MMD_TOOLs插件固有贴图、预设通用金属和高光贴图、已含有角色英文名的解包贴图 """
    if 图像.filepath:
        名称, 后缀 = 剪去后缀(os.path.basename(图像.filepath))
    else:
        名称, 后缀 = 剪去后缀(图像.name)
    名称, 扩展 = os.path.splitext(名称)
    return (
        # MMD_tools插件固有贴图
        any(名称.startswith(f"toon{i:02d}") for i in range(1, 11)) or
        # 预设通用金属和高光贴图
        名称.startswith("Avatar_Tex_MetalMap") or 名称.startswith("hair_s") or
        # 解包贴图已含有角色英文名
        名称.startswith("Avatar_") or "_FaceMap" in 名称 or  # 崩坏三、原神、崩坏：星穹铁道的解包贴图
        any(名称.endswith(f"_{后}") for 后 in ["A","D","M","N"]) or 名称.startswith("Eff_MatCap_") or "_SDF" in 名称 or  # 绝区零的解包贴图  # 1.1.0优化检查方法
        名称.startswith("MI_") or 名称.startswith("R2T1") or 名称.startswith("T_NHT1") or (名称.startswith("T_R2T1") and "Md10011" in 名称)  # 鸣潮的解包贴图  # 1.1.0增加"MI_"、"R2T1"、"T_NHT1"
    )

def 确认贴图(图像名):
    """ 只导入'.png', '.jpg', '.jpeg', '.tga', '.exr', '.tif', '.tiff'格式的贴图 """
    return any(图像名.endswith(后) for 后 in ['.png', '.jpg', '.jpeg', '.tga', '.exr', '.tif', '.tiff'])