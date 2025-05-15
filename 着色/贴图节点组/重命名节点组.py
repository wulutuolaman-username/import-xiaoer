# coding: utf-8

import bpy
import re
from ...通用.剪尾 import 剪去后缀

def 重命名节点组(self, 节点树):
    """自动处理节点组后缀：.001→2，有后缀的相似无后缀节点组+1"""
    原名,后缀 = 剪去后缀(节点树.name)
    if 后缀:
        原名节点组 = bpy.data.node_groups[原名]
        序号 = int(后缀[1:]) + 1  # 递增现有后缀
        分解名称 = re.compile(r"^([^\s-]+)([\s-].*)$") # 按空格或连字符分离名称，将空格或连字符分到后半部分
        分解部分 = 分解名称.match(原名)
        if 分解部分:
            前半 = 分解名称.match(原名).group(1)
            后半 = 分解名称.match(原名).group(2)
            if not re.search(r'\d', 原名节点组.name):  # 如果原节点组没有编号
                # self.report({"INFO"}, f'节点组["{original_node_group.name}"]')
                原名节点组.name = f"{前半}1{后半}"
                # self.report({"INFO"}, f'重命名["{original_node_group.name}"]')
            if 前半[-1].isdigit():
                前半 = 前半[:-1]
                while f"{前半}{序号}{后半}" in bpy.data.node_groups:
                    序号 += 1
            # self.report({"INFO"}, f'if match节点组["{node_tree.name}"]')
            节点树.name = f"{前半}{序号}{后半}"
            # self.report({"INFO"}, f'if match重命名["{node_tree.name}"]')

        else:
            if not re.search(r'\d', 原名节点组.name):  # 如果原节点组没有编号
                # self.report({"INFO"}, f'节点组["{original_node_group.name}"]')
                原名节点组.name = f"{原名}1"
                # self.report({"INFO"}, f'重命名["{original_node_group.name}"]')
            if 原名[-1].isdigit():
                原名 = 原名[:-1]
                while f"{原名}{序号}" in bpy.data.node_groups:
                    序号 += 1
            # self.report({"INFO"}, f'else节点组["{node_tree.name}"]')
            节点树.name = f"{原名}{序号}"
            # self.report({"INFO"}, f'else重命名["{node_tree.name}"]')