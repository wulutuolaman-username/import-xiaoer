import bpy  # type:ignore
from .属性.预设 import *  # type:ignore
from .属性.模板 import *  # type:ignore
from .属性.物体 import *
from .属性.材质 import *
from .属性.图像 import *
from .属性.节点 import *
from .属性.几何 import *
from .属性.窗口 import *
from .通用.类型 import *
from .通用.新建 import *

# 代码参考：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/properties/__init__.py
指针属性 = {
    bpy.types.Object: {
    "小二预设模型":bpy.props.PointerProperty(type=XiaoerAddonModelPresetsInformation),
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
    # bpy.types.NodeGroup: {  # 这是群组节点
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
    bpy.types.WindowManager: {  # 1.2.0模块安装进度
    "小二预设模板": bpy.props.PointerProperty(type=XiaoerAddonWindowManagerInformation),
    }
}

# # 1.2.0明确导出列表
# __all__ = ['小二对象', '小二物体', '小二材质', '小二贴图', '小二节点', '小二着色节点树', '小二几何节点树', '小二合成节点树', '小二窗口',
#            '注册指针', '注销指针']
#
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     物体 = bpy.types.Object
#     材质 = bpy.types.Material
#     贴图 = bpy.types.Image
#     节点 = bpy.types.Node
#     着色节点树 = bpy.types.ShaderNodeTree
#     几何节点树 = bpy.types.GeometryNodeTree
#     合成节点树 = bpy.types.CompositorNodeTree
#     窗口 = bpy.types.WindowManager
# else:
#     物体, 材质, 贴图, 节点, 着色节点树, 几何节点树, 合成节点树, 窗口 = (object,) * 8
#
# # 1.2.0包装属性判断类型
class 小二对象:
    判断类型: 类型判断器
#     def __init__(self, 对象):
#         self._对象 = 对象
#     # def __getattr__(self, name):
#     #     return getattr(self._对象, name)  # 透传给原生对象
#     # def __getattr__(self, name):
#     #     属性 = getattr(self._对象, name)
#     #     # 如果是方法，包一层确保用原生对象调用
#     #     if callable(属性):
#     #         def 包装(*args, **kwargs):
#     #             return 属性(*args, **kwargs)
#     #         return 包装
#     #     return 属性
#     @property  # 把方法伪装成属性，访问时不需要加括号
#     def 判断类型(self) -> 类型判断器:
#         return 类型判断器(self._对象)
# ❌ 不能让 小二物体 同时继承 小二对象 和 bpy.types.Object
# 因为 bpy.types.Object 是 Blender 的 C 扩展类型（bpy_struct 子类），不允许被 Python 多继承。
# 1.1.2添加IDE类型注解
class 小二物体(bpy.types.Object):
    小二预设模型: XiaoerAddonModelPresetsInformation
    小二预设模板: XiaoerAddonModelPresetsTemplateInformation
    判断类型: 类型判断器
    新建修改器: 新建修改器
    # @property
    # def 新建修改器(self) -> 新建修改器: return 新建修改器(self._对象)
    # @property
    # def 原对象(self) -> bpy.types.Object:  # ← 覆盖返回类型
    #     return self._对象
class 小二材质(bpy.types.Material):
    小二预设材质: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonMaterialPresetsTemplateInformation
    判断类型: 类型判断器
    type: any
    class mmd_material:
        alpha: any
class 小二贴图(bpy.types.Image):
    小二预设贴图: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonImagePresetsTemplateInformation
    判断类型: 类型判断器
class 小二节点(bpy.types.Node):
    小二预设节点: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonNodePresetsTemplateInformation
    判断类型: 类型判断器
    node_tree: any
class 小二着色节点树(bpy.types.ShaderNodeTree):
    小二预设节点树: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonPresetsTemplateInformation
    判断类型: 类型判断器
    新建节点: 新建着色节点
    # @property
    # def 新建节点(self) -> 新建着色节点: return 新建着色节点(self._对象)
class 小二几何节点树(bpy.types.GeometryNodeTree,):
    小二预设节点树: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonGeometryNodeTreePresetsTemplateInformation
    判断类型: 类型判断器
    新建节点: 新建几何节点
    # @property
    # def 新建节点(self) -> 新建几何节点: return 新建几何节点(self._对象)
    class interface:  # blender4.0
        items_tree: any
        def new_socket(name: str, in_out, socket_type: str):...
class 小二合成节点树(bpy.types.CompositorNodeTree):
    小二预设节点: XiaoerAddonPresetsInformation
    小二预设模板: XiaoerAddonPresetsTemplateInformation
    判断类型: 类型判断器
    新建节点: 新建合成节点
    # @property
    # def 新建节点(self) -> 新建合成节点: return 新建合成节点(self._对象)
class 小二窗口(bpy.types.WindowManager):
    小二预设模板: XiaoerAddonWindowManagerInformation
    判断类型: 类型判断器

# 需要注入判断类型的所有bpy类型
注入类型列表 = [
    bpy.types.Object,
    bpy.types.Material,
    bpy.types.Image,
    bpy.types.Node,
    bpy.types.ShaderNodeTree,
    bpy.types.GeometryNodeTree,
    bpy.types.CompositorNodeTree,
    bpy.types.Modifier,
    bpy.types.NodeSocket,
    # bpy.types.WindowManager,
    # bpy.types.Screen,
    bpy.types.Area,
    bpy.types.Region,
]

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

    # 注入判断类型
    for 类型 in 注入类型列表:
        try:
            setattr(类型, '判断类型', property(lambda self: 类型判断器(self)))
        except Exception as e:
            print(f"无法注入 {类型.__name__}.判断类型: {e}")

    setattr(bpy.types.Object,                     '新建修改器', property(lambda self: 新建修改器(self)))
    setattr(bpy.types.ShaderNodeTree,             '新建节点', property(lambda self: 新建着色节点(self)))
    setattr(bpy.types.GeometryNodeTree,           '新建节点', property(lambda self: 新建几何节点(self)))
    setattr(bpy.types.CompositorNodeTree,         '新建节点', property(lambda self: 新建合成节点(self)))

def 注销指针():
    for 类型, 属性 in 指针属性.items():
        for 属性名称 in 属性.keys():
            if hasattr(类型, 属性名称):
                delattr(类型, 属性名称)

    # 注销判断类型
    for 类型 in 注入类型列表:
        if hasattr(类型, '判断类型'):
            try:
                delattr(类型, '判断类型')
            except Exception as e:
                print(f"无法注销 {类型.__name__}.判断类型: {e}")

    delattr(bpy.types.Object,                     '新建修改器')
    delattr(bpy.types.ShaderNodeTree,             '新建节点')
    delattr(bpy.types.GeometryNodeTree,           '新建节点')
    delattr(bpy.types.CompositorNodeTree,         '新建节点')
