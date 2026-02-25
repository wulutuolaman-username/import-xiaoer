import bpy, threading  # noqa: F401
from ...合体.安装 import 安装模块
from ...通用.信息 import *

class Install_Packages(bpy.types.Operator):
    """安装pillow和ImageHash模块"""
    bl_idname = "import_xiaoer.install_packages"
    bl_label = "安装模块"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            threading.Thread(target=安装模块, daemon=True).start()
        except Exception as e:
            输出错误(self, e, '模块安装失败')
        return {'FINISHED'}  # ✅ 必须是 set 类型！