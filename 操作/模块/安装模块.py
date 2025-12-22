import bpy, sys, site, subprocess, importlib, traceback
from pathlib import Path

目录 = Path(__file__).parent.parent.parent / "轮子"
abi = f"cp{sys.version_info.major}{sys.version_info.minor}"  # 1.1.2不同版本blender使用的python版本亦不同

模块字典 = {
"PIL": f"pillow-12.0.0-{abi}-{abi}-win_amd64.whl",
"imagehash": "ImageHash-4.3.2-py2.py3-none-any.whl",
}

def 检查轮子存在():
    pillow = 目录 / 模块字典["PIL"]
    imagehash = 目录 / "ImageHash-4.3.2-py2.py3-none-any.whl"
    return pillow.exists() and imagehash.exists()

def 安装模块(self:bpy.types.Operator, 模块):
    轮子 = 模块字典[模块]
    路径 = 目录 / 轮子
    路径 = 路径.resolve()
    try:
        版本 = importlib.import_module(模块).__version__
        self.report({'INFO'}, f"{模块}已安装版本{版本}，跳过安装")
    except Exception as e:
        try:
            subprocess.run(
                [sys.executable,
                 "-m", "pip", "install",
                 "--upgrade-strategy",
                 "only-if-needed",  # 仅当需要时升级
                 str(路径)])
            importlib.invalidate_caches()  # 重新扫描可导入模块
            site.main()  # 重新加载 site-packages 路径，让新安装的包进入 sys.path
            try:
                版本 = importlib.import_module(模块).__version__
                self.report({'INFO'}, f"{模块}{版本}已完成安装")
            except Exception as e:
                错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                self.report({'ERROR'}, f"{模块} 安装成功但导入失败，尝试重新安装\n{错误信息}")
                try:
                    try:
                        subprocess.call([sys.executable, "-m", "pip", "uninstall", 模块, "-y"])  # 先清理模块残余文件
                    except Exception as e:
                        pass
                    subprocess.run(
                        [sys.executable,
                         "-m", "pip", "install",
                         "--force-reinstall",
                         "--no-deps",  # 不重新安装依赖
                         str(路径)])
                    importlib.invalidate_caches()  # 重新扫描可导入模块
                    site.main()  # 重新加载 site-packages 路径，让新安装的包进入 sys.path
                    try:
                        版本 = importlib.import_module(模块).__version__
                        self.report({'INFO'}, f"{模块}{版本}已完成重新安装")
                    except Exception as e:
                        错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                        self.report({'ERROR'}, f"{模块} 重新安装成功但导入失败\n{错误信息}")
                except Exception as e:
                    错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                    self.report({'ERROR'}, f"{模块} 重新安装出现异常\n{错误信息}")
        except Exception as e:
            错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            self.report({'ERROR'}, f"{模块} 安装出现异常\n{错误信息}")

class Install_Packages(bpy.types.Operator):
    """安装pillow和ImageHash模块"""
    bl_idname = "import_xiaoer.install_packages"
    bl_label = "安装模块"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            # 按顺序安装依赖
            安装模块(self, "PIL")
            安装模块(self, "imagehash")
        except Exception as e:
            错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            self.report({"ERROR"}, f'模块安装失败\n{错误信息}')
        return {'FINISHED'}  # ✅ 必须是 set 类型！