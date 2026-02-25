import bpy
from .偏好设置 import *

def 获取偏好() -> 小二偏好|bpy.types.AddonPreferences:
    return bpy.context.preferences.addons[XiaoerAddonPreferences.bl_idname].preferences
