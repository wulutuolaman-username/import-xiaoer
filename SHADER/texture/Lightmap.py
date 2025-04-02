import bpy
import re

def lightmap_texture(game,diffuse_image):
    if diffuse_image.name[-3:].isdigit():  # 如果有副本后缀
        diffuse_image.name = diffuse_image.name[:-4]
###################################################################################################
    if game == "崩坏三":
        if "Color" in diffuse_image.name:
            lightmap_name = diffuse_image.name.replace("Color", "LightMap")
            for img in bpy.data.images:
                if img.name.lower() == lightmap_name.lower():  # 忽略大小写
                    return img
###################################################################################################
    if game == "原神":
        if "Diffuse" in diffuse_image.name:
            lightmap_image = bpy.data.images[diffuse_image.name.replace("Diffuse", "Lightmap")]
            return lightmap_image
        else:
            return None
###################################################################################################
    if game == "崩坏：星穹铁道":
        # 新正则表达式结构说明：
        # ^(.*_\d{2})_       -> 前缀包含两位数字 (如 Avatar_Fugue_00)
        # ([^_]+)            -> 部件类型 (Body/Hair/Tail等)
        # _Color(.*)\.png$   -> Color及其后缀
        match = re.match(r'^(.*_\d{2})_([^_]+)_Color(.*)\.png$', diffuse_image.name)
        if match:
            prefix, part_type, color_suffix = match.groups()
            # 处理LightMap后缀：仅当Color后缀以_L结尾时保留
            split_parts = [p for p in color_suffix.split('_') if p]
            last_part = split_parts[-1] if split_parts else ''
            lightmap_suffix = f"_{last_part}" if last_part == 'L' else ''
            lightmap_name = f"{prefix}_{part_type}_LightMap{lightmap_suffix}.png"
            for img in bpy.data.images:
                if img.name.lower() == lightmap_name.lower():  # 忽略大小写
                    return img
        else:  # 可能不是角色贴图
            if "Color" in diffuse_image.name:
                lightmap_name = diffuse_image.name.replace("Color","LightMap")
                for img in bpy.data.images:
                    if img.name.lower() == lightmap_name.lower():  # 忽略大小写
                        return img
            else:
                return None
###################################################################################################
    if game == "绝区零":
        if "_D" in diffuse_image.name:
            lightmap_image = bpy.data.images[diffuse_image.name.replace("_D", "_M")]
            return lightmap_image
        else:
            return None
###################################################################################################
    if game == "鸣潮":
        if "_D" in diffuse_image.name:
            # 从前截到_D，从后截到.png
            match = re.compile(r"^(.*_D).*?(\.png)$").search(diffuse_image.name)
            if match:
                diffuse_name = match.group(1) + match.group(2)
                lightmap_image = (
                                bpy.data.images.get(diffuse_name.replace("_D", "_HM")) or
                                bpy.data.images.get(diffuse_name.replace("_D", "_ID")) or
                                bpy.data.images.get(diffuse_name.replace("_D", "_VC")) or
                                bpy.data.images.get(diffuse_name.replace("_D", "_M"))
                                  )
                return lightmap_image
            else:
                return None
###################################################################################################
