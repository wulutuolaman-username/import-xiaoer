import bpy

# 清理材质图像
def clean_material_image(node):
    image = node.image
    # 检查最后 4 个字符
    suffix = node.image.name[-4:]
    if suffix[0] == '.' and suffix[1:].isdigit():
        new_name = image.name[:-4]
        new_image = bpy.data.images.get(new_name)
        if new_image:
            node.image = new_image
        else:
            node.image.name = new_name
    # bpy.ops.outliner.orphans_purge()  # 清除孤立数据

# 整理MMD刚体材质
def clean_mmd_tools_rigid_material():
    for i, rigid_material in enumerate(bpy.data.materials):
        if rigid_material.name.startswith("mmd_tools_rigid_"):
            if rigid_material.name[-3:].isdigit():
                new_name = rigid_material.name[:-4]
                new_material = bpy.data.materials.get(new_name)
                if new_material:
                    bpy.data.materials[i] = new_material

# 整理MMD固有节点组
def clean_mmd_tools_node_group():
    for i, mmd_node_group in enumerate(bpy.data.node_groups):
        if mmd_node_group.name.startswith("MMDTexUV") or mmd_node_group.name.startswith("MMDShaderDev"):
            if mmd_node_group.name[-3:].isdigit():
                new_name = mmd_node_group.name[:-4]
                mmd_node_group.name = new_name