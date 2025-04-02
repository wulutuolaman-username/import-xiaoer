import bpy
def AO_texture(game,diffuse_image):
###################################################################################################
    if game == "绝区零":
        if "_D" in diffuse_image.name:
            AO_image = bpy.data.images[diffuse_image.name.replace("_D", "_A")]
            return AO_image
        else:
            return None
###################################################################################################
