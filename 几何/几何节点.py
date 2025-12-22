# coding: utf-8

import bpy
from ..通用.剪尾 import 剪去后缀
from ..指针 import XiaoerGeometryNodeTree

# 代码来源：峰峰居士
def 几何节点(模型:bpy.types.Object, 节点组:XiaoerGeometryNodeTree):
    名称1, 后缀1 = 剪去后缀(节点组.name)
    节点组角色 = 节点组.小二预设节点树.角色
    if 节点组角色 and 节点组.name.endswith(f'_{节点组角色}'):
        名称1 = 名称1.rsplit('_', 1)[0]  # 节点组可能重命名
    # 1.1.1检查Blender版本是否小于4.0，将几何节点的输出插槽设置为插槽的名称
    if bpy.app.version[0] < 4:
        for o in 节点组.outputs:
            if not o.default_attribute_name:
                o.default_attribute_name = o.name
    else:
        for o in 节点组.interface.items_tree:
            if o.item_type == 'SOCKET' and o.in_out == 'OUTPUT':
                if not o.default_attribute_name:
                    o.default_attribute_name = o.name
    # 为选中网格应用几何节点
    if 模型.type == 'MESH':
        for 修改器 in 模型.modifiers:
            if 修改器.type == 'NODES':
                节点树 = bpy.data.node_groups.get(修改器.node_group.name)
                名称2, 后缀2 = 剪去后缀(节点树.name)
                节点树角色 = 节点树.小二预设节点树.角色
                if 节点树角色 and 节点树.name.endswith(f'_{节点树角色}'):
                    名称2 = 名称2.rsplit('_', 1)[0]  # 节点组可能重命名
                if 名称1 == 名称2:  # 1.1.0导入前清除重复的几何节点，不可删除节点组导致fbx其他网格出现数据源缺失几何节点组
                    # bpy.data.node_groups.remove(节点树)
                    模型.modifiers.remove(修改器)
        修改器 = 模型.modifiers.new(name=节点组.name, type='NODES')
        修改器.node_group = 节点组
        名称, 后缀 = 剪去后缀(节点组.name)
        节点组.name = 名称
        节点组.小二预设模板.应用修改器 = True