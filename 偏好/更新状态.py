import bpy
from typing import TYPE_CHECKING

# 1.1.2只在类型检查时导入，避免运行时循环导入
if TYPE_CHECKING:
    from ..偏好.偏好设置 import *
    from ..指针 import *

# Python 允许类型注解写字符串 → 不会触发 import → 也就不会循环导入
def 更新基础贴图alpha连接(self: '小二偏好', context:bpy.types.Context):
    from ..着色.节点.材质节点组.材质节点组 import 搜索材质节点组
    from ..着色.节点.贴图.基础贴图 import 搜索基础贴图节点
    物体 = context.active_object  # type:小二物体|bpy.types.Object
    if 物体.判断类型.物体.是网格:
        # print(context.active_object.name)
        for 材质 in 物体.data.materials:  # type:小二材质
            材质节点组 = 搜索材质节点组(材质)
            基础贴图节点 = 搜索基础贴图节点(材质)
            if 基础贴图节点 and 材质节点组 and len(材质节点组.inputs) > 1 and "alpha" in 材质节点组.inputs[1].name.lower():
                # print(材质.name, 材质节点组.name, 基础贴图节点.name)
                if self.连接基础贴图alpha and not 基础贴图节点.小二预设模板.已连接基础贴图alpha:
                    材质.node_tree.links.new(基础贴图节点.outputs[1], 材质节点组.inputs[1])
                    基础贴图节点.小二预设模板.已连接基础贴图alpha = True
                    # print(f"{材质.name}已连接基础贴图alpha")
                if not self.连接基础贴图alpha and 基础贴图节点.小二预设模板.已连接基础贴图alpha:
                    材质.node_tree.links.remove(next((连接 for 连接 in 材质.node_tree.links
                      if 连接.from_socket== 基础贴图节点.outputs[1] and 连接.to_socket == 材质节点组.inputs[1]),None))
                    基础贴图节点.小二预设模板.已连接基础贴图alpha = False
    return None