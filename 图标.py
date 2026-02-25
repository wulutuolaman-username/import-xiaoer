import os
from bpy.utils import previews

# # 1.2.0明确导出列表
# __all__ = ['加载图标']
#
# def 加载图标():
#     图标预览 = previews.new()
#     图标文件夹 = os.path.join(os.path.dirname(__file__), "图标")
#     for 文件名 in os.listdir(图标文件夹):
#         图标路径 = os.path.join(os.path.dirname(__file__), "图标", 文件名)
#         图标名称 = os.path.splitext(文件名)[0]
#         if os.path.exists(图标路径):
#             try:
#                 if 图标名称 not in 图标预览:
#                     图标预览.load(图标名称, 图标路径, 'IMAGE')  # 使用显示名作为键
#             except KeyError as e:
#                 if "already exists" in str(e):
#                     continue  # 如果已经加载则跳过
#                 raise  # 其他错误继续抛出
#     return 图标预览

# 1.2.0类管理图标
class 图标预览():
    _预览 = None    # 图标预览集缓存

    def __class_getitem__(cls, 图标名称:str) -> int:
        """支持 图标管理器["某图标"] 语法"""
        return cls.加载()[图标名称].icon_id

    @classmethod
    def 加载(cls):
        """首次调用时加载，之后直接返回缓存"""
        if cls._预览 is None:
            cls._预览 = previews.new()
            图标文件夹 = os.path.join(os.path.dirname(__file__), "图标")
            for 文件名 in os.listdir(图标文件夹):
                图标名称 = os.path.splitext(文件名)[0]
                图标路径 = os.path.join(图标文件夹, 文件名)
                if os.path.exists(图标路径) and 图标名称 not in cls._预览:
                    try:
                        cls._预览.load(图标名称, 图标路径, 'IMAGE')
                    except KeyError as e:
                        if "already exists" not in str(e):
                            raise
        return cls._预览

    @classmethod
    def 卸载(cls):
        """插件注销时调用"""
        if cls._预览 is not None:
            previews.remove(cls._预览)
            cls._预览 = None