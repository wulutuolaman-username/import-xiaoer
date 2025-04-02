from ..texture.Shadow_Ramp import shadow_ramp_texture

def ramp_texture_node(self,game,material,material_node_group,diffuse_image):
###################################################################################################
    if game == "原神":
        Shadow_Ramp_image = shadow_ramp_texture(self,game, diffuse_image)
        if Shadow_Ramp_image:
            ramp_material_node_group = next((node for node in material_node_group.node_tree.nodes
                    if node.type == 'GROUP' and
                    node.node_tree.name.startswith("ramp.")), None)
            ramp_tex_node_group = next((node for node in ramp_material_node_group.node_tree.nodes
                        if node.type == 'GROUP' and
                        node.node_tree.name.startswith("ramptex.")), None)
            ramp_node = next((node for node in ramp_tex_node_group.node_tree.nodes
                        if node.type == 'TEX_IMAGE'), None)  # 找到ramp贴图节点
            ramp_node.image = Shadow_Ramp_image
            self.report({"INFO"}, f'材质Material["{material.name}"]输入ramp贴图:Texture["{Shadow_Ramp_image.name}"]')
###################################################################################################
    if game == "崩坏：星穹铁道":
        Cool_Ramp_image,Warm_Ramp_image = shadow_ramp_texture(self,game, diffuse_image)
        if Cool_Ramp_image and Warm_Ramp_image:
            Ramp_image = [Warm_Ramp_image,Cool_Ramp_image]
            ramp_node_group = next((node for node in material_node_group.node_tree.nodes
                        if node.type == 'GROUP' and
                        node.node_tree.name.startswith("ramp")), None)
            tex_node = next((node for node in ramp_node_group.node_tree.nodes
                        if node.type == 'TEX_IMAGE'), None)
            Ramp_image_node = []
            if tex_node:  # 找到ramp贴图节点
                for ramp_node in sorted(ramp_node_group.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 从上到下
                    if ramp_node.type == 'TEX_IMAGE':
                        Ramp_image_node.append(ramp_node)
            else:  # 头发和衣服ramp贴图节点位置不同
                ramp_tex_node_group = next((node for node in ramp_node_group.node_tree.nodes
                        if node.type == 'GROUP' and
                        node.node_tree.name.startswith("ramp")), None)
                for ramp_node in sorted(ramp_tex_node_group.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 从上到下
                    if ramp_node.type == 'TEX_IMAGE':
                        Ramp_image_node.append(ramp_node)
            for ramp_node,Ramp_image in zip(Ramp_image_node,Ramp_image):
                ramp_node.image = Ramp_image
                self.report({"INFO"},f'材质Material["{material.name}"]输入ramp贴图:Texture["{Ramp_image.name}"]')
###################################################################################################