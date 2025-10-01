# coding: utf-8

import bpy
from .模板 import XiaoerAddonPresetsTemplateInformation

class XiaoerAddonGeometryNodeTreePresetsTemplateInformation(XiaoerAddonPresetsTemplateInformation):

    # 1.1.0fbx模型分离
    应用修改器:bpy.props.BoolProperty(
        name="应用修改器",
        default=False,
    )