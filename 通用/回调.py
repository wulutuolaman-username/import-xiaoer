import bpy, inspect
from typing import cast
from ..指针 import XiaoerObject

def 判断类型(模型):
    if isinstance(模型, bpy.types.Object) and 模型.type == 'MESH':
        return True
    else:
        return False

# 1.1.2针对fbx模型多网格
def 回调(函数, *位置参数, **关键字参数):

    入口模型 = None
    # 根据类型找到位置参数中的模型
    for 模型 in 位置参数:
        if 判断类型(模型):
            入口模型 = 模型
            break
    骨架 = cast(XiaoerObject, 入口模型.parent)

    # 递归时需要替换模型
    def 调用(当前模型):
        # 动态生成参数列表，将模型参数替换
        sig = inspect.signature(函数)
        ba = sig.bind_partial(*位置参数, **关键字参数)
        print(ba.arguments)
        # 替换模型参数
        for name, val in ba.arguments.items():
            if 判断类型(val):
                ba.arguments[name] = 当前模型
                break
        print(ba.arguments)
        函数(*ba.args, **ba.kwargs)

    集合 = {入口模型}  # 不需要递归的物体集合
    if 骨架:
        def 递归(骨架):
            # self.report({"INFO"}, f"{骨架.name} {骨架.type}")
            if 骨架 not in 集合:
                集合.add(骨架)
                # self.report({"INFO"}, f"当前递归 {骨架.name} {datetime.datetime.now()}")
                for 模型 in 骨架.children:
                    # self.report({"INFO"}, f"{骨架.name} 当前子级 {模型.name} {datetime.datetime.now()}")
                    if 模型.type == 'MESH' and not 模型.rigid_body:  # 排除面部定位和刚体
                        # self.report({"INFO"}, f"{骨架.name} 子级网格 {模型.name} {datetime.datetime.now()}")
                        调用(模型)
                    elif 模型.children:
                        for 物体 in 模型.children:
                            # self.report({"INFO"}, f"{骨架.name} 当前孙级 {物体.name} {datetime.datetime.now()}")
                            递归(物体)
                if 骨架.parent:
                    # self.report({"INFO"}, f"{骨架.name} 当前父级 {骨架.parent.name} {datetime.datetime.now()}")
                    递归(骨架.parent)
        递归(骨架)
    else:
        调用(入口模型)