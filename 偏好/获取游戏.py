from .获取偏好 import *
from ..列表 import *

def 获取游戏():
    偏好 = 获取偏好()
    选项 = 偏好.游戏列表[偏好.当前列表选项索引]  # type:GameTemplateItem
    游戏 = 选项.名称
    return 游戏