import bpy
from .模板 import XiaoerAddonPresetsTemplateInformation
from ..着色.更新.更新材质 import 更新材质
from ..着色.更新.更新透明 import 更新透明

class XiaoerAddonMaterialPresetsTemplateInformation(XiaoerAddonPresetsTemplateInformation):

    def 材质代码分类(self):
        return self.初始分类
    代码分类: bpy.props.StringProperty(
        name="代码分类",
        description="已禁用:此属性仅供内部使用,无法编辑",
        get=材质代码分类,
    )
    初始分类: bpy.props.StringProperty(
        name="初始分类",
        description="插件代码的材质分类结果",
    )
    材质分类: bpy.props.EnumProperty(
        name="材质分类",
        description="材质分类结果，可修改类型重新查找节点组",
        items=[
        ('', " ", ""),
        ('脸部', "脸部材质", ""),
        ('五官', "五官材质", "使用调色节点组"),
        ('表情', "表情材质", "使用调色节点组，默认透明"),
        ('头发', "头发材质", ""),
        ('皮肤', "皮肤材质", "和衣服材质节点组相同，但是描边材质不同"),
        ('衣服', "衣服材质", ""),
        ],
        default='',
        update=更新材质,
    )
    更新分类: bpy.props.StringProperty(
        name="更新分类",
        default='',
    )

    使用检测透明材质: bpy.props.BoolProperty(
        name="使用检测透明材质",
        default=False,
    )
    def 检测透明材质结果(self):
        return self.检测结果
    检测为透明材质: bpy.props.BoolProperty(
        name="检测为透明材质",
        description="已禁用:此属性仅供内部使用,无法编辑",
        default=False,
        get=检测透明材质结果
    )
    检测结果: bpy.props.BoolProperty(
        name="透明更新",
        default=False,
    )

    透明材质: bpy.props.BoolProperty(
        name="透明材质",
        description="可以手动更新材质为透明着色",
        default=False,
        update=lambda self, context: 更新透明(self, context),
    )
    透明更新: bpy.props.BoolProperty(
        name="透明更新",
        default=False,
    )

    基础贴图: bpy.props.EnumProperty(
        name="基础贴图",
        items=lambda self, context: context.object.小二预设模板.基础贴图枚举项,
    )
    完成匹配基础贴图: bpy.props.BoolProperty(
        name="完成匹配基础贴图",
        default=False,
    )

    混合模式: bpy.props.StringProperty()
    显示背面: bpy.props.BoolProperty()