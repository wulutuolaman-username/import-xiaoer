import bpy


class ExecuteTemplateUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "制作预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import5"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    @classmethod  # 1.0.3新增
    def poll(cls, context):
        偏好 = context.preferences.addons["导入小二"].preferences
        return 偏好.开启制作预设

    # 定义一个绘制函数
    def draw(self, context):
        偏好 = context.preferences.addons["导入小二"].preferences

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
        行 = self.layout.row()
        行.prop(偏好, "导入贴图", text="导入贴图", icon='IMPORT')

        # 搜索贴图路径开关
        行 = self.layout.row()
        行.prop(偏好, "搜索贴图文件夹", text="通过模型名称搜索贴图文件夹", icon='VIEWZOOM')
        行.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用

        # # 自动匹配贴图开关
        # 行 = self.layout.row()
        # 左侧 = 行.split(align=True)  # 分割行
        # 左侧.prop(偏好, "匹配基础贴图", text="匹配基础贴图", icon='XRAY')  #1.0.3
        # 左侧.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用
        # 汉明距离
        行 = self.layout.row()
        行.prop(偏好, "汉明距离", text="匹配基础贴图汉明距离", slider=True, icon='XRAY')
        行.enabled = 偏好.导入贴图

        # 通过alpha混合贴图
        行 = self.layout.row()
        行.prop(偏好, "通过alpha混合贴图", text="通过alpha混合贴图", icon='IMAGE_ALPHA')  #1.0.3
        行.enabled = 偏好.导入贴图

        # 导入预设模板
        行 = self.layout.row()
        行.scale_y = 2
        行.operator("import_xiaoer.execute_template", text="加载预设模板", icon='NODE')

        # 导出预设
        行 = self.layout.row()
        行.scale_y = 2
        行.operator("export_test.export_mat_presets", text="导出预设", icon='EXPORT')
