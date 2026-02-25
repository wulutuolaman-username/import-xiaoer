import os, bpy  # noqa: F401
from ...通用.改名 import 模型名称处理
from ...通用.路径 import 获取模型路径
from ...偏好.获取偏好 import 获取偏好
from ...偏好.获取游戏 import 获取游戏
from ...指针 import *

class ExecuteTemplateUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "制作预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_6"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    @classmethod  # 1.0.3新增
    def poll(cls, context):
        偏好 = 获取偏好()
        return 偏好.开启制作预设

    # 定义一个绘制函数
    def draw(self, context):
        偏好 = 获取偏好()
        游戏 = 获取游戏()

        布局 = self.layout

        # 选择预设模板
        行 = 布局.row()
        左侧 = 行.split(factor=0.4)  # 分割行，左侧占40%宽度
        左侧.label(text = "选择游戏")
        右侧 = 左侧.column(align=True)  # 右侧子行
        右侧.operator("import_xiaoer.open_addon_prefs", text="打开偏好设置", icon='PREFERENCES')

        框 = 布局.box()
        框.template_list(
            "GAME_UL_TemplateList",  # UIList类名
            "template_list",         # 列表ID
            偏好, "游戏列表", # 数据集合
            偏好, "当前列表选项索引" # 当前选中索引
        )

        # 导入贴图开关
        行 = 布局.row(align=True)
        行.scale_y = 1.2
        行.prop(偏好, "导入贴图", text="导入贴图", icon='IMPORT')

        导入贴图设置列 = 布局.column(align=True)
        导入贴图设置列.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用

        # 1.2.0增加边缘哈希算法
        行 = 导入贴图设置列.row(align=True)
        行.alignment = 'CENTER'
        左部 = 行.row()
        左部.label(text="基础贴图通过")
        左部.scale_x = 2 # 导致下一行 偏好.贴图来源 的按钮占用面板空间不均匀
        # 左部.ui_units_x = 18  # 导致下一行 偏好.贴图来源 的按钮占用面板空间不均匀
        行.prop(偏好, "匹配方式", expand=True)
        行.label(text="匹配")

        # 获取贴图路径方式设置
        行 = 导入贴图设置列.row()  # align=True受到上一行影响导致分布不均匀
        行.prop(偏好, "贴图来源", expand=True)  # 1.1.2
        行 = 导入贴图设置列.row(align=True)
        if 偏好.贴图来源 == '搜索':
            if 偏好.贴图目录 and os.path.exists(偏好.贴图目录):
                行.label(text = f"贴图目录：{偏好.贴图目录}", icon='VIEWZOOM')
            elif not 偏好.贴图目录:
                行.alert = True
                行.label(text=f"偏好未设置贴图目录", icon='ERROR')
            elif not os.path.exists(偏好.贴图目录):
                行.alert = True
                行.label(text=f"偏好贴图目录不存在", icon='ERROR')
        if 偏好.贴图来源 == '指定':  # 1.1.0增加对应的指定贴图路径
            列 = 行.column()
            列.prop(偏好, "贴图文件夹", text="", icon='FOLDER_REDIRECT')
        if 偏好.贴图来源 == '模型':  # 1.1.0增加对应的使用模型路径
            模型 = context.active_object  # type:小二物体|bpy.types.Object
            if 模型.判断类型.物体.是网格:
                模型路径 = 获取模型路径(None, 模型)
                if 模型路径 and os.path.exists(模型路径):
                    行.label(text=f"{模型路径}", icon='OUTLINER_OB_ARMATURE')
                else:
                    角色 = 模型名称处理(模型)
                    行 = 导入贴图设置列.row(align=True)
                    if not 模型路径:
                        行.alert = True
                        行.label(text=f"未找到{角色}模型导入路径", icon='ERROR')
                    elif not os.path.exists(模型路径):
                        行.alert = True
                        行.label(text=f"无效路径{模型路径}", icon='ERROR')
            elif not 模型:
                行.label(text=f"未选中模型", icon='ERROR')
            elif not 模型.判断类型.物体.是网格:
                行.label(text=f"选中项 {模型.name} 非网格物体", icon='ERROR')

        行 = 导入贴图设置列.row(align=True)
        列 = 行.column()
        列.ui_units_x = 6  # 设置固定宽度单位
        列.enabled = 偏好.检测透明材质
        # 列.prop(偏好, "射线法检测透明", text="射线法", icon='ORIENTATION_LOCAL')  # 1.1.0
        # 列.prop(偏好, "面积法检测透明", text="面积法", icon='OVERLAY')  # 1.1.0
        # 列.prop(偏好, "检测方式", expand=True)  # 1.1.2
        列.prop_enum(偏好, "检测方式", '射线')  # 1.1.2
        列.prop_enum(偏好, "检测方式", '面积')  # 1.1.2
        列 = 行.column()
        列.scale_y = 2.0  # 让这一行更宽
        列.prop(偏好, "检测透明材质", text="检测透明材质", icon='MATERIAL')  # 1.1.0

        # 连接基础贴图alpha
        if 游戏 == "原神":
            行 = 导入贴图设置列.row()
            if 偏好.连接基础贴图alpha:  #1.1.0
                行.prop(偏好, "连接基础贴图alpha", text="连接基础贴图alpha", icon='LINKED')
            else:
                行.prop(偏好, "连接基础贴图alpha", text="连接基础贴图alpha", icon='UNLINKED')  # 1.0.9

        # 全选模型 #1.0.10在制作面板增加按钮
        行 = 布局.row()
        行.scale_y = 2
        行.operator("import_xiaoer.select_model", text="选中模型", icon='RESTRICT_SELECT_OFF')

        # 导入预设模板
        行 = 布局.row()
        行.scale_y = 2
        行.operator("import_xiaoer.execute_template", text="加载预设模板", icon='NODE')

        # 导出预设
        行 = 布局.row()
        行.scale_y = 2
        行.operator("import_xiaoer.export_mat_presets", text="导出预设", icon='EXPORT')