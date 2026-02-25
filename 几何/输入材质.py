# coding: utf-8

import bpy  # noqa: F401
from .打包材质 import 布尔节点
from ..通用.信息 import 报告信息
from ..指针 import *

def 跳过转接点找到相连节点(节点:小二节点) -> 小二节点 | bpy.types.Node | bpy.types.NodeGroup:
    """ 递归追踪转接节点（Reroute），返回最终连接的节点 """
    if 节点.判断类型.节点.是转接点:
        if 节点.inputs and 节点.inputs[0].is_linked:
            连接 = 节点.inputs[0].links[0]
            return 跳过转接点找到相连节点(连接.from_node)
    return 节点

# 分类设置描边材质
def 输入材质(self, 节点:小二节点, 材质类):
    材质去重 = set()
    for 材质 in 材质类:
        if 材质 in 材质去重:
            材质类.remove(材质)
        else:
            材质去重.add(材质)
    global 材质节点
    接口类 = []  # 建立列表存储需要连接的接口
    for 输入 in 节点.inputs:  # type: 小二对象|bpy.types.NodeSocket
        if 输入.判断类型.接口.是布尔 and 输入.is_linked:  # 设置材质节点的布尔接口
            # self.report({"INFO"}, f"布尔接口:" + str(输入))
            for 连接 in 输入.links:
                相连节点 = 跳过转接点找到相连节点(连接.from_node)
                if 相连节点.判断类型.节点.是群组:  # 确保相连的是节点组
                    for 材质节点 in sorted(相连节点.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # type:小二节点  # 按位置从上到下
                        if 材质节点.判断类型.节点.几何.是材质选择:
                            # AttributeError: 'NodeSocketMaterial' object has no attribute 'material'
                            接口 = 材质节点.inputs[0]
                            接口.default_value = None  # 清空材质接口
                            接口类.append(接口)
                    # self.report({"INFO"}, f"接口:" + str(接口))
                    if len(材质类) > len(接口类):
                        布尔节点(self, 相连节点, 材质类[len(接口类):], 材质节点.location)
                    break
    # 使用 zip 将材质和接口一一对应
    for 材质, 接口 in zip(材质类, 接口类):
        接口.default_value = 材质  # 输入材质
        报告信息(self, '正常', f'GeometryNodeTree["{接口.node.id_data.name}"]输入材质:Material["{材质.name}"]')