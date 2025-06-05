import bpy
import os
from bpy.props import CollectionProperty, StringProperty
from bpy_extras.io_utils import ImportHelper
from ...通用.查找 import 查找预设
from ...核心.导入模型预设 import 炒飞小二
from ...通用.清理 import 清理MMD刚体材质

class ImportMatPresets(bpy.types.Operator):
    """ 选择对应模型预设导入 """
    bl_idname = "import_test.import_mat_presets"
    bl_label = "导入材质到模型"
    bl_options = {"UNDO"}

    file_path: StringProperty(
        name="文件路径",
        description="预设文件路径",
        default="",
        subtype='FILE_PATH'
    )

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context):
        偏好 = context.preferences.addons["导入小二"].preferences
        if 偏好.预设目录:
            if os.path.exists(偏好.预设目录):
                for 模型 in bpy.context.selected_objects:  # 可能选择了多个物体
                    文件路径, 角色 = 查找预设(偏好, 模型)  # 读取文件路径和文件名称
                    if 文件路径 and 角色:
                        self.report({"INFO"}, "匹配名称："+str(角色))
                        炒飞小二(偏好, 模型, 文件路径, 角色, self)
                    else:
                        self.report({"WARNING"}, f"未找到{模型.name}匹配预设，请检查：\n  偏好设置预设目录是否包含对应的预设文件\n  模型名称和预设文件名是否正确对应\n或关闭自动查找预设手动导入")
                if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
                    清理MMD刚体材质()  # 整理MMD刚体材质
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, f"预设目录不存在")
                return {'CANCELLED'}  # 确保返回有效结果
        else:
            self.report({'WARNING'}, f"未设置预设目录")
            return {'CANCELLED'}  # 确保返回有效结果

class ImportMatPresetsFilebrowser(bpy.types.Operator, ImportHelper):
    bl_idname = "import_test.import_mat_presets_filebrowser"
    bl_label = "选择预设文件"

    files: CollectionProperty(type=bpy.types.PropertyGroup)
    filter_glob: StringProperty(
        default="*.blend",
        options={'HIDDEN'},
        maxlen=255,
    )

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context):
        偏好 = context.preferences.addons["导入小二"].preferences
        文件路径 = self.filepath  # 手动选择的文件路径
        角色 = os.path.splitext(os.path.basename(文件路径))[0]  # 获取文件名（去掉路径和扩展名）
        角色 = 角色.replace("渲染", "")  # 去掉“渲染”字样（如果有）
        角色 = 角色.replace("预设", "")  # 去掉“预设”字样（如果有）
        self.report({"INFO"}, f"匹配名称：" + str(角色))
        模型 = bpy.context.object  # 获取当前选中的模型
        炒飞小二(偏好, 模型, 文件路径, 角色, self)
        if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
            清理MMD刚体材质()  # 整理MMD刚体材质
        return {'FINISHED'}