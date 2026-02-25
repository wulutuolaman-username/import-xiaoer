import bpy
from .判断类型 import *

def 法线校正():
    法线贴图转换 = bpy.data.node_groups.get("法线贴图转换")
    if 法线贴图转换:
        合并XYZ = next((节点 for 节点 in 法线贴图转换.nodes if 是合并XYZ(节点)), None)  # type:ignore
        法线贴图 = next((节点 for 节点 in 法线贴图转换.nodes if 是法线贴图(节点)), None)  # type:ignore
        if 合并XYZ and 法线贴图:
            法线贴图转换.links.new(合并XYZ.outputs[0], 法线贴图.inputs[1])
