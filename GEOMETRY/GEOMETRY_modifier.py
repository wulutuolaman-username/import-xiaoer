import bpy

# 应用几何节点
def GEOMETRY_modifier(model,node_group):
    # 检查Blender版本是否小于4.1，将几何节点的输出插槽设置为插槽的名称
    if bpy.app.version >= (4, 1, 0):
        for o in node_group.interface.items_tree:
            if o.item_type == 'SOCKET' and o.in_out == 'OUTPUT':
                if not o.default_attribute_name:
                    o.default_attribute_name = o.name
    else:
        for o in node_group.outputs:
            if not o.default_attribute_name:
                o.default_attribute_name = o.name
    # 为选中网格应用几何节点
    if model.type == 'MESH':
        modifier = model.modifiers.new(name=node_group.name, type='NODES')
        modifier.node_group = node_group