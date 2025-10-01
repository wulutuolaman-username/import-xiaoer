import os
import bpy
import traceback
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper
from ...核心.导出模型预设 import 透透小二
from ...通用.改名 import 模型名称处理

class ExportMatPresets(bpy.types.Operator, ExportHelper):
    """ 选择一个模型导出预设 """
    bl_idname = "import_xiaoer.export_mat_presets"
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
        return context.object is not None and context.object.type == 'MESH' and context.mode == 'OBJECT' and len(context.selected_objects) == 1  # 1.1.0只支持一个模型

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
            # if 模型.parent and 模型.parent.type == 'ARMATURE':
            #     if 模型.parent.parent:
            #         return f"{模型名称处理(模型.parent.parent)}预设.blend"
            #     return f"{模型名称处理(模型.parent)}预设.blend"
            # # 名称 = 模型.name.replace("_mesh", "")
            return f"{模型名称处理(模型)}预设.blend"
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

        # # 执行保存操作
        # bpy.ops.wm.save_as_mainfile(
        #     filepath=保存路径,
        #     check_existing=True,  # 检查文件存在
        #     copy=True  # 保持原文件不受影响
        # )
        # self.report({'INFO'}, f"导出预设: {保存路径}")
        模型 = context.object
        # 模型名称 = 模型.name
        # bpy.ops.wm.open_mainfile(filepath=保存路径)
        # 模型 = bpy.data.objects[模型名称]
        # 模型.select_set(True)
        try:
            透透小二(self, 模型, 保存路径)
        except Exception as e:
            错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            self.report({"ERROR"}, f"{模型.name}导出模型预设过程出现异常，可向插件作者反馈错误信息\n{错误信息}")
        # 1.1.0保存文件（确保不会因打包失败而终止）
        try:
            bpy.ops.wm.save_mainfile(filepath=self.filepath)
        except RuntimeError as e:
            self.report({'ERROR'}, f"保存文件出现问题: {str(e)}")
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
                self.report({'ERROR'}, f"删除备份文件失败: {str(e)}")
        return {'FINISHED'}