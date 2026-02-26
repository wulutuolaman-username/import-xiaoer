import bpy, site, importlib  # noqa: F401
from ..刷新 import *
from ...模块 import *
from ...指针 import *

class InformationFeedbackUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "信息反馈"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_2"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        布局 = self.layout

        行 = 布局.row()
        from ...__init__ import bl_info
        行.label(text=f"插件版本 " + ".".join(map(str, bl_info["version"])))

        # importlib.invalidate_caches()  # 重新扫描可导入模块
        # site.main()  # 重新加载 site-packages 路径，让新安装的包进入 sys.path

        窗口 = context.window_manager  # type:小二窗口|bpy.types.WindowManager

        模块正常 = True
        # 1.2.0面板显示安装进度
        def 显示安装情况(模块):
            nonlocal 模块正常
            行 = 布局.row()
            try:
                行.label(text=f"{导入名称[模块]} {获取版本(模块)}")
            except:
                模块正常 = False
                行.alert = True
                if   安装状态[模块] in ["正在下载", "正在安装"]:
                    框 = 行.box()
                    bpy.app.timers.register(刷新3D视图UI面板, first_interval=0.1)
                    框.label(text=f"{模块}模块{安装状态[模块]}......", icon='SCRIPTPLUGINS')
                    框.label(text=f"{安装状态[模块][-2:]}进度 {窗口.小二预设模板.已下载:.2f} / {窗口.小二预设模板.总大小:.2f}MB")
                elif 安装状态[模块] == "安装失败":
                    行.label(text=f"{模块}模块安装失败", icon='ERROR')
                    行 = 布局.row()
                    # 行.alignment = 'CENTER'
                    行.alert = True
                    行.label(text=f"切换系统控制台查看详情", icon='CONSOLE')
                else:
                    行.label(text=f"{模块}模块未安装", icon='ERROR')
        for 模块 in 模块列表:
            显示安装情况(模块)

        行 = 布局.row()
        if 模块正常:
            行.label(text="模块已安装成功", icon='CHECKBOX_HLT')
        else:
            行.alert = True
            行.label(text="模块导入失败", icon='ERROR')
            行 = 布局.row()
            行.operator("wm.console_toggle", icon='CONSOLE')
            行 = 布局.row()
            行.operator("import_xiaoer.restart_blender", icon='BLENDER')

        # if 检查轮子存在():
        行 = 布局.row()
        列 = 行.column()
        列.operator("import_xiaoer.install_packages", icon='IMPORT')
        列 = 行.column()
        列.operator("import_xiaoer.uninstall_packages", icon='TRASH')
        # elif not 模块正常:
        #     行 = 布局.row()
        #     行.operator(
        #         "wm.url_open",
        #         text="下载本地版安装模块",
        #         icon='TRIA_DOWN_BAR'
        #     ).url = "https://www.aplaybox.com/details/model/j8uwC55rjW4G"

        行 = 布局.row()
        行.scale_y = 2
        行.operator("screen.info_log_show", text="信息面板", icon='INFO')
        行 = 布局.row()
        行.operator(
            "wm.url_open",
            text="提交错误信息",
            icon='URL'
        ).url = "https://github.com/wulutuolaman-username/import-xiaoer/issues"
        行 = 布局.row(align=True)
        列 = 行.column()
        列.ui_units_x = 15  # 设置固定宽度单位
        列.label(text="联系插件作者")
        列 = 行.column()
        列.operator("wulutuolaman.open_website_tiktok",text="抖音")
        列 = 行.column()
        列.operator("wulutuolaman.open_website_bilibili",text="B站")