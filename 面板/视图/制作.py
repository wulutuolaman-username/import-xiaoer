import bpy
import os
from ...通用.改名 import 模型名称处理
from ...通用.路径 import 获取模型路径

class ExecuteTemplateUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "制作预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_6"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    @classmethod  # 1.0.3新增
    def poll(cls, context):
        偏好 = context.preferences.addons["导入小二"].preferences
        return 偏好.开启制作预设

    # 定义一个绘制函数
    def draw(self, context):
        偏好 = context.preferences.addons["导入小二"].preferences
        选项 = 偏好.游戏列表[偏好.当前列表选项索引]
        游戏 = 选项.名称

        # 选择预设模板
        行 = self.layout.row()
        左侧 = 行.split(factor=0.4)  # 分割行，左侧占40%宽度
        左侧.label(text = "选择游戏")
        右侧 = 左侧.column(align=True)  # 右侧子行
        右侧.operator("import_xiaoer.open_addon_prefs", text="打开偏好设置", icon='PREFERENCES')

        框 = self.layout.box()
        框.template_list(
            "GAME_UL_TemplateList",  # UIList类名
            "template_list",         # 列表ID
            偏好, "游戏列表", # 数据集合
            偏好, "当前列表选项索引" # 当前选中索引
        )

        # 导入贴图开关
        导入贴图设置列 = self.layout.column(align=True)
        导入贴图设置列.scale_y = 1.2
        行 = 导入贴图设置列.row()
        行.prop(偏好, "导入贴图", text="导入贴图", icon='IMPORT')

        # 获取贴图路径方式设置
        行 = 导入贴图设置列.row(align=True)
        行.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用
        列 = 行.column()
        列.prop(偏好, "搜索贴图文件夹", text="搜索贴图", toggle=True)
        列 = 行.column()
        列.prop(偏好, "指定贴图文件夹", text="指定路径", toggle=True)
        列 = 行.column()
        列.prop(偏好, "使用模型路径", text="模型路径", toggle=True)
        行 = 导入贴图设置列.row(align=True)
        行.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用
        if 偏好.搜索贴图文件夹:
            if 偏好.贴图目录 and os.path.exists(偏好.贴图目录):
                行.label(text = f"贴图目录：{偏好.贴图目录}", icon='VIEWZOOM')
            elif not 偏好.贴图目录:
                行.label(text=f"偏好未设置贴图目录", icon='ERROR')
            elif not os.path.exists(偏好.贴图目录):
                行.label(text=f"偏好贴图目录不存在", icon='ERROR')
        if 偏好.指定贴图文件夹:  # 1.1.0增加对应的指定贴图路径
            列 = 行.column()
            列.prop(偏好, "贴图文件夹", text="", icon='FOLDER_REDIRECT')
            # 列.label(text = f"{偏好.贴图文件夹}", icon='FOLDER_REDIRECT')
            # 列 = 行.column()
            # 键 = 列.operator("xiaoer.set_image_path", text="选择路径")
            # 键.属性 = "贴图文件夹"  # 将路径属性名传递给操作符
        if 偏好.使用模型路径:  # 1.1.0增加对应的使用模型路径
            模型 = context.active_object
            if 模型 and 模型.type == 'MESH':
                模型路径 = 获取模型路径(None, 模型)
                if 模型路径 and os.path.exists(模型路径):
                # if 模型.parent and 模型.parent.parent and 模型.parent.parent["import_folder"]:
                #     模型路径 = 模型.parent.parent["import_folder"]
                    行.label(text=f"{模型路径}", icon='OUTLINER_OB_ARMATURE')
                else:
                    角色 = 模型名称处理(模型)
                    行 = 导入贴图设置列.row(align=True)
                    if not 模型路径:
                        行.label(text=f"未找到{角色}模型导入路径", icon='ERROR')
                    elif not os.path.exists(模型路径):
                        行.label(text=f"无效路径{模型路径}", icon='ERROR')
                    # 行 = 导入贴图设置列.row(align=True)
                    # 行.label(text=f"可能是非mmd_tools导入的模型", icon='ERROR')
            elif not 模型:
                行.label(text=f"未选中模型", icon='ERROR')
            elif 模型.type != 'MESH':
                行.label(text=f"选中项 {模型.name} 非网格物体", icon='ERROR')

        # # 1.1.0设置基础贴图匹配方式
        # 行 = 导入贴图设置列.row(align=True)
        # 行.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用
        # 列 = 行.column()
        # # 列.scale_x = 2.0  # 让这一列更宽
        # 列.ui_units_x = 12  # 设置固定宽度单位
        # 列.label(text=f"基础贴图")
        # 列 = 行.column()
        # 列.prop(偏好, "基础贴图快速匹配", text="快速", toggle=True)
        # 列 = 行.column()
        # 列.prop(偏好, "基础贴图精确匹配", text="精确", toggle=True)
        # 列 = 行.column()
        # 列.label(text=f"匹配")

        # # 图像匹配精度
        # 行 = 导入贴图设置列.row(align=True)
        # 行.enabled = 偏好.导入贴图
        # 列 = 行.column()
        # 列.label(icon='CON_SIZELIMIT')
        # 列 = 行.column()
        # 列.prop(偏好, "哈希尺寸", text="哈希尺寸", slider=True)

        # 通过alpha混合贴图
        行 = 导入贴图设置列.row(align=True)
        行.enabled = 偏好.导入贴图
        # 列 = 行.column()
        # 列.prop(偏好, "通过alpha混合贴图", text="混合贴图", icon='IMAGE_ALPHA')  # 1.0.9
        # # 通过alpha混合透明
        # 列 = 行.column()
        # 列.prop(偏好, "通过alpha混合透明", text="混合透明", icon='IMAGE_ALPHA')  # 1.0.9
        列 = 行.column()
        列.ui_units_x = 6  # 设置固定宽度单位
        列.enabled = 偏好.检测透明材质
        列.prop(偏好, "射线法检测透明", text="射线法", icon='ORIENTATION_LOCAL')  # 1.1.0
        # 列 = 行.column()
        # 列.ui_units_x = 6  # 设置固定宽度单位
        # 列.enabled = 偏好.检测透明材质
        列.prop(偏好, "面积法检测透明", text="面积法", icon='OVERLAY')  # 1.1.0
        列 = 行.column()
        列.scale_y = 2.0  # 让这一行更宽
        列.prop(偏好, "检测透明材质", text="检测透明材质", icon='MATERIAL')  # 1.1.0

        # 连接基础贴图alpha
        if 游戏 == "原神":
            行 = 导入贴图设置列.row()
            行.enabled = 偏好.导入贴图
            if 偏好.连接基础贴图alpha:  #1.1.0
                行.prop(偏好, "连接基础贴图alpha", text="连接基础贴图alpha", icon='LINKED')
            else:
                行.prop(偏好, "连接基础贴图alpha", text="连接基础贴图alpha", icon='UNLINKED')  # 1.0.9

        # # 1.1.0设置贴图名称匹配方式
        # 行 = 导入贴图设置列.row(align=True)
        # if 游戏 != "绝区零":  # 绝区零必须严格匹配
        #     列 = 行.column(align=True)
        #     列.scale_x = 2.0  # 让这一列更宽
        #     列.label(text=f"贴图名称")
        #     列 = 行.column()
        #     列.prop(偏好, "贴图名称严格匹配", text="严格", toggle=True)
        #     列 = 行.column()
        #     列.prop(偏好, "贴图名称宽松匹配", text="宽松", toggle=True)
        #     列 = 行.column()
        #     列.label(text=f"匹配")
        #     行.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用

        # # 通过点乘混合法向
        # 行 = 导入贴图设置列.row()
        # 行.enabled = 偏好.导入贴图
        # 行.prop(偏好, "通过点乘混合法向", text="通过点乘混合法向", icon='NORMALS_FACE')  #1.0.10

        # 全选模型 #1.0.10在制作面板增加按钮
        行 = self.layout.row()
        行.scale_y = 2
        行.operator("import_xiaoer.select_model", text="选中模型", icon='RESTRICT_SELECT_OFF')

        # 导入预设模板
        行 = self.layout.row()
        行.scale_y = 2
        行.operator("import_xiaoer.execute_template", text="加载预设模板", icon='NODE')

        # 导出预设
        行 = self.layout.row()
        行.scale_y = 2
        行.operator("import_xiaoer.export_mat_presets", text="导出预设", icon='EXPORT')