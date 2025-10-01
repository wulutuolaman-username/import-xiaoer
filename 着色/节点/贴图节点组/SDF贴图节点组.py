def 获取SDF贴图节点组(游戏, 节点组列表, 材质):
    SDF贴图节点组 = 材质.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    SDF贴图集合 = set()
    组输出节点 = None
    for 节点组 in 节点组列表:  # 设置材质节点组并输出材质
        if 节点组.type == 'SHADER' and 节点组.name == "SDF.tex":
            SDF贴图节点组.node_tree = 节点组  # 获取节点组
            SDF贴图节点组.location = (-800, 1500)  # 定位节点组
            SDF贴图节点组.name = "小二插件：SDF贴图节点组"
            for 节点 in 节点组.nodes:  # 1.1.0智能插值
                if 节点.type == 'TEX_IMAGE':
                    节点.interpolation = 'Smart'
                if 节点.type == 'GROUP_OUTPUT' and 节点.is_active_output:
                    组输出节点 = 节点
            break
    return SDF贴图节点组