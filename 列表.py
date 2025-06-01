import bpy
from bpy.props import StringProperty
from .图标 import 加载图标
图标预览 = 加载图标()

class GameTemplateItem(bpy.types.PropertyGroup):  # 必须在偏好前定义
    """存储单个游戏模板数据"""
    名称: StringProperty(
        name="",
        description="游戏名称"
    )

class GAME_UL_TemplateList(bpy.types.UIList):
    """自定义游戏模板列表"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        # 紧凑模式布局
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            行 = layout.row(align=True)
            行.alignment = 'LEFT'

            # 显示图标
            icon_id = 图标预览[item.名称].icon_id
            行.label(text=item.名称, icon_value=icon_id)

def 游戏列表添加(游戏):
    偏好 = bpy.context.preferences.addons["导入小二"].preferences
    for 东西 in 偏好.游戏列表:
        if 东西.名称 == 游戏:
            return
    东西 = 偏好.游戏列表.add()
    东西.名称 = 游戏