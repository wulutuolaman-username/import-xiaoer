import time
from bpy.utils import previews
from .指针 import 注册指针, 注销指针
from .合体.基础 import 注册类, 注销类
from .合体.属性 import 注册属性, 注销属性
from .合体.列表 import 列表添加
from .合体.安装 import 安装模块
from .图标 import 加载图标

def 回调(函数):
    起始 = time.perf_counter()
    函数()
    终止 = time.perf_counter()
    print(函数, f'耗时{终止-起始:.6f}秒')

def 注册():
    注册属性()
    注册指针()
    注册类()
    global 图标预览
    图标预览 = 加载图标()  # 使用游戏列表检查，必须在注册之后
    列表添加()
    # 安装模块()
    回调(安装模块)
def 注销():
    注销指针()
    注销属性()
    注销类()
    global 图标预览
    previews.remove(图标预览)
    图标预览 = None
    # subprocess.run([sys.executable, "-m", "pip", "uninstall", "imagehash"])  # 卸载或关闭插件会卡死