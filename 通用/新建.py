# import bpy
#
# def 新建节点(类型):  # 1.2.0闭包新建节点
#     def 节点(节点树:bpy.types.NodeTree):
#         return 节点树.nodes.new(type=类型)
#     return 节点

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..指针 import *

# 1.2.0明确导出列表
__all__ = ['新建着色节点', '新建几何节点', '新建合成节点', '新建修改器']

# 1.2.0闭包新建对象
def 节点(节点树, 类型) -> '小二节点':
    return 节点树.nodes.new(type=类型)  # bl_idname

def 组输出(self): return 节点(self._节点树, 'NodeGroupOutput')
def 转接点(self): return 节点(self._节点树, 'NodeReroute')
def 帧(self): return 节点(self._节点树, 'NodeFrame')

class 新建着色节点:
    def __init__(self, 节点树):
        self._节点树 = 节点树
    @property
    def 组输出(self): return 组输出(self)
    @property
    def 转接点(self): return 转接点(self)
    @property
    def 帧(self): return 帧(self)
    @property
    def 群组(self): return 节点(self._节点树, 'ShaderNodeGroup')
    @property
    def 材质输出(self): return 节点(self._节点树, 'ShaderNodeOutputMaterial')
    @property
    def 映射范围(self): return 节点(self._节点树, 'ShaderNodeMapRange')
    @property
    def 混合(self): return 节点(self._节点树, 'ShaderNodeMix')
    @property
    def 混合着色器(self): return 节点(self._节点树, 'ShaderNodeMixShader')
    @property
    def 透明(self): return 节点(self._节点树, 'ShaderNodeBsdfTransparent')
    @property
    def 图像(self): return 节点(self._节点树, 'ShaderNodeTexImage')

class 新建几何节点:
    def __init__(self, 节点树):
        self._节点树 = 节点树
    @property
    def 组输出(self): return 组输出(self)
    @property
    def 转接点(self): return 转接点(self)
    @property
    def 帧(self): return 帧(self)
    @property
    def 群组(self): return 节点(self._节点树, 'GeometryNodeGroup')
    @property
    def 布尔(self): return 节点(self._节点树, 'FunctionNodeBooleanMath')
    @property
    def 材质选择(self): return 节点(self._节点树, 'GeometryNodeMaterialSelection')

class 新建合成节点:
    def __init__(self, 节点树):
        self._节点树 = 节点树
    @property
    def 组输出(self): return 组输出(self)
    @property
    def 转接点(self): return 转接点(self)
    @property
    def 帧(self): return 帧(self)
    @property
    def 渲染层(self): return 节点(self._节点树, 'CompositorNodeRLayers')
    @property
    def 合成(self): return 节点(self._节点树, 'CompositorNodeComposite')  # blender 5.0 合成器只有组输出
    @property
    def 预览器(self): return 节点(self._节点树, 'CompositorNodeViewer')
    @property
    def 辉光(self): return 节点(self._节点树, 'CompositorNodeGlare')

# @property
# 把方法伪装成属性，访问时不需要加括号：
# 没有 @property
# 对象.判断类型()   # 要加括号
#
# 有 @property
# 对象.判断类型     # 不加括号，像访问普通属性一样
# 对象.判断类型.物体.是网格()  # 所以链式调用才自然

def 修改器(模型, 名称, 类型):
    return 模型.modifiers.new(name=名称, type=类型)

class 新建修改器:
    def __init__(self, 模型):
        self._模型 = 模型
    # 需要传入名称 不需要@property
    def 几何节点修改器(self, 名称): return 修改器(self._模型, 名称, 'NODES')