import threading
# from bpy.utils import previews
from .指针 import 注册指针, 注销指针
from .合体.基础 import 注册类, 注销类
from .合体.属性 import 注册属性, 注销属性
from .合体.列表 import 列表添加
from .合体.安装 import 安装模块
from .图标 import 图标预览

def 注册():
    注册属性()
    注册指针()
    注册类()
    # global 图标预览
    # 图标预览 = 加载图标()  # 使用游戏列表检查，必须在注册之后
    图标预览.加载()
    列表添加()
    # 安装模块()
    # 后台线程安装
    threading.Thread(target=安装模块, daemon=True).start()

def 注销():
    注销指针()
    注销属性()
    注销类()
    图标预览.卸载()
    # global 图标预览
    # previews.remove(图标预览)
    # 图标预览 = None
    # subprocess.run([sys.executable, "-m", "pip", "uninstall", "imagehash"])  # 卸载或关闭插件会卡死