import bpy

def 获取空白贴图(名称='', 宽度=4, 透明=False):
    空白贴图 = bpy.data.images.get(名称, "")
    if not 空白贴图:
        空白贴图 = bpy.data.images.new(名称, width=int(宽度), height=int(宽度), alpha=透明)
    空白贴图.pixels = [1.0] * (宽度 * 宽度 * 4)  # type:ignore  # 4通道(R,G,B,A)
    空白贴图.pack()  # 强制打包像素数据到 .blend 文件
    return 空白贴图