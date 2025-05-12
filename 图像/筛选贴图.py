# coding: utf-8

def 筛选图像(图像):
    return (
        # MMD_tools插件固有贴图
        any(图像.name.startswith(f"toon{i:02d}.bmp") for i in range(1, 11)) or
        # 预设通用金属和高光贴图
        图像.name.startswith("Avatar_Tex_MetalMap.tga") or 图像.name.startswith("hair_s.bmp") or
        # 解包贴图已含有角色英文名
        图像.name.startswith("Avatar_") or "_FaceMap" in 图像.name or  # 崩坏三、原神、崩坏：星穹铁道的解包贴图
        "_Body_Map" in 图像.name or 图像.name.startswith("Eff_MatCap_") or  # 绝区零的解包贴图，下一行也是
        any(图像.name.endswith(suffix) for suffix in ["_Body_A", "_Body_D", "_Body_M", "_Body_N", "_Face_D", "_Hair_A", "_Hair_D", "_Hair_M", "_Hair_N"]) or
        图像.name.startswith("T_R2T1") and "Md10011" in 图像.name  # 鸣潮的解包贴图
    )
