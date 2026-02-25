import bpy

class XiaoerAddonWindowManagerInformation(bpy.types.PropertyGroup):
    已下载: bpy.props.FloatProperty(
        default=0
    )
    总大小: bpy.props.FloatProperty(
        default=0
    )