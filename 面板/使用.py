import bpy

class ImportMatPresetsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "使用预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import3"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    # 定义一个绘制函数
    def draw(self, context):

        偏好 = context.preferences.addons["导入小二"].preferences

        # 导入按钮
        行 = self.layout.row()
        行.scale_y = 2
        if 偏好.自动查找预设:  # 自动导入
            行.operator("import_test.import_mat_presets", text="炒飞小二", icon='IMPORT')
        else:  #手动导入
            行.operator("import_test.import_mat_presets_filebrowser", text="手动导入", icon='IMPORT')

        # 自动查找开关
        行 = self.layout.row()
        行.prop(偏好, "自动查找预设", text="自动查找预设", icon='VIEWZOOM')

        # 默认姿态开关
        行 = self.layout.row()
        行.prop(偏好, "默认姿态", text="默认姿态",icon='OUTLINER_DATA_ARMATURE')

        # 连续导入开关
        行 = self.layout.row(align=True)
        列 = 行.column()
        列.operator("import_xiaoer.select_all_meshes", text="全选模型", icon='SELECT_EXTEND')
        列 = 行.column()
        列.prop(偏好, "重命名资产", text="重命名资产",icon='ASSET_MANAGER')

        if not 偏好.开启制作预设:  # 1.0.3新增
            行 = self.layout.row()
            行.operator("import_xiaoer.open_addon_prefs", text="打开偏好设置", icon='PREFERENCES')
            # 导出预设
            行 = self.layout.row()
            行.scale_y = 2
            行.operator("export_test.export_mat_presets", text="导出预设", icon='EXPORT')
