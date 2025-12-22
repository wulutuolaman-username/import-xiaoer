# coding: utf-8

import bpy
from .模板 import XiaoerAddonPresetsTemplateInformation

class XiaoerAddonNodePresetsTemplateInformation(XiaoerAddonPresetsTemplateInformation):

    已连接基础贴图alpha: bpy.props.BoolProperty(
        name='已连接基础贴图alpha',
        default=False
    )