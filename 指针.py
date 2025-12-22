import bpy
from .属性.预设 import XiaoerAddonPresetsInformation
from .属性.模板 import XiaoerAddonPresetsTemplateInformation
from .属性.物体 import XiaoerAddonModelPresetsTemplateInformation
from .属性.材质 import XiaoerAddonMaterialPresetsTemplateInformation
from .属性.图像 import XiaoerAddonImagePresetsTemplateInformation
from .属性.节点 import XiaoerAddonNodePresetsTemplateInformation
from .属性.几何 import XiaoerAddonGeometryNodeTreePresetsTemplateInformation

# 代码参考：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/properties/__init__.py
指针属性 = {
    bpy.types.Object: {
    "小二预设模型":bpy.props.PointerProperty(type=XiaoerAddonPresetsInformation),
    # "小二预设定位":bpy.props.PointerProperty(type=),
    # "小二预设灯光":bpy.props.PointerProperty(type=),
    "小二预设模板":bpy.props.PointerProperty(type=XiaoerAddonModelPresetsTemplateInformation),
    },
    bpy.types.Material:{
    "小二预设材质":bpy.props.PointerProperty(type=XiaoerAddonPresetsInformation),
    "小二预设模板":bpy.props.PointerProperty(type=XiaoerAddonMaterialPresetsTemplateInformation),
    },
    bpy.types.Image:{
    "小二预设贴图":bpy.props.PointerProperty(type=XiaoerAddonPresetsInformation),
    "小二预设模板":bpy.props.PointerProperty(type=XiaoerAddonImagePresetsTemplateInformation),
    },
    bpy.types.Node: {
    "小二预设节点":bpy.props.PointerProperty(type=XiaoerAddonPresetsInformation),
    "小二预设模板":bpy.props.PointerProperty(type=XiaoerAddonNodePresetsTemplateInformation),
    },
    # bpy.types.NodeGroup: {
    # "小二预设节点组": bpy.props.PointerProperty(type=XiaoerAddonImportModelPresetsInformation),
    # # "小二预设模板":bpy.props.PointerProperty(type=),
    # },
    bpy.types.ShaderNodeTree: {  # 直接针对着色节点树
    "小二预设节点树":bpy.props.PointerProperty(type=XiaoerAddonPresetsInformation),
    "小二预设模板":bpy.props.PointerProperty(type=XiaoerAddonPresetsTemplateInformation),
    },
    bpy.types.GeometryNodeTree: {  # 直接针对几何节点树
    "小二预设节点树":bpy.props.PointerProperty(type=XiaoerAddonPresetsInformation),
    "小二预设模板": bpy.props.PointerProperty(type=XiaoerAddonGeometryNodeTreePresetsTemplateInformation),
    },
    bpy.types.CompositorNodeTree: {  # 直接针对合成节点树
    "小二预设节点树": bpy.props.PointerProperty(type=XiaoerAddonPresetsInformation),
    "小二预设模板": bpy.props.PointerProperty(type=XiaoerAddonPresetsTemplateInformation),
    },

}

# 1.1.2添加IDE类型注解
class XiaoerObject(bpy.types.Object):
    小二预设模型: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonModelPresetsTemplateInformation
class XiaoerMaterial(bpy.types.Material):
    小二预设材质: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonMaterialPresetsTemplateInformation
    type: any
    class mmd_material():
        alpha: any
class XiaoerImage(bpy.types.Image):
    小二预设贴图: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonImagePresetsTemplateInformation
class XiaoerNode(bpy.types.Node):
    小二预设节点: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonNodePresetsTemplateInformation
    node_tree: any
class XiaoerShaderNodeTree(bpy.types.ShaderNodeTree):
    小二预设节点树: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonPresetsTemplateInformation
class XiaoerGeometryNodeTree(bpy.types.GeometryNodeTree):
    小二预设节点树: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonGeometryNodeTreePresetsTemplateInformation
    class interface():  # blender4.0
        items_tree: any
        def new_socket(name: str, in_out, socket_type: str):...
class XiaoerCompositorNodeTree(bpy.types.CompositorNodeTree):
    小二预设节点: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonPresetsTemplateInformation

def 注册指针():
    for 类型, 属性 in 指针属性.items():
        for 属性名称, 属性定义 in 属性.items():
            # 如果已经注册过同名属性，先删掉
            if hasattr(类型, 属性名称):
                print(f"覆盖已存在属性: {类型.__name__}.{属性名称}")
            try:
                # delattr(类型, 属性名称)
                setattr(类型, 属性名称, 属性定义)  # 动态添加属性
            except Exception as e:
                print(f"无法删除 {类型.__name__}.{属性名称}: {e}")
            # setattr(类型, 属性名称, 属性定义)  # 动态添加属性

def 注销指针():
    for 类型, 属性 in 指针属性.items():
        for 属性名称 in 属性.keys():
            if hasattr(类型, 属性名称):
                delattr(类型, 属性名称)
