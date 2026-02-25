import os, bpy, traceback
from bpy.props import CollectionProperty, StringProperty
from bpy_extras.io_utils import ImportHelper
from ...查找.查找预设 import 查找预设
from ...核心.导入模型预设 import 炒飞小二
from ...通用.清理 import 清理MMD刚体材质
from ...偏好.获取偏好 import 获取偏好
from ...指针 import *

class XiaoerAddonImportMatPresets(bpy.types.Operator):
    """ 自动导入所有模型预设 """
    bl_idname = "import_xiaoer.import_presets_auto"
    bl_label = "导入模型预设"
    bl_options = {"UNDO"}

    file_path: StringProperty(
        name="文件路径",
        description="预设文件路径",
        default="",
        subtype='FILE_PATH'
    )

    @classmethod
    def poll(self, context):
        网格 = True
        if len(context.selected_objects) > 0:
            for 物体 in context.selected_objects:  # type:小二物体
                if not 物体.判断类型.物体.是网格:
                    网格 = False
                    break
        else:
            网格 = False
        return 网格 and context.mode == 'OBJECT'
        # return all(物体.判断类型.物体.是网格 for 物体 in context.selected_objects) and context.mode == 'OBJECT'

    def execute(self, context):
        偏好 = 获取偏好()
        if 偏好.预设目录:
            if os.path.exists(偏好.预设目录):
                模型列表 = []
                for 模型 in bpy.context.selected_objects:  # 可能选择了多个物体
                    模型列表.append(模型)
                for 模型 in 模型列表:  # type:小二物体
                    if 模型.小二预设模型.导入完成 == True:
                        self.report({"INFO"}, f"{模型.name}已导入预设，在物体属性面板取消导入完成状态可再次导入")
                        continue
                    文件路径, 角色 = 查找预设(self, 偏好, 模型)  # 读取文件路径和文件名称
                    if 文件路径 and 角色:
                        self.report({"INFO"}, f"{模型.name}匹配预设：{文件路径}")
                        if 偏好.自动查找预设 and 偏好.查找预设深度检索:
                            self.report({"WARNING"}, f"如果{模型.name}深度检索结果错误，请检查：\n"
                                                              f"{偏好.预设目录} 是否包含对应的预设文件\n  "
                                                              f"{模型.name}模型名称和预设文件名是否存在相同字符\n"
                                                              f"或关闭自动查找预设手动导入")
                        try:
                            炒飞小二(self, 偏好, 模型, 文件路径, 角色)
                            if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
                                清理MMD刚体材质()  # 整理MMD刚体材质
                            for 材质 in list(bpy.data.materials):  # 1.1.0完成导入预设后清理无用预设材质
                                if 材质.users == 1 and 材质.use_fake_user:
                                    bpy.data.materials.remove(材质)
                        except Exception as e:
                            错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                            self.report({"ERROR"}, f"{模型.name}自动导入预设过程出现异常，可向插件作者反馈错误信息\n{错误信息}")
                    else:
                        self.report({"ERROR"}, f"未找到{模型.name}匹配预设，请检查：\n  "
                                                        f"{偏好.预设目录} 是否包含对应的预设文件\n  "
                                                        f"{模型.name}模型名称和预设文件名是否正确对应\n或关闭自动查找预设手动导入")
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, f"预设目录不存在")
                return {'CANCELLED'}  # 确保返回有效结果
        else:
            self.report({'WARNING'}, f"未设置预设目录")
            return {'CANCELLED'}  # 确保返回有效结果

class XiaoerAddonImportMatPresetsFilebrowser(bpy.types.Operator, ImportHelper):
    """ 选择对应模型预设导入 """
    bl_idname = "import_xiaoer.import_presets_hand"
    bl_label = "选择预设文件"

    files: CollectionProperty(type=bpy.types.PropertyGroup)
    filter_glob: StringProperty(
        default="*.blend",
        options={'HIDDEN'},
        maxlen=255,
    )

    @classmethod
    def poll(self, context):
        物体 = context.active_object  # type:小二物体|bpy.types.Object
        return 物体 and 物体.判断类型.物体.是网格 and context.mode == 'OBJECT' and len(context.selected_objects) == 1

    def execute(self, context):
        偏好 = 获取偏好()
        文件路径 = self.filepath  # type: ignore
        角色 = os.path.splitext(os.path.basename(文件路径))[0]  # 获取文件名（去掉路径和扩展名）
        角色 = 角色.replace("渲染", "")  # 去掉“渲染”字样（如果有）
        角色 = 角色.replace("预设", "")  # 去掉“预设”字样（如果有）
        self.report({"INFO"}, f"匹配名称：" + str(角色))
        模型 = context.active_object  # type:小二物体|bpy.types.Object  # 获取当前选中的模型
        try:
            if 模型.小二预设模型.导入完成 == True:
                self.report({"INFO"}, f"{模型.name}已导入预设，在物体属性面板取消导入完成状态可再次导入")
                return {'FINISHED'}
            炒飞小二(self, 偏好, 模型, 文件路径, 角色)
            if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
                清理MMD刚体材质()  # 整理MMD刚体材质
        except Exception as e:
            错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            self.report({"ERROR"}, f"{模型.name}手动导入预设过程出现异常，可向插件作者反馈错误信息\n{错误信息}")
        return {'FINISHED'}