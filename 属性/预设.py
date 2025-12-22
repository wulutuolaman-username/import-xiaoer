import bpy

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