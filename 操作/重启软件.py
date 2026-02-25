import os, bpy

class IMPORT_XIAOER_OT_restart_blender(bpy.types.Operator):
    bl_idname = "import_xiaoer.restart_blender"
    bl_label = "尝试重启 Blender"
    bl_description = "如遇模块安装异常中断、安装失败等问题，可尝试重启当前 Blender，或使用本地版手动安装模块"

    def execute(self, context):
        import sys, subprocess
        blender_exe = sys.executable  # 当前 Blender 的 Python 解释器路径
        # 从 python.exe 路径推算 blender.exe 路径
        # Blender 3.6 结构: .../Blender 3.6/3.6/python/bin/python3.10.exe
        # blender.exe 在:  .../Blender 3.6/blender.exe
        python路径 = os.path.normpath(blender_exe)
        blender路径 = os.path.normpath(
            os.path.join(python路径, "..", "..", "..", "..", "blender.exe")
        )

        if not os.path.exists(blender路径):
            self.report({'ERROR'}, f"找不到 blender.exe: {blender路径}")
            return {'CANCELLED'}

        print(f"正在重启 Blender: {blender路径}")
        subprocess.Popen([blender路径])  # 启动新进程
        bpy.ops.wm.quit_blender()        # 关闭当前进程
        return {'FINISHED'}