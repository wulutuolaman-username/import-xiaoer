import bpy

def normalmap_texture(game,diffuse_image):
###################################################################################################
    if game == "崩坏三":
        if "Color" in diffuse_image.name:
            normalmap_name = diffuse_image.name.replace("Color", "Normal")
            if normalmap_name in bpy.data.images:
                return bpy.data.images[normalmap_name]
            else:
                return None
###################################################################################################
    if game == "原神":
        try:
            Normalmap_image = bpy.data.images[diffuse_image.name.replace("Diffuse", "Normalmap")]
            return Normalmap_image
        except KeyError as e:
            if "not found" in str(e):
                pass  # 如果已经加载则跳过
            else:
                raise  # 其他错误继续抛出
###################################################################################################
    if game == "绝区零" or game == "鸣潮":
        if "_D" in diffuse_image.name:
            Normalmap_name = diffuse_image.name.replace("_D", "_N")
            if Normalmap_name in bpy.data.images:
                return bpy.data.images[Normalmap_name]
            else:
                return None
###################################################################################################