from ...指针 import *

def 是图像(节点:小二节点) -> bool:
    return 节点.判断类型.节点.着色.是图像

def 是群组(节点:小二节点) -> bool:
    return 节点.判断类型.节点.是群组

def 是合并XYZ(节点:小二节点) -> bool:
    return 节点.判断类型.节点.着色.是合并XYZ

def 是法线贴图(节点:小二节点) -> bool:
    return 节点.判断类型.节点.着色.是法线贴图