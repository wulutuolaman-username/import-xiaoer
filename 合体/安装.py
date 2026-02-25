import os, bpy, re, time, sys, site, subprocess, tempfile, glob, threading, sysconfig, zipfile  # noqa: F401
from ..模块 import *  # noqa: F401
from ..通用.信息 import *  # noqa: F401
from ..操作.模块.卸载模块 import *
from ..面板.刷新 import *
from ..指针 import *

def 安装模块():

    清理残留()
    # # 1.2.0设置环境变量
    # os.environ["PYTHONNOUSERSITE"] = "1"

    起始 = time.perf_counter()
    # 1.1.0修复numpy
    try:
        import numpy
        if not numpy.__file__:
            print("numpy路径无效，正在重新安装")
            安装numpy()
        当前版本 = tuple(map(int, numpy.__version__.split(".")[:2]))
        print(f"当前 numpy 版本: {numpy.__version__}")
        if 当前版本 > (1, 25):
            print("numpy版本过高，可能导致 aud 不兼容，开始降级 ...")
            安装numpy()
            print(f"当前 numpy 版本: {numpy.__version__}")
    except ImportError:
        try:
            安装numpy()
            try:
                import numpy
                print(f"numpy 安装成功 (版本: {numpy.__version__})")
            except ImportError:
                numpy = None
                print(f"numpy 安装命令执行完毕但无法导入，请关闭blender，删除缓存文件后重新启动")
        except Exception as e:
            print(f"numpy 安装失败: {str(e)}")
    终止 = time.perf_counter()
    print(f'检测numpy模块耗时{终止-起始:.6f}秒')

    # 1.2.0读取每个模块的安装进度
    for 模块 in 模块列表:
        if 模块 != "numpy":
            安装单个模块(None, 模块)
    # importlib.invalidate_caches()  # 重新扫描可导入模块
    # site.main()  # 重新加载 site-packages 路径，让新安装的包进入 sys.path

def 重载模块(模块名):
    """
    强制重新加载模块，刷新版本号
    1. 从 sys.modules 删除缓存
    2. 重新 import，获取新版本
    """
    try:
        if 模块名 in sys.modules:
            del sys.modules[模块名]
        # 如果有子模块，也需要删除（如 PIL.Image）
        子模块列表 = [key for key in sys.modules if key.startswith(f"{模块名}.")]
        for 子模块 in 子模块列表:
            del sys.modules[子模块]

        if hasattr(sys, 'OpenCV_LOADER'):  # 解决cv2安装成功后无法导入 ImportError: ERROR: recursion is detected during loading of "cv2" binary extensions. Check OpenCV installation.
            del sys.OpenCV_LOADER
            # print("清除残留标记OpenCV_LOADER")
    except:
        pass

    return None

def 安装numpy(版本="1.25.2"):
    python_exe = sys.executable
    print(f"正在安装 numpy=={版本} ...")
    # 安装状态 = 获取安装状态()
    # 安装状态.numpy = "正在安装"
    安装状态["numpy"] = "正在安装"
    subprocess.run(
        [python_exe, "-m", "pip", "install",
             f"numpy=={版本}", "--no-deps", "--force-reinstall",
             "--no-user",  # 禁止装到 Roaming
             "--no-cache-dir",  # 防止旧 wheel
             "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",  # 指定清华镜像
             "--trusted-host", "pypi.tuna.tsinghua.edu.cn",
             ],
             encoding='gbk',  # 明确使用GBK解码中文系统的CMD输出
             text=True,
             check=True,
             capture_output=True,
    )
    重载模块("numpy")

