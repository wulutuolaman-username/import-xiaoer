import os, bpy, sys, site, subprocess, importlib, shutil  # noqa: F401
from ...模块 import *
from ...通用.信息 import *

def 卸载模块(self:bpy.types.Operator|None, 模块):
    try:
        获取版本(模块)
        导入模块 = 导入名称[模块]
        # importlib.import_module(导入模块)
        subprocess.call([sys.executable, "-m", "pip", "uninstall", 安装名称[模块], "-y"])
        安装状态[模块] = "完成卸载"
        # self.report({"INFO"}, f'{模块}模块卸载成功')
        报告信息(self, '正常', f'{模块}模块卸载成功')
        # 关键：清理模块缓存
        if 导入模块 in sys.modules:
            del sys.modules[导入模块]
        # 卸载后清理所有 site-packages 目录里的损坏残留
        清理残留()
        importlib.invalidate_caches()  # 重新扫描可导入模块
        site.main()  # 重新加载 site-packages 路径，让新安装的包进入 sys.path
    except:
        # self.report({"INFO"}, f'未检测到需要卸载的{模块}模块')
        报告信息(self, '正常', f'未检测到需要卸载的{模块}模块')

def 清理残留():
    # 但 ~il 和 ~v2 目录因为 Blender 还在运行、文件锁没释放，所以 PermissionError 清理失败。这两个等下次重启后再清理就能成功了。
    for 目录 in sys.path:
        if "site-packages" not in 目录:
            continue
        if not os.path.exists(目录):
            continue
        for 项目 in os.listdir(目录):
            if 项目.startswith("-") or 项目.startswith("~"):
                完整路径 = os.path.join(目录, 项目)
                try:
                    if os.path.isdir(完整路径):
                        shutil.rmtree(完整路径)
                    else:
                        os.remove(完整路径)
                    print(f"已清理损坏残留: {完整路径}")
                except Exception as e:
                    输出错误(None, e, f'清理失败 {完整路径}')

class Uninstall_Packages(bpy.types.Operator):
    """卸载pillow和imagehash模块"""
    bl_idname = "import_xiaoer.uninstall_packages"
    bl_label = "卸载模块"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for 模块 in 模块列表:
            if 模块 != "numpy":
                卸载模块(self, 模块)
        return {'FINISHED'}  # ✅ 必须是 set 类型！