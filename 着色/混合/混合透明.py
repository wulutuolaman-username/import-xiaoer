from ...通用.信息 import 报告信息
from ...着色.节点.透明.透明节点 import 获取透明节点
from ...着色.节点.透明.混合节点 import 获取混合节点
from ...着色.节点.透明.区域节点 import 获取区域节点

def 混合透明(self, 材质, 图像节点, 贴图节点, 材质节点组, 材质输出节点):
    透明节点 = 获取透明节点(材质, '小二插件：透明节点')
    混合节点 = 获取混合节点(材质, '小二插件：混合节点')
    区域节点 = 获取区域节点(材质, '小二插件：通过alpha混合透明')
    # print(透明节点.name, 混合节点.name, 区域节点.name)
    if 贴图节点:
        alpha = MMDalpha(材质)
        if alpha == 1:
            材质.node_tree.links.new(
                贴图节点.outputs[1],  # 节点组的输出插槽
                混合节点.inputs[0]  # 输出节点的输入插槽
            )
    # print(1)
    材质.node_tree.links.new(
        透明节点.outputs[0],  # 节点组的输出插槽
        混合节点.inputs[1]  # 输出节点的输入插槽
    )
    # print(2)
    if 材质节点组:
        材质.node_tree.links.new(
            材质节点组.outputs[0],  # 节点组的输出插槽
            混合节点.inputs[2]  # 输出节点的输入插槽
        )
        # print(3)
    else:
        材质.node_tree.links.new(
            贴图节点.outputs[0],  # 节点组的输出插槽
            混合节点.inputs[2]  # 输出节点的输入插槽
        )
    材质.node_tree.links.new(
        混合节点.outputs[0],  # 节点组的输出插槽
        材质输出节点.inputs['Surface']  # 输出节点的输入插槽
    )
    # print(4)
    透明节点.parent = 区域节点
    混合节点.parent = 区域节点
    材质.小二预设模板.透明材质 = True  # 记录透明材质，之后在几何节点设置无描边
    材质.小二预设模板.透明更新 = True
    # print(材质.name, 材质.小二预设模板.透明材质, 材质.小二预设模板.透明更新, 5)
    报告信息(self, '正常', f'材质Material["{材质.name}"]通过alpha混合透明')

def MMDalpha(材质):
    # alpha = 1
    # MMD着色节点组 = 材质.node_tree.nodes.get("mmd_shader")
    # if MMD着色节点组:
    #     alpha = MMD着色节点组.inputs[12].default_value
    try:
        alpha = 材质.mmd_material.alpha
    except:
        alpha = 1
    return alpha