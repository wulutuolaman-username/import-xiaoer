def check_material_image_name(image):
    return (
        # 如果是MMD_tools插件固有贴图，无需后续重命名
        any(image.name.startswith(f"toon{i:02d}.bmp") for i in range(1, 11)) or
        # 如果是预设通用贴图，无需后续重命名
        image.name.startswith("Avatar_Tex_MetalMap.tga") or image.name.startswith("hair_s.bmp") or
        # 如果是解包贴图已含有角色英文名，无需后续重命名
        image.name.startswith("Avatar_") or "_FaceMap" in image.name or  # 崩坏三、原神、崩坏：星穹铁道的解包贴图
        "_Body_Map" in image.name or image.name.startswith("Eff_MatCap_") or  # 绝区零的解包贴图，下一行也是
        any(image.name.endswith(suffix) for suffix in ["_Body_A", "_Body_D", "_Body_M", "_Body_N", "_Face_D", "_Hair_A", "_Hair_D", "_Hair_M", "_Hair_N"]) or
        image.name.startswith("T_R2T1") and "Md10011" in image.name  # 鸣潮的解包贴图
    )
