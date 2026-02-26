模块列表 = ["numpy", "pillow", "imagehash", "opencv"]

安装状态 = {
    # "numpy": "未检测",
    "pillow": "未检测",
    "imagehash": "未检测",
    "opencv": "未检测"
}

安装名称 = {
    "numpy": "numpy",
    "pillow": "pillow",
    "imagehash": "ImageHash",
    "opencv": "opencv-python-headless",
}

安装版本 = {
    "numpy": "1.25.2",
    "pillow": "12.0.0",
    "imagehash": "4.3.2",
    "opencv": "4.10.0.84",
}

安装指令 = {
    "numpy": ["--no-deps", "--force-reinstall"],
    "pillow": ["--upgrade-strategy", "only-if-needed"],
    "imagehash": ["--disable-pip-version-check"],
    "opencv": ["--no-cache-dir"],
}

导入名称 = {
    "numpy": "numpy",
    "pillow": "PIL",
    "imagehash": "imagehash",
    "opencv": "cv2",
}

安装大小 = {  # MB
    # "numpy": 61.675,
    # "pillow": 14.477,
    # "imagehash": 0.045656,
    # "opencv": 105.903,
}

def 获取版本(模块):

    if 模块 != 'opencv':
        import importlib
        importlib.import_module(导入名称[模块])

    import importlib.metadata
    版本 = importlib.metadata.version(安装名称[模块])  # PIL已安装None
    if 版本:
        # print(模块, '找到版本', 版本)
        return 版本
    # 裸 raise 必须在 except 块内才能重新抛出异常
    raise importlib.metadata.PackageNotFoundError(安装名称[模块])
    # import importlib.metadata
    # try:
    #     # 先尝试读pip包版本（完整版本号）
    #     return importlib.metadata.version(安装名称[模块])
    # except importlib.metadata.PackageNotFoundError:
    #     # 回退到模块自身的__version__
    #     return importlib.import_module(导入名称[模块]).__version__

# opencv读取安装进度时 触发面板获取插件版本 importlib.import_module(导入名称[模块])疯狂打印sys.path
# ['C:\\Users\\wulutuolaman\\AppData\\Roaming\\Blender Foundation\\Blender\\3.6\\scripts\\startup',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\scripts\\startup',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\scripts\\modules',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\python310.zip',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\python\\DLLs',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\python\\lib',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\python\\bin',
#  'C:\\Users\\wulutuolaman\\AppData\\Roaming\\Python\\Python310\\site-packages',
#  'C:\\Users\\wulutuolaman\\AppData\\Roaming\\Python\\Python310\\site-packages\\win32',
#  'C:\\Users\\wulutuolaman\\AppData\\Roaming\\Python\\Python310\\site-packages\\win32\\lib',
#  'C:\\Users\\wulutuolaman\\AppData\\Roaming\\Python\\Python310\\site-packages\\Pythonwin',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\python',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\python\\lib\\site-packages',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\scripts\\freestyle\\modules',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\scripts\\addons\\modules',
#  'C:\\Users\\wulutuolaman\\AppData\\Roaming\\Blender Foundation\\Blender\\3.6\\scripts\\addons\\modules',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\scripts\\addons',
#  'C:\\Users\\wulutuolaman\\AppData\\Roaming\\Blender Foundation\\Blender\\3.6\\scripts\\addons',
#  'C:\\Program Files\\Blender Foundation\\Blender 3.6\\3.6\\scripts\\addons_contrib']
