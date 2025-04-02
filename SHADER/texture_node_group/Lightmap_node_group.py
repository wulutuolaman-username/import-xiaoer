# 找到ligthmap节点组
def lightmap_texture_node_group(game, material_node_group):
###################################################################################################
    if "崩坏三" in game or game == "原神":
        return next((node for node in material_node_group.node_tree.nodes if node.type == 'GROUP' and
                     node.node_tree.name.startswith("lig")), None)
###################################################################################################
    if game == "崩坏：星穹铁道":
        return next((node for node in material_node_group.node_tree.nodes if node.type == 'GROUP' and
                     node.node_tree.name.startswith("ilm")), None)
###################################################################################################