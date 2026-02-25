import bpy  # noqa: F401
from .混合透明 import 混合透明
from ...属性.属性 import 小二预设模板属性
from ...指针 import *

def 混合贴图(self:bpy.types.Operator, 材质, 图像节点, 贴图节点, 材质节点组, 材质输出节点):
    节点树 = 材质.node_tree # type:小二着色节点树
    贴图节点.location = (-840, 1600)
    映射范围 = 节点树.新建节点.映射范围
    映射范围.location = (-550, 1440)
    小二预设模板属性(映射范围.小二预设模板, None, None, None, None)
    混合颜色 = 节点树.新建节点.混合
    混合颜色.location = (-375, 1500)
    混合颜色.data_type = 'RGBA'
    小二预设模板属性(混合颜色.小二预设模板, None, None, None, None)
    节点树.links.new(图像节点.outputs[1], 映射范围.inputs[0])
    节点树.links.new(图像节点.outputs[1], 映射范围.inputs[1])
    节点树.links.new(映射范围.outputs[0], 混合颜色.inputs[0])
    节点树.links.new(图像节点.outputs[0], 混合颜色.inputs[6])
    节点树.links.new(贴图节点.outputs[0], 混合颜色.inputs[7])
    节点树.links.new(混合颜色.outputs[2], 材质节点组.inputs[0])
    混合透明(self, 材质, 图像节点, 图像节点, 材质节点组, 材质输出节点)
    框 = 节点树.新建节点.帧
    框.label = "小二插件：通过alpha混合贴图"
    框.location = (-600, 1500)  # 定位
    映射范围.parent = 框
    混合颜色.parent = 框
    小二预设模板属性(框.小二预设模板, None, None, None, None)