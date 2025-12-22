import os, bpy
from ..通用.改名 import 模型名称处理
from .深度检索 import 深度检索
from ..偏好.偏好设置 import XiaoerAddonPreferences
from ..指针 import XiaoerObject

def 查找贴图(self:bpy.types.Operator, 偏好:XiaoerAddonPreferences, 模型:XiaoerObject, 游戏):

    if not 偏好.贴图目录 or not os.path.exists(偏好.贴图目录):
        return None, None

    匹配名称 = 模型名称处理(模型)
    最大匹配 = 0  # 名称最大匹配长度
    候选路径 = set()
    替换表 = str.maketrans('', '', '0123456789._')  # 创建翻译表，删除数字、小数点、下划线
    for 目录, 子目录, 文件列表 in os.walk(偏好.贴图目录):
        for 文件夹 in 子目录:
            名称 = 文件夹.translate(替换表)
            路径 = os.path.join(目录, 文件夹)
            if any(字符 in 名称 for 字符 in 匹配名称):
                匹配长度 = len(set(名称) & set(匹配名称))
                if 匹配长度 > 最大匹配:
                    最大匹配 = 匹配长度
                候选路径.add(路径)
            # if 名称 in 匹配名称:  # 如果处理后的模型名称包含了文件夹名称
            #     # if 名称 != None:  # 1.1.0搜索到的贴图文件夹不能是纯数字和小数点
            #         return 路径, 名称
    剔除路径 = set()
    for 路径 in 候选路径:
        文件夹 = os.path.basename(路径)
        名称 = 文件夹.translate(替换表)
        匹配长度 = len(set(名称) & set(匹配名称))
        if 匹配长度 < 最大匹配:
            # 候选预设.remove(预设)  # 不能在遍历集合时改变集合元素数量
            剔除路径.add(路径)
    候选路径 -= 剔除路径  # 剔除匹配长度不够的预设
    if len(候选路径) == 1:
        路径 = 候选路径.pop()
        文件夹 = os.path.basename(路径)
        名称 = 文件夹.translate(替换表)
        return 路径, 名称
    elif len(候选路径) > 1:
        return 深度检索(self, 模型, 候选路径, 游戏)
    return None, None  # 1.0.10改动