# 1.2.0读取模块安装进度
def 安装单个模块(self, 模块):
    窗口 = bpy.context.window_manager  # type:小二窗口|bpy.types.WindowManager
    窗口.小二预设模板.总大小 = 窗口.小二预设模板.已下载 = 0
    下载目录 = tempfile.mkdtemp(prefix=f"blender_pip_{模块}_")
    下载开始时间 = time.time()
    pip已完成 = threading.Event()  # 用 Event 通知 Timer 停止
    pip已完成下载 = threading.Event()  # 用 Event 通知 Timer 停止
    pip已完成安装 = threading.Event()  # 用 Event 通知 Timer 停止
    print()
    def pip线程():
        # 增加 --progress-bar on 强制 pip 输出进度
        cmd = [sys.executable, "-m", "pip", "download", 安装名称[模块] + "==" + 安装版本[模块]] + [
                "-d", 下载目录,
                "--no-deps",  # 不下载依赖
                "--no-cache-dir",  # 防止旧 wheel
                "--progress-bar", "on",
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",  # 指定清华镜像
                "--trusted-host", "pypi.tuna.tsinghua.edu.cn",
              ]
        # 卸载模块(self, 模块)
        安装状态[模块] = "正在下载"
        过程 = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='gbk',
        )

        状态 = None
        while True:
            # import datetime
            # print(datetime.datetime.now())
            输出 = 过程.stdout.readline()
            if not 输出:  # 进程意外结束，stdout关闭
                if 过程.poll() is not None:
                    break
                continue
            print(repr(输出))  # 调试用，确认后可删
            # if not 输出 and 过程.poll() is not None:
            #     break

            if "Downloading" in 输出:
                状态 = "下载"
                读取下载目标(窗口, 输出)  # 先解析总大小
            if "Successfully downloaded" in 输出:
                pip已完成下载.set()
                break
            # if "Installing collected packages" in 输出:
            #     状态 = "安装"
            #     pip已完成下载.set()
            #
            # if "Successfully installed" in 输出:
            #     pip已完成安装.set()
            #     重载模块(导入名称[模块])
            #     print(f"{导入名称[模块]} 安装成功 (版本: {获取版本(模块)})")
            #     安装状态[模块] = "安装成功"
            #     break

            if 状态 == "下载":
                # 注册下载进度Timer（避免重复注册）
                if not bpy.app.timers.is_registered(读取下载进度):
                    bpy.app.timers.register(读取下载进度, first_interval=0.1)

            # if 状态 == "安装":
            #     # 切换到安装进度Timer
            #     if not bpy.app.timers.is_registered(读取安装进度):
            #         bpy.app.timers.register(读取安装进度, first_interval=0.2)

            # 读取下载目标(窗口, 输出)
        过程.wait()
        pip已完成下载.set()

        # 解析 whl 文件计算解压大小
        窗口.小二预设模板.总大小 = 安装大小[模块] = 0
        最新文件 = glob.glob(os.path.join(下载目录, "*.whl"))[0]  # pip 清理临时目录 需要重新在下载目录里查找
        with zipfile.ZipFile(最新文件, 'r') as z:
            for info in z.infolist():
                安装大小[模块] += info.file_size / (1024 * 1024)
            窗口.小二预设模板.总大小 = 安装大小[模块]
            print(最新文件)
            print(模块, '解析安装后大小', 安装大小[模块], 'MB')

        cmd = [
            sys.executable, "-m", "pip", "install",
            最新文件,
            "--no-user",  # 禁止装到 Roaming
            "--no-cache-dir",  # 防止旧 wheel
        ] + 安装指令[模块]
        安装状态[模块] = "正在安装"
        过程 = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='gbk',
        )

        状态 = None
        while True:
            # import datetime
            # print(datetime.datetime.now())
            输出 = 过程.stdout.readline()
            if not 输出:  # 进程意外结束，stdout关闭
                if 过程.poll() is not None:
                    break
                continue
            print(repr(输出))  # 调试用，确认后可删
            # if not 输出 and 过程.poll() is not None:
            #     break

            if "Installing collected packages" in 输出:
                状态 = "安装"

            if "Successfully installed" in 输出:
                pip已完成安装.set()
                break

            if 状态 == "安装":
                # 切换到安装进度Timer
                if not bpy.app.timers.is_registered(读取安装进度):
                    bpy.app.timers.register(读取安装进度, first_interval=0.01)

        过程.wait()
        pip已完成安装.set()
        # 重载模块(导入名称[模块])
        print(f"{导入名称[模块]} 安装成功 (版本: {获取版本(模块)})")
        安装状态[模块] = "安装成功"
        pip已完成.set()  # 通知 Timer 可以停止了

        if os.path.exists(下载目录):
            shutil.rmtree(下载目录, ignore_errors=True)
            print(f"已清理临时下载目录: {下载目录}")

    def 读取下载目标(窗口: '小二窗口', 输出):
        try:
            # 匹配总大小，例如 "Downloading xxx.whl (38.8 MB)"
            # print(模块, f'此时总大小属性值{窗口.小二预设模板.总大小}')
            # print(输出)
            # if 窗口.小二预设模板.总大小 == 0:
                总大小匹配 = re.search(r'\((\d+\.?\d*)\s*(MB|kB|KB|GB)\)', 输出)
                # print('总大小匹配', 总大小匹配)
                if 总大小匹配:
                    数值 = float(总大小匹配.group(1))
                    单位 = 总大小匹配.group(2).upper()
                    # print('数值', 数值)
                    # print('单位', 单位)
                    倍数 = {'KB': 1/1024, 'MB': 1, 'GB': 1024}
                    窗口.小二预设模板.总大小 = 数值 * 倍数.get(单位, 1)
                    print(模块, '下载目标大小', 窗口.小二预设模板.总大小, 'MB')
        except Exception as e: 输出错误(None, e, "读取下载目标失败")

    最新文件 = None
    def 读取下载进度():

        if pip已完成下载.is_set():
            return None  # 停止Timer

        nonlocal 最新文件
        try:
            窗口 = bpy.context.window_manager  # type:小二窗口|bpy.types.WindowManager
            if 窗口.小二预设模板.总大小 > 0:
                if not 最新文件:
                    # pip_tmp = os.path.join(tempfile.gettempdir(), "pip-*", "*.whl")
                    # 已下载匹配 = re.search(r'(\d+\.?\d*)/\d+\.?\d*\s*(?:MB|kB|KB|GB)', 输出)
                    候选 = glob.glob(os.path.join(tempfile.gettempdir(), "pip-download-*", "*.whl"))
                    候选 += glob.glob(os.path.join(tempfile.gettempdir(), "pip-*", "*.whl"))
                    候选 = [f for f in 候选 if os.path.getmtime(f) >= 下载开始时间]
                    # print('候选', 候选)
                    最新文件 = max(候选, key=os.path.getmtime)
                    # print('最新文件', 最新文件, 模块 in 最新文件)
                    print('最新文件', 最新文件)
                if 最新文件 and os.path.exists(最新文件) and 模块 in os.path.basename(最新文件):
                    # print(os.path.getsize(最新文件) / (1024 * 1024))
                    窗口.小二预设模板.已下载 = os.path.getsize(最新文件) / (1024 * 1024)
                    print(模块, '已下载大小', 窗口.小二预设模板.已下载, 'MB')
                    刷新3D视图UI面板()

        except Exception as e: 输出错误(None, e, "读取下载进度失败")
        return 0.01  # 继续，0.01秒后再次调用

    def 读取安装进度():
        if pip已完成安装.is_set():
            return None  # 停止Timer

        try:
            窗口 = bpy.context.window_manager   # type:小二窗口|bpy.types.WindowManager
            模块目录 = os.path.join(sysconfig.get_path('purelib'), 导入名称[模块])

            if os.path.isdir(模块目录):
                安装状态[模块] = "正在安装"

                窗口.小二预设模板.已下载  = sum(
                    os.path.getsize(os.path.join(根目录, 文件))
                    for 根目录, 目录列表, 文件列表 in os.walk(模块目录)
                    if "__pycache__" not in 根目录  # 排除路径中包含缓存文件夹的情况
                    for 文件 in 文件列表
                ) / 1024 / 1024  # 转MB
                print(模块, '已安装大小', 窗口.小二预设模板.已下载, 'MB')
                刷新3D视图UI面板()
        except Exception as e:
            输出错误(None, e, "读取安装进度失败")
        return 0.1  # 继续，0.1秒后再次调用

    起始 = time.perf_counter()

    try:
        print(f"{导入名称[模块]}已安装{获取版本(模块)}")
        return
    except:
        pass
    try:
        pip线程实例 = threading.Thread(target=pip线程, daemon=True)
        pip线程实例.start()
        # bpy.app.timers.register(读取下载进度, first_interval=0.1)
        # 主线程等待安装完成（阻塞当前操作，但 Timer 在后台跑）
        pip线程实例.join()

    except Exception as e:
        输出错误(None, e, f"{导入名称[模块]} 安装失败")
        安装状态[模块] = "安装失败"

    终止 = time.perf_counter()
    print(f'检测{导入名称[模块]}模块耗时 {终止-起始:.6f}秒')


