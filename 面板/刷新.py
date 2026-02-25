import bpy
from ..指针 import *

# Window
#  └── Screen
#       └── Area
#            └── Region

def 刷新3D视图UI面板():
    """ 强制刷新UI """
    for 窗体 in bpy.context.window_manager.windows:
        for 屏幕 in [窗体.screen]:
            for 区域 in 屏幕.areas:  # type:小二对象|bpy.types.Area
                if 区域.判断类型.编辑器.是3D视图:
                    for 面板 in 区域.regions:  # type:小二对象|bpy.types.Region
                        if 面板.判断类型.分区.是UI面板:
                            面板.tag_redraw()