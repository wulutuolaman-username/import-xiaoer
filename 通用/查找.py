# coding: utf-8

import os

def 查找预设(偏好, 模型):
    if not 偏好.预设目录 or not os.path.exists(偏好.预设目录):
        return None

    for 目录, 子目录, 文件列表 in os.walk(偏好.预设目录):
        for 文件名 in 文件列表:
            if 文件名.endswith(".blend"):
                名称 = 文件名[:-6]  # 去掉.blend后缀
                角色 = 名称.replace("渲染", "")  # 去除文件名"渲染"字样
                角色 = 角色.replace("预设", "")  # 去除文件名"预设"字样
                if 角色 in 模型.name :  # 如果模型名称包含了处理以后的文件名
                    return os.path.join(目录, 文件名), 角色

# 自动查找贴图文件
def 查找贴图(偏好, 模型):
    if not 偏好.贴图目录 or not os.path.exists(偏好.贴图目录):
        return None

    匹配名称 = 模型.name.replace("_mesh", "")
    匹配名称 = 匹配名称.replace("【", "")
    匹配名称 = 匹配名称.replace("】", "")
    for 目录, 子目录, 文件列表 in os.walk(偏好.贴图目录):
        for 文件夹 in 子目录:
            if 文件夹 in 匹配名称:  # 如果处理后的模型名称包含了文件夹名称
                return os.path.join(目录, 文件夹),文件夹