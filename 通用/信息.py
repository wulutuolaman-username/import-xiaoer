import bpy, traceback
from typing import Literal

def 报告信息(self:bpy.types.Operator|None, 状态: Literal['正常', '警告', '异常'], 信息):
    if 状态 == '正常':
        try:
            self.report({"INFO"}, 信息)
        except:
            print(f'正常 {信息}')
    if 状态 == '警告':
        try:
            self.report({"WARNING"}, 信息)
        except:
            print(f'警告 {信息}')
    if 状态 == '异常':
        try:
            self.report({"ERROR"}, 信息)
        except:
            print(f'异常 {信息}')

def 输出错误(self:bpy.types.Operator|None, e, 信息):
    错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    try:
        self.report({"ERROR"}, 信息+":\n"+错误信息)
    except:
        print(信息+":\n"+错误信息)
