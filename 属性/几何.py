# coding: utf-8

import bpy
from .模板 import XiaoerAddonPresetsTemplateInformation

class XiaoerAddonGeometryNodeTreePresetsTemplateInformation(XiaoerAddonPresetsTemplateInformation):

    # 1.1.0fbx模型分离
    """
    对fbx模型多网格导入预设时，需要给不同网格应用相同的几何节点组。
    导出预设时将几何节点修改器的节点组设为False，
    导入预设、加载模板时，第一次通过使用次数找到节点组，然后设为True，
    之后fbx其他网格再次应用时，根据此属性找到需要作为修改器的几何节点组。
    """
    应用修改器:bpy.props.BoolProperty(
        name="应用修改器",
        default=False,
    )