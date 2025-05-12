from ..贴图.Ramp贴图 import 获取Ramp贴图

def ramp节点组(self, 游戏, 材质, 材质节点组, 基础贴图):
###################################################################################################
    if 游戏 == "原神":
        Ramp贴图 = 获取Ramp贴图(self, 游戏, 基础贴图)
        if Ramp贴图:
            Ramp材质节点组 = next((node for node in 材质节点组.node_tree.nodes
                                             if node.type == 'GROUP' and
                                             node.node_tree.name.startswith("ramp.")), None)
            Ramp贴图节点组 = next((node for node in Ramp材质节点组.node_tree.nodes
                        if node.type == 'GROUP' and
                        node.node_tree.name.startswith("ramptex.")), None)
            Ramp节点 = next((node for node in Ramp贴图节点组.node_tree.nodes
                        if node.type == 'TEX_IMAGE'), None)  # 找到ramp贴图节点
            Ramp节点.image = Ramp贴图
            self.report({"INFO"}, f'材质Material["{材质.name}"]输入ramp贴图:Texture["{Ramp贴图.name}"]')
###################################################################################################
    if 游戏 == "崩坏：星穹铁道":
        冷Ramp,暖Ramp = 获取Ramp贴图(self, 游戏, 基础贴图)
        if 冷Ramp and 暖Ramp:
            Ramp贴图 = [暖Ramp,冷Ramp]
            Ramp节点组 = next((节点 for 节点 in 材质节点组.node_tree.nodes
                                    if 节点.type == 'GROUP' and
                                    节点.node_tree.name.startswith("ramp")), None)
            贴图节点 = next((节点 for 节点 in Ramp节点组.node_tree.nodes
                        if 节点.type == 'TEX_IMAGE'), None)
            Ramp贴图节点 = []
            if 贴图节点:  # 找到ramp贴图节点
                for Ramp节点 in sorted(Ramp节点组.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 从上到下
                    if Ramp节点.type == 'TEX_IMAGE':
                        Ramp贴图节点.append(Ramp节点)
            else:  # 头发和衣服ramp贴图节点位置不同
                Ramp贴图节点组 = next((节点 for 节点 in Ramp节点组.node_tree.nodes
                        if 节点.type == 'GROUP' and
                        节点.node_tree.name.startswith("ramp")), None)
                for Ramp节点 in sorted(Ramp贴图节点组.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 从上到下
                    if Ramp节点.type == 'TEX_IMAGE':
                        Ramp贴图节点.append(Ramp节点)
            for 节点,贴图 in zip(Ramp贴图节点,Ramp贴图):
                节点.image = 贴图
                self.report({"INFO"},f'材质Material["{材质.name}"]输入ramp贴图:Texture["{贴图.name}"]')
###################################################################################################