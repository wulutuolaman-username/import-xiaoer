import bpy
import datetime

class XiaoerAddonPresetsInformation(bpy.types.PropertyGroup):
    """ 小二插件导入模型预设信息 """

    def 获取渲染作者(self):
        if self.使用插件:
            return "小二今天吃啥啊"
        return ""  # 返回空字符串，而不是 None
    渲染作者: bpy.props.StringProperty(
        name="渲染",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=获取渲染作者
    )

    def 获取插件作者(self):
        if self.使用插件:
            return "五路拖拉慢"
        return ""  # 返回空字符串，而不是 None
    插件作者: bpy.props.StringProperty(
        name="插件",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=获取插件作者
    )

    使用插件: bpy.props.BoolProperty(
        name="使用插件",
        default=False,
    )

    导入完成: bpy.props.BoolProperty(
        name="导入完成",
        description="已完成导入模型预设，取消可再次导入预设",
        default=False,
    )

    def 文件路径(self):
        return self.get("文件路径","")
    文件: bpy.props.StringProperty(
        name="文件",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=文件路径,
    )

    def 角色名称(self):
        return self.get("角色名称","")
    角色: bpy.props.StringProperty(
        name="角色",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=角色名称,
    )

    def 使用时间(self):
        return self.get("使用时间","")
    时间: bpy.props.StringProperty(
        name="时间",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=使用时间,
    )

    def 使用版本(self):
        return self.get("使用版本","")
    版本: bpy.props.StringProperty(
        name="版本",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=使用版本
    )
def 小二预设属性(属性, 文件路径, 角色):
    from ..__init__ import bl_info
    属性.使用插件 = True
    属性["文件路径"] = str(文件路径)
    属性["角色名称"] = 角色
    属性["使用时间"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    属性["使用版本"] = ".".join(map(str, bl_info["version"]))
def 小二预设模型属性(模型, 文件路径, 角色):
    小二预设属性(模型.小二预设模型, 文件路径, 角色)
def 小二预设材质属性(材质, 文件路径, 角色):
    小二预设属性(材质.小二预设材质, 文件路径, 角色)
def 小二预设贴图属性(贴图, 文件路径, 角色):
    小二预设属性(贴图.小二预设贴图, 文件路径, 角色)
    贴图.小二预设贴图.导入完成 = True
def 小二预设节点属性(节点, 文件路径, 角色):
    小二预设属性(节点.小二预设节点, 文件路径, 角色)
    节点.小二预设节点.导入完成 = True
def 小二预设节点组属性(节点组, 文件路径, 角色):
    小二预设属性(节点组.小二预设节点树, 文件路径, 角色)
    节点组.小二预设节点树.导入完成 = True