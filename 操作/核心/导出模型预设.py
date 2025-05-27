import os
import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper
from ...核心.导出模型预设 import 透透小二

class ExportMatPresets(bpy.types.Operator,ExportHelper):
    """ 选择对应模型导出预设 """
    bl_idname = "export_test.export_mat_presets"
    bl_label = "导出模型预设"
    bl_options = {"UNDO"}

    # 文件类型过滤
    filename_ext = ".blend"
    filter_glob: StringProperty(
        default="*.blend",
        options={'HIDDEN'},
        maxlen=255,
    )

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH'

    # 动态设置默认路径和文件名
    def invoke(self, context, event):
        # 获取用户预设路径
        偏好 = context.preferences.addons["导入小二"].preferences
        if 偏好.预设目录:
            self.filepath = os.path.join(
                偏好.预设目录,  # 从偏好设置获取路径
                self.generate_filename(context)  # 自动生成文件名
            )
            return super().invoke(context, event)
        else:
            self.report({'WARNING'}, f"未设置预设目录")
            return {'CANCELLED'}  # 确保返回有效结果

    def generate_filename(self, context):
        """生成默认文件名逻辑"""
        模型 = context.object
        if 模型:
            名称 = 模型.name.replace("_mesh", "")
            return f"{名称}预设.blend"
        return "untitled.blend"

    def execute(self, context):

        # 最终保存路径处理
        保存路径 = os.path.normpath(self.filepath)
        保存信息 = os.path.dirname(保存路径)

        # 路径有效性检查
        if not os.path.exists(保存信息):
            os.makedirs(保存信息)

        if not os.access(保存信息, os.W_OK):
            self.report({'WARNING'}, f"无写入权限: {保存信息}")
            return {'CANCELLED'}

        # try:
        # 执行保存操作
        bpy.ops.wm.save_as_mainfile(
            filepath=保存路径,
            check_existing=True,  # 检查文件存在
            copy=True  # 保持原文件不受影响
        )
        self.report({'INFO'}, f"导出预设: {保存路径}")
        模型 = context.object
        模型名称 = 模型.name
        bpy.ops.wm.open_mainfile(filepath=保存路径)
        模型 = bpy.data.objects[模型名称]
        模型.select_set(True)
        透透小二(self, 模型)
        # 保存最终文件
        bpy.ops.wm.save_mainfile(filepath=self.filepath)
        # except Exception as e:
        #     self.report({'ERROR'}, f"导出失败: {str(e)}")
        #     return {'CANCELLED'}
        # 删除备份文件 (blend1)  #1.0.3新增
        备份文件 = f"{保存路径}1"  # Blender自动创建的备份文件
        if os.path.exists(备份文件):
            try:
                os.remove(备份文件)
                self.report({'INFO'}, f"已删除备份文件: {备份文件}")
            except Exception as e:
                self.report({'WARNING'}, f"删除备份文件失败: {str(e)}")
        return {'FINISHED'}