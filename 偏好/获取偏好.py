import bpy
from typing import cast
from .偏好设置 import XiaoerAddonPreferences

def 获取偏好() -> XiaoerAddonPreferences:
    return cast(XiaoerAddonPreferences, bpy.context.preferences.addons[XiaoerAddonPreferences.bl_idname].preferences)
