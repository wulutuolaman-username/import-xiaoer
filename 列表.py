import bpy
from .图标 import *
# 图标预览 = 加载图标()

# # 1.2.0明确导出列表
# __all__ = ['GameTemplateItem', 'GAME_UL_TemplateList', '游戏列表添加']

class GameTemplateItem(bpy.types.PropertyGroup):  # 必须在偏好前定义
    """存储单个游戏模板数据"""
    名称: bpy.props.StringProperty(
        name="",
        description="游戏名称"
    )

class GAME_UL_TemplateList(bpy.types.UIList):
    """自定义游戏模板列表"""
    # noinspection PyMethodOverriding
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        # 紧凑模式布局
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            行 = layout.row(align=True)
            行.alignment = 'LEFT'

            # 显示图标
            行.label(text=item.名称, icon_value=图标预览[item.名称])  # type: ignore

def 游戏列表添加(游戏):
    from .偏好.获取偏好 import 获取偏好
    偏好 = 获取偏好()
    for 选项 in 偏好.游戏列表:
        if 选项.名称 == 游戏:
            return
    选项 = 偏好.游戏列表.add()
    选项.名称 = 游戏