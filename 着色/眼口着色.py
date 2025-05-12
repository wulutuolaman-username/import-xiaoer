# coding: utf-8

from .贴图.基础贴图 import 获取基础贴图

def 眼口着色(self, 偏好, 数据源, 材质, 匹配贴图):
    调色节点组 = 材质.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    节点组 = next((ng for ng in 数据源.node_groups if ng.name == "眼睫"), None)  # 优先"眼睫"
    if not 节点组:
        for 节点组 in 数据源.node_groups:  # 设置材质节点组并输出材质
            if 节点组.type == 'SHADER' and any(节点组.name.startswith(后缀) for 后缀 in ["调色", "校色"]):  # 搜索材质节点组
                调色节点组.node_tree = 节点组  # 应用节点组
    else:
        调色节点组.node_tree = 节点组  # 应用节点组
    self.report({"INFO"}, f'材质Material["{材质.name}"]应用节点组:ShaderNodeNodeTree["{调色节点组.node_tree.name}"]')
    调色节点组.location = (-200, 1500)  # 定位节点组
    材质输出节点 = (材质.node_tree.nodes.get("材质输出") or 材质.node_tree.nodes.get("Material Output"))  # 找到材质输出节点
    alpha = 材质.node_tree.nodes["mmd_shader"].inputs[12].default_value
    if alpha < 1:
        透明节点 = 材质.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')  # 新建透明节点
        透明节点.location = (-200, 1600)  # 定位透明节点
        混合节点 = 材质.node_tree.nodes.new(type='ShaderNodeMixShader')  # 新建混合节点
        混合节点.location = (250, 1500)  # 定位混合节点
        混合节点.inputs[0].default_value = alpha
        材质.node_tree.links.new(
            透明节点.outputs[0],  # 节点组的输出插槽
            混合节点.inputs[1]  # 输出节点的输入插槽
        )
        材质.node_tree.links.new(
            调色节点组.outputs[0],  # 节点组的输出插槽
            混合节点.inputs[2]  # 输出节点的输入插槽
        )
        材质.blend_method = 'BLEND'  # 材质模式
        self.report({"INFO"}, f'材质Material["{材质.name}"]根据MMDShaderDev的alpha设置透明')
        # material.node_tree.links.new(
        #     mix_node.outputs[0],  # 节点的输出插槽
        #     output_node.inputs['Surface']  # 输出节点的输入插槽
        # )
    else:  # 材质节点组直接输出
        材质.node_tree.links.new(
            调色节点组.outputs[0],  # 节点组的输出插槽
            材质输出节点.inputs['Surface']  # 输出节点的输入插槽
        )
    if 偏好.导入贴图:  # 如果开启了导入贴图
        原始贴图节点,基础贴图 = 获取基础贴图(self, 材质, 匹配贴图)  # 基础贴图
        if 基础贴图:
            self.report({"INFO"}, f'材质Material["{材质.name}"]输入贴图:Texture["{基础贴图.name}"]')
            图像节点 = 材质.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
            图像节点.image = 基础贴图  # 应用贴图
            图像节点.location = (-500, 1500)  # 定位图像节点
            材质.node_tree.links.new(
                图像节点.outputs[0],  # 图像节点的输出插槽
                调色节点组.inputs[0]  # 输出节点的输入插槽
            )
        else:
            self.report({"WARNING"}, f'材质Material["{材质.name}"]未找到匹配的基础贴图')
            if 原始贴图节点:  # 薇塔的眼睛2材质没有基础贴图
                材质.node_tree.links.new(
                    原始贴图节点.outputs[0],  # 图像节点的输出插槽
                    调色节点组.inputs[0]  # 输出节点的输入插槽
                )
