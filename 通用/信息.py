from typing import Literal

def 报告信息(self, 状态: Literal['正常', '异常'], 信息):
    if 状态 == '正常':
        try:
            self.report({"INFO"}, 信息)
        except:
            print(f'正常 {信息}')
    if 状态 == '异常':
        try:
            self.report({"ERROR"}, 信息)
        except:
            print(f'异常 {信息}')