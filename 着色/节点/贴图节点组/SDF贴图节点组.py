from ....指针 import *

def 获取SDF贴图节点组(游戏, 节点组列表, 材质):
    节点树 = 材质.node_tree   # type:小二着色节点树
    SDF贴图节点组 = 节点树.新建节点.群组
    SDF贴图集合 = set()
    组输出节点 = None
    for 节点组 in 节点组列表:   # type:小二着色节点树  # 设置材质节点组并输出材质
        if 节点组.判断类型.节点树.是着色节点树 and 节点组.name == "SDF.tex":
            SDF贴图节点组.node_tree = 节点组  # 获取节点组
            SDF贴图节点组.location = (-800, 1500)  # 定位节点组
            SDF贴图节点组.name = "小二插件：SDF贴图节点组"
            for 节点 in 节点组.nodes:   # type:小二节点  # 1.1.0智能插值
                if 节点.判断类型.节点.着色.是图像:
                    节点.interpolation = 'Smart'
                if 节点.判断类型.节点.是组输出 and 节点.is_active_output:  #type:ignore
                    组输出节点 = 节点
            break
    return SDF贴图节点组