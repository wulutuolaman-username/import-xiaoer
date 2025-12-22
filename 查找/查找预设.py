import os, bpy
from ..通用.改名 import 模型名称处理
from ..通用.剪尾 import 剪去后缀
from .处理文件 import 处理文件
from .深度检索 import 深度检索
from ..偏好.偏好设置 import XiaoerAddonPreferences
from ..指针 import XiaoerObject

def 查找预设(self:bpy.types.Operator, 偏好:XiaoerAddonPreferences, 模型:XiaoerObject):

    if not 偏好.预设目录 or not os.path.exists(偏好.预设目录):
        return None, None
    名称, 后缀 = 剪去后缀(模型.name)
    if 偏好.查找预设深度检索:
        匹配名称 = 模型名称处理(模型)
    else:
        匹配名称 = 模型名称处理(模型, 星穹铁道=True)
    最大匹配 = 0
    候选预设 = set()
    同名预设 = set()  # 文件名处理后和模型匹配名称完全相同的预设
    # self.report({"INFO"}, 匹配名称)
    for 目录, 子目录, 文件列表 in os.walk(偏好.预设目录):
        for 文件 in 文件列表:
            if 文件.endswith(".blend"):
                角色 = 处理文件(文件)
                路径 = os.path.join(目录, 文件)
                if 匹配名称 in 角色:
                    # self.report({"INFO"}, f"{角色}\n{匹配名称}\n{文件}\n{路径}")
                    同名预设.add(路径)
                # 1.1.0深度检索
                if 偏好.查找预设深度检索:
                    if any(字符 in 角色 for 字符 in 匹配名称):
                        匹配长度 = len(set(角色)&set(匹配名称))
                        if 匹配长度 > 最大匹配:
                            最大匹配 = 匹配长度
                    # for 字符 in 匹配名称:
                    #     if 字符 in 角色:
                    #         self.report({"INFO"}, f"检测到{角色}包含{字符}")
                        候选预设.add(路径)
                else:
                    if 角色 in 匹配名称:  # 如果模型名称包含了处理以后的文件名
                        return 路径, 角色
    if len(同名预设) == 1:
        路径 = 同名预设.pop()
        文件 = os.path.basename(路径)
        角色 = 处理文件(文件)
        self.report({"INFO"}, f"{模型.name}唯一同名预设\n{路径}")
        return 路径, 角色
    # 1.1.0深度检索
    if 偏好.查找预设深度检索:
        剔除预设 = set()
        for 预设 in 候选预设:
            文件 = os.path.basename(预设)
            角色 = 处理文件(文件)
            匹配长度 = len(set(角色) & set(匹配名称))
            if 匹配长度 < 最大匹配:
                # 候选预设.remove(预设)  # 不能在遍历集合时改变集合元素数量
                剔除预设.add(预设)
        候选预设 -= 剔除预设  # 剔除匹配长度不够的预设
        if len(候选预设) == 1:
            路径 = 候选预设.pop()
            文件 = os.path.basename(路径)
            角色 = 处理文件(文件)
            return 路径, 角色
        elif len(候选预设) > 1:
            return 深度检索(self, 模型, 候选预设)
    return None, None  # 1.0.9改动