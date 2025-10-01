from .混合透明 import 混合透明
from ...属性.模板 import 小二预设模板属性

def 混合贴图(self, 材质, 图像节点, 贴图节点, 材质节点组, 材质输出节点):
    贴图节点.location = (-840, 1600)
    映射范围 = 材质.node_tree.nodes.new(type='ShaderNodeMapRange')
    映射范围.location = (-550, 1440)
    小二预设模板属性(映射范围.小二预设模板, None, None, None, None)
    混合颜色 = 材质.node_tree.nodes.new(type='ShaderNodeMix')
    混合颜色.location = (-375, 1500)
    混合颜色.data_type = 'RGBA'
    小二预设模板属性(混合颜色.小二预设模板, None, None, None, None)
    材质.node_tree.links.new(图像节点.outputs[1], 映射范围.inputs[0])
    材质.node_tree.links.new(图像节点.outputs[1], 映射范围.inputs[1])
    材质.node_tree.links.new(映射范围.outputs[0], 混合颜色.inputs[0])
    材质.node_tree.links.new(图像节点.outputs[0], 混合颜色.inputs[6])
    材质.node_tree.links.new(贴图节点.outputs[0], 混合颜色.inputs[7])
    材质.node_tree.links.new(混合颜色.outputs[2], 材质节点组.inputs[0])
    混合透明(self, 材质, 图像节点, 图像节点, 材质节点组, 材质输出节点)
    框 = 材质.node_tree.nodes.new(type='NodeFrame')
    框.label = "小二插件：通过alpha混合贴图"
    框.location = (-600, 1500)  # 定位
    映射范围.parent = 框
    混合颜色.parent = 框
    小二预设模板属性(框.小二预设模板, None, None, None, None)