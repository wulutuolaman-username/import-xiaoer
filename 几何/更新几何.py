import bpy
# from ..通用.回调 import 回调
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..属性.物体 import *
    from ..指针 import *

def 更新描边开关(self:'XiaoerAddonModelPresetsInformation', context:bpy.types.Context):
    # 必须是骨架
    # 骨架 = context.object
    骨架 = self.id_data  # type:小二物体
    if 骨架.判断类型.物体.是骨架:
        for 网格 in 骨架.children:  # type:小二物体
            if 网格.判断类型.物体.是网格 and 网格.modifiers:
                for 修改器 in 网格.modifiers:  # type:小二对象
                    if 修改器.判断类型.修改器.是几何节点修改器:
                        节点组: 小二几何节点树
                        节点组 = 修改器.node_group  # type:ignore
                        if 节点组 and 节点组.name.startswith("Geometry Nodes"):
                            for 节点 in 节点组.nodes:  # type:小二节点
                                if 节点.判断类型.节点.是群组:
                                    if 节点.node_tree and 节点.node_tree.name.startswith("实体化描边"):
                                        输入接口, 节点接口, 输出接口 = (None,) * 3
                                        # 其实也可以考虑新建输出节点切换激活状态
                                        # print(self.描边开关)
                                        if 节点.inputs:
                                            for 接口 in 节点.inputs:  # type:小二对象|bpy.types.NodeSocket
                                                if 接口.判断类型.接口.是几何数据:
                                                    if 接口.is_linked:
                                                        # print('输入节点', 接口.links[0].from_node)
                                                        输入接口 = 接口.links[0].from_socket
                                                    break
                                        if 节点.outputs:
                                            for 接口 in 节点.outputs:  # type:小二对象|bpy.types.NodeSocket
                                                if 接口.判断类型.接口.是几何数据:
                                                    节点接口 = 接口
                                                    if 接口.is_linked:
                                                        # print('输出节点', 接口.links[0].to_node)
                                                        输出接口 = 接口.links[0].to_socket
                                                    break
                                        if self.描边开关:
                                        # elif 输入接口:
                                            for 连接 in 输入接口.links:
                                                if 连接.to_node != 节点:
                                                    # print('输出节点', 连接.to_node)
                                                    输出接口 = 连接.to_socket
                                                    break

                                        # print(输入接口)
                                        # print(节点接口)
                                        # print(输出接口)
                                        # print()
                                        if 输入接口 and 输出接口:
                                            if self.描边开关 and 节点接口:
                                                节点组.links.new(节点接口, 输出接口)
                                            else:
                                                节点组.links.new(输入接口, 输出接口)

                                        # def 更新状态(模型:XiaoerObject):
                                        #     模型.小二预设模型.描边开关 = self.描边开关
                                        # 回调(更新状态, 模型)

                                        return None


    return None
