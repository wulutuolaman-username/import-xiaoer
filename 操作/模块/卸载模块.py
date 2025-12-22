import bpy, sys, subprocess, importlib

模块字典 = {
    "pillow": "PIL",
    "imagehash": "imagehash"
}

def 卸载模块(self:bpy.types.Operator, 模块):
    try:
        导入模块 = 模块字典[模块]
        importlib.import_module(导入模块)
        subprocess.call([sys.executable, "-m", "pip", "uninstall", 模块, "-y"])
        self.report({"INFO"}, f'{模块}模块卸载成功')
        # 关键：清理模块缓存
        if 导入模块 in sys.modules:
            del sys.modules[导入模块]
        importlib.invalidate_caches()
    except:
        self.report({"INFO"}, f'未检测到需要卸载的{模块}模块')

class Uninstall_Packages(bpy.types.Operator):
    """卸载pillow和imagehash模块"""
    bl_idname = "import_xiaoer.uninstall_packages"
    bl_label = "卸载模块"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 获取Blender的Python解释器路径
        卸载模块(self, "pillow")  # 指定版本
        卸载模块(self, "imagehash")
        return {'FINISHED'}  # ✅ 必须是 set 类型！