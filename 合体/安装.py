import sys
import subprocess


def 安装模块():

    python_exe = sys.executable

    # 1.1.0修复numpy
    try:
        import numpy
        if not numpy.__file__:
            print("numpy路径无效，重新安装")
            安装numpy()
        当前版本 = tuple(map(int, numpy.__version__.split(".")[:2]))
        print(f"当前 numpy 版本: {numpy.__version__}")
        if 当前版本 > (1, 25):
            print("numpy版本过高，可能导致 aud 不兼容，开始降级 ...")
            安装numpy()
    except ImportError:
        try:
            # subprocess.check_call(
            #     [python_exe, "-m", "pip", "install", "--force-reinstall", "numpy", "--disable-pip-version-check"],
            #     stdout=subprocess.DEVNULL,
            #     stderr=subprocess.DEVNULL
            # )
            安装numpy()
            try:
                import numpy
                print(f"numpy 安装成功 (版本: {numpy.__version__})")
            except ImportError:
                print(f"numpy 安装成功但无法导入，请关闭blender，删除缓存文件后重新启动")
        except Exception as e:
            print(f"numpy 安装失败: {str(e)}")

    # 1.0.1注册安装/升级Pillow
    try:
        from PIL import Image # 1.1.0优化启动速度
        print(f"pillow已安装")
    except ImportError:
        try:
            # 安装/升级Pillow
            subprocess.check_call(
                [python_exe, "-m", "pip", "install", "--upgrade", "pillow", "--disable-pip-version-check"],
                stdout=subprocess.DEVNULL
            )
            # 验证安装
            try:
                from PIL import Image
                print(f"pillow 安装成功 (版本: {Image.__version__})")
            except ImportError:
                print(f"pillow安装成功但无法导入，请关闭blender，删除缓存文件后重新启动")
        except Exception as e:
            print(f"pillow安装失败: {str(e)}")

    # 1.0.7注册安装/升级imagehash
    try:
        import imagehash # 1.1.0优化启动速度
        print(f"imagehash已安装")
    except ImportError:
        try:
            subprocess.check_call(
                [python_exe, "-m", "pip", "install", "--upgrade", "ImageHash", "--disable-pip-version-check"],
                stdout=subprocess.DEVNULL
            )
            try:
                import imagehash
                print(f"ImageHash 安装成功 (版本: {imagehash.__version__})")
            except ImportError:
                print(f"ImageHash 安装成功但无法导入，请关闭blender，删除缓存文件后重新启动")
        except Exception as e:
            print(f"ImageHash 安装失败: {str(e)}")

def 安装numpy(版本="1.25.2"):
    python_exe = sys.executable
    print(f"正在安装 numpy=={版本} ...")
    subprocess.run([
        python_exe, "-m", "pip", "install",
        f"numpy=={版本}", "--no-deps", "--force-reinstall"
    ], check=True)