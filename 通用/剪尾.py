# coding: utf-8

# 1.0.5新增
def 剪去后缀(名称):
    """去掉 .001, .002 等后缀"""
    if len(名称) > 4 and 名称[-4] == '.' and 名称[-3:].isdigit():
        return 名称[:-4], 名称[-4:]
    return 名称, None