# coding: utf-8

from .贴图.基础贴图 import 获取基础贴图

def 脸部着色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图):
    材质输出节点 = (材质.node_tree.nodes.get("材质输出") or 材质.node_tree.nodes.get("Material Output"))  # 找到材质输出节点
    MMD着色节点组 = 材质.node_tree.nodes["mmd_shader"]
    if MMD着色节点组.inputs[12].default_value == 0:
        透明节点 = 材质.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')  # 新建透明节点
        透明节点.location = (-200, 1600)  # 定位透明节点
        材质.node_tree.links.new(
            透明节点.outputs[0],  # 节点组的输出插槽
            材质输出节点.inputs['Surface']  # 输出节点的输入插槽
        )
        self.report({"INFO"}, f'材质Material["{材质.name}"]根据MMDShaderDev的alpha值为0设为透明')
        return  # 如果MMD节点组设置为透明，材质直接输出透明，然后进入下一个循环
    脸节点组 = 材质.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    SDF贴图节点组 = 材质.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    已找到 = False
    已找到SDF = False
    for 节点组 in 数据源.node_groups:  # 设置材质节点组并输出材质
        if 节点组.type == 'SHADER' and ("脸" in 节点组.name or "face" in 节点组.name):  # 搜索材质节点组
            self.report({"INFO"}, f'材质Material["{材质.name}"]应用节点组:ShaderNodeNodeTree["{节点组.name}"]')
            脸节点组.node_tree = 节点组  # 应用节点组
            脸节点组.location = (-200, 1500)  # 定位节点组
            已找到 = True  # 记录已找到
        if 节点组.type == 'SHADER' and 节点组.name == "SDF.tex":
            SDF贴图节点组.node_tree = 节点组  # 获取节点组
            SDF贴图节点组.location = (-800, 1500)  # 定位节点组
            已找到SDF = True  # 记录已找到
        # 当两个节点组都找到时，跳出循环
        if 已找到 and 已找到SDF:
            break
    材质.node_tree.links.new(
        脸节点组.outputs[0],  # 节点组的输出插槽
        材质输出节点.inputs['Surface']  # 输出节点的输入插槽
    )
    if 偏好.导入贴图:  # 如果开启了导入贴图
        原始贴图节点,基础贴图 = 获取基础贴图(self, 材质, 匹配贴图)  # 基础贴图
        if 基础贴图:
            self.report({"INFO"}, f'材质Material["{材质.name}"]输入贴图:Texture["{基础贴图.name}"]')
            图像节点 = 材质.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
            图像节点.image = 基础贴图  # 应用贴图
            if alpha贴图:
                if 基础贴图 in alpha贴图:
                    图像节点.image.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
            图像节点.location = (-500, 1500)  # 定位图像节点
            材质.node_tree.links.new(
                图像节点.outputs[0],  # 图像节点的输出插槽
                脸节点组.inputs[0]  # 输出节点的输入插槽
            )
        else:
            self.report({"WARNING"}, f'材质Material["{材质.name}"]未找到匹配的基础贴图')
            if 原始贴图节点:  # 薇塔的眼睛2材质没有基础贴图
                材质.node_tree.links.new(
                    原始贴图节点.outputs[0],  # 图像节点的输出插槽
                    脸节点组.inputs[0]  # 输出节点的输入插槽
                )
