import bpy, datetime  # noqa: F401
from .预设 import *  # noqa: F401
from .模板 import *  # noqa: F401
from ..指针 import *
from ..偏好.获取偏好 import *

# 1.2.0明确导出列表
__all__ = ['小二预设模型属性', '小二预设材质属性', '小二预设贴图属性', '小二预设节点属性', '小二预设节点组属性', '小二预设模板属性']

def 小二预设属性(属性:XiaoerAddonPresetsInformation, 文件路径, 角色):
    from ..__init__ import bl_info
    属性.使用插件 = True
    属性["文件路径"] = str(文件路径)
    属性["角色名称"] = 角色
    属性["使用时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    属性["使用版本"] = ".".join(map(str, bl_info["version"]))
def 小二预设模型属性(模型:小二物体, 文件路径, 角色):
    小二预设属性(模型.小二预设模型, 文件路径, 角色)
def 小二预设材质属性(材质:小二材质, 文件路径, 角色):
    小二预设属性(材质.小二预设材质, 文件路径, 角色)
def 小二预设贴图属性(贴图:小二贴图, 文件路径, 角色):
    小二预设属性(贴图.小二预设贴图, 文件路径, 角色)
    贴图.小二预设贴图.导入完成 = True
def 小二预设节点属性(节点:小二节点, 文件路径, 角色):
    小二预设属性(节点.小二预设节点, 文件路径, 角色)
    节点.小二预设节点.导入完成 = True
def 小二预设节点组属性(节点组: 小二着色节点树 | 小二几何节点树 | 小二合成节点树, 文件路径, 角色):
    小二预设属性(节点组.小二预设节点树, 文件路径, 角色)
    节点组.小二预设节点树.导入完成 = True

def 小二预设模板属性(属性: XiaoerAddonPresetsTemplateInformation, 贴图路径, 文件路径, 游戏, 角色):
    from ..__init__ import bl_info
    模型 = bpy.context.object  # type:小二物体|bpy.types.Object
    if 模型.小二预设模板.使用插件:
        属性.使用插件 = True
        属性["文件路径"] = str(模型.小二预设模板.文件)
        属性["贴图路径"] = str(模型.小二预设模板.贴图)
        偏好 = 获取偏好()
        属性["游戏名称"] = 偏好.游戏列表[偏好.当前列表选项索引].名称
        属性["角色名称"] = 模型.小二预设模板.角色
    else:
        属性.使用插件 = True
        属性["文件路径"] = str(文件路径)
        属性["贴图路径"] = str(贴图路径)
        属性["游戏名称"] = 游戏
        属性["角色名称"] = 角色
    属性["使用时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    属性["使用版本"] = ".".join(map(str, bl_info["version"]))