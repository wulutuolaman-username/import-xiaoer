import bpy
from ..属性.预设 import XiaoerAddonPresetsInformation
from ..属性.模板 import XiaoerAddonPresetsTemplateInformation
from ..属性.物体 import XiaoerAddonModelPresetsTemplateInformation, XiaoerAddonMaterial, XiaoerAddonImage, XiaoerAddonNodeTree
from ..属性.材质 import XiaoerAddonMaterialPresetsTemplateInformation
from ..属性.图像 import XiaoerAddonImagePresetsTemplateInformation, XiaoerAddonImageNodeTree
from ..属性.节点 import XiaoerAddonNodePresetsTemplateInformation
from ..属性.几何 import XiaoerAddonGeometryNodeTreePresetsTemplateInformation
from ..面板.属性.物体 import ModelObjectPanel, TemplateObjectPanel
from ..面板.属性.材质 import MaterialPanel, TemplateMaterialPanel
from ..面板.图像.图像 import ImagePanel, TemplateImagePanel
from ..面板.节点.节点 import NodePanel, TemplateNodePanel
from ..面板.节点.节点树 import NodeGroupPanel, TemplateNodeGroupPanel
from ..面板.节点.材质 import MaterialNodeTreePanel, TemplateMaterialNodeTreePanel

# 1.1.0注册属性
classes = (
    XiaoerAddonMaterial,
    XiaoerAddonImage,
    XiaoerAddonNodeTree,
    XiaoerAddonImageNodeTree,

    XiaoerAddonPresetsInformation,
    XiaoerAddonPresetsTemplateInformation,
    XiaoerAddonModelPresetsTemplateInformation,
    XiaoerAddonMaterialPresetsTemplateInformation,
    XiaoerAddonImagePresetsTemplateInformation,
    XiaoerAddonNodePresetsTemplateInformation,
    XiaoerAddonGeometryNodeTreePresetsTemplateInformation,

    ModelObjectPanel,
    MaterialPanel,
    ImagePanel,
    NodePanel,
    NodeGroupPanel,
    MaterialNodeTreePanel,

    TemplateObjectPanel,
    TemplateMaterialPanel,
    TemplateNodePanel,
    TemplateNodeGroupPanel,
    TemplateMaterialNodeTreePanel,
    TemplateImagePanel,
)

def 注册属性():
    for cls in classes:
        try:  # 1.0.8避免重复注册
            bpy.utils.register_class(cls)
        except:
            pass

def 注销属性():
    for clss in classes:
        try:
            bpy.utils.unregister_class(clss)
        except:
            pass