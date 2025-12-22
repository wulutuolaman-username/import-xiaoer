import bpy, datetime
from typing import cast
from .预设 import XiaoerAddonPresetsInformation
from .模板 import XiaoerAddonPresetsTemplateInformation
from ..指针 import XiaoerObject, XiaoerMaterial, XiaoerImage, XiaoerNode, XiaoerShaderNodeTree, XiaoerGeometryNodeTree, XiaoerCompositorNodeTree
from ..偏好.获取偏好 import 获取偏好

def 小二预设属性(属性:XiaoerAddonPresetsInformation, 文件路径, 角色):
    from ..__init__ import bl_info
    属性.使用插件 = True
    属性["文件路径"] = str(文件路径)
    属性["角色名称"] = 角色
    属性["使用时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    属性["使用版本"] = ".".join(map(str, bl_info["version"]))
def 小二预设模型属性(模型:XiaoerObject, 文件路径, 角色):
    小二预设属性(模型.小二预设模型, 文件路径, 角色)
def 小二预设材质属性(材质:XiaoerMaterial, 文件路径, 角色):
    小二预设属性(材质.小二预设材质, 文件路径, 角色)
def 小二预设贴图属性(贴图:XiaoerImage, 文件路径, 角色):
    小二预设属性(贴图.小二预设贴图, 文件路径, 角色)
    贴图.小二预设贴图.导入完成 = True
def 小二预设节点属性(节点:XiaoerNode, 文件路径, 角色):
    小二预设属性(节点.小二预设节点, 文件路径, 角色)
    节点.小二预设节点.导入完成 = True
def 小二预设节点组属性(节点组:XiaoerShaderNodeTree|XiaoerGeometryNodeTree|XiaoerCompositorNodeTree, 文件路径, 角色):
    小二预设属性(节点组.小二预设节点树, 文件路径, 角色)
    节点组.小二预设节点树.导入完成 = True

def 小二预设模板属性(属性: XiaoerAddonPresetsTemplateInformation, 贴图路径, 文件路径, 游戏, 角色):
    from ..__init__ import bl_info
    模型 = cast(XiaoerObject, bpy.context.object)
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