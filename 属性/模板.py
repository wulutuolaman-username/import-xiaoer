import bpy

class XiaoerAddonPresetsTemplateInformation(bpy.types.PropertyGroup):
    """ 小二插件模型预设模板信息 """

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

    加载完成: bpy.props.BoolProperty(
        name="加载完成",
        description="防止重复加载。"
                    # "已完成加载预设模板，取消可再次加载模板"
                    "（第一次加载预设模板必须导入所有贴图，"
                    "不要修改模型的贴图和节点组）",
        default=False,
    )

    def 文件路径(self):
        return self.get("文件路径","")
    文件: bpy.props.StringProperty(
        name="文件",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=文件路径,
    )

    def 贴图路径(self):
        return self.get("贴图路径","")
    贴图: bpy.props.StringProperty(
        name="贴图",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=贴图路径,
    )

    def 游戏名称(self):
        return self.get("游戏名称","")
    游戏: bpy.props.StringProperty(
        name="游戏",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=游戏名称,
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