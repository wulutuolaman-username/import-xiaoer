import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from ..偏好.获取偏好 import 获取偏好

# 操作符基类
class SetTemplatePathBaseOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "xiaoer.set_path"
    bl_label = "Set Path"  # 这个属性是必须的
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(
        default="*.blend",
        options={'HIDDEN'},
        maxlen=255
    )
    属性: StringProperty()

    def execute(self, context):
        偏好 = 获取偏好()
        setattr(偏好, self.属性, self.filepath)
        return {'FINISHED'}
# 具体操作符类
class SetUserPathOperator(SetTemplatePathBaseOperator):
    """设置用户路径"""
    bl_idname = "xiaoer.set_user_path"  # 操作符的唯一标识符
    bl_label = "选择预设目录"
    属性 = "预设目录"
class SetImagePathOperator(bpy.types.Operator, ImportHelper):
    """设置贴图路径"""
    bl_idname = "xiaoer.set_image_path"  # 操作符的唯一标识符
    bl_label = "选择贴图目录"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(
        default="*.png;*.jpg;*.jpeg;*.tga;*.exr;*.tif;*.tiff",
        options={'HIDDEN'},
        maxlen=255
    )
    # 目标属性名称
    属性: bpy.props.StringProperty()

    def execute(self, context):
        # 获取偏好设置对象
        偏好 = 获取偏好()

        # 将选择的路径保存到目标属性
        setattr(偏好, self.属性, self.filepath)
        return {'FINISHED'}

class SetHonkai3PathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_honkai3_path"
    bl_label = "选择崩坏三模板文件"
    属性 = "honkai3_path"
class SetGenshinPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_genshin_path"
    bl_label = "选择原神模板文件"
    属性 = "genshin_path"
class SetHonkaiStarRailPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_honkai_star_rail_path"
    bl_label = "选择崩坏：星穹铁道模板文件"
    属性 = "honkai_star_rail_path"
class SetZenlessZoneZeroPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_zenless_zone_zero_path"
    bl_label = "选择绝区零模板文件"
    属性 = "zenless_zone_zero_path"
class SetWutheringwavesPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_wuthering_waves_path"
    bl_label = "选择鸣潮模板文件"
    属性 = "wuthering_waves_path"