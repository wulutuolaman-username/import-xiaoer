import os, bpy
from bpy.utils import previews

def 加载图标():
    图标预览 = previews.new()
    图标文件夹 = os.path.join(os.path.dirname(__file__), "图标")
    for 文件名 in os.listdir(图标文件夹):
        图标路径 = os.path.join(os.path.dirname(__file__), "图标", 文件名)
        图标名称 = os.path.splitext(文件名)[0]
        if os.path.exists(图标路径):
            try:
                if 图标名称 not in 图标预览:
                    图标预览.load(图标名称, 图标路径, 'IMAGE')  # 使用显示名作为键
            except KeyError as e:
                if "already exists" in str(e):
                    continue  # 如果已经加载则跳过
                raise  # 其他错误继续抛出
    return 图标预览