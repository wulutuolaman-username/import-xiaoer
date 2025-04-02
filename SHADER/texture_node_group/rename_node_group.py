import bpy
import re

def rename_node_group(self,node_tree):
    """自动处理节点组后缀：.001→2，有后缀的相似无后缀节点组+1"""
    suffix_pattern = re.compile(r"(.*?)(\.\d+)?$")  # 分离名称和后缀
    # 分解名称
    match = suffix_pattern.match(node_tree.name)
    original_name = match.group(1)
    current_suffix = match.group(2)
    original_node_group = bpy.data.node_groups[original_name]
    num = int(current_suffix[1:]) + 1  # 递增现有后缀
    pattern = re.compile(r"^([^\s-]+)([\s-].*)$") # 按空格或连字符分离名称，将其分到后半部分
    match = pattern.match(original_name)
    if match:
        part1_name = pattern.match(original_name).group(1)
        part2_name = pattern.match(original_name).group(2)
        if part1_name[-1].isdigit():
            part1_name = part1_name[:-1]
            while f"{part1_name}{num}{part2_name}" in bpy.data.node_groups:
                num += 1
        # self.report({"INFO"}, f'if match节点组["{node_tree.name}"]')
        node_tree.name = f"{part1_name}{num}{part2_name}"
        # self.report({"INFO"}, f'if match重命名["{node_tree.name}"]')
        if not re.search(r'\d', original_node_group.name):  # 如果原节点组没有编号
            # self.report({"INFO"}, f'节点组["{original_node_group.name}"]')
            original_node_group.name = f"{part1_name}1{part2_name}"
            # self.report({"INFO"}, f'重命名["{original_node_group.name}"]')
    else:
        if original_name[-1].isdigit():
            original_name = original_name[:-1]
            while f"{original_name}{num}" in bpy.data.node_groups:
                num += 1
        # self.report({"INFO"}, f'else节点组["{node_tree.name}"]')
        node_tree.name = f"{original_name}{num}"
        # self.report({"INFO"}, f'else重命名["{node_tree.name}"]')
        if not re.search(r'\d', original_node_group.name):  # 如果原节点组没有编号
            # self.report({"INFO"}, f'节点组["{original_node_group.name}"]')
            original_node_group.name = f"{original_name}1"
            # self.report({"INFO"}, f'重命名["{original_node_group.name}"]')