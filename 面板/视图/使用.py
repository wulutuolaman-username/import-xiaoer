import os, bpy
from ...偏好.获取偏好 import 获取偏好

class ImportMatPresetsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "使用预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_4"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    # 定义一个绘制函数
    def draw(self, context):

        偏好 = 获取偏好()

        行 = self.layout.row(align=True)
        # 行.label(text="记得写借物表！", icon='ERROR')
        行.operator("import_xiaoer.copy_to_clipboard", text="点击复制借物表", icon='COPYDOWN')
        行 = self.layout.row()
        行.label(text="渲染：小二今天吃啥啊", icon='SHADERFX')
        行 = self.layout.row()
        行.label(text="插件：五路拖拉慢", icon='SCRIPT')

        # 自动查找开关
        行 = self.layout.row(align=True)
        左侧 = 行.column()  # 分割行
        左侧.ui_units_x = 13  # 设置固定宽度单位
        左侧.prop(偏好, "自动查找预设", text="自动查找预设", icon='VIEWZOOM')
        右侧 = 行.column()  # 右侧子行
        右侧.enabled = 偏好.自动查找预设
        右侧.prop(偏好, "查找预设深度检索", text="深度检索", icon='SCRIPTPLUGINS')
        if 偏好.自动查找预设:
            行 = self.layout.row()
            if 偏好.预设目录 and os.path.exists(偏好.预设目录):
                行.label(text=f"预设目录：{偏好.预设目录}", icon='VIEWZOOM')
                # 深度检测icon='SCRIPTPLUGINS'
            elif not 偏好.预设目录:
                行.label(text=f"偏好未设置预设目录", icon='ERROR')
            elif not os.path.exists(偏好.预设目录):  # 1.1.1 elif
                行.label(text=f"无效路径{偏好.预设目录}", icon='ERROR')

        # # 默认姿态开关
        # 行 = self.layout.row()
        # 行.prop(偏好, "默认姿态", text="默认姿态",icon='OUTLINER_DATA_ARMATURE')

        # 连续导入开关
        行 = self.layout.row(align=True)
        行.scale_y = 2
        列 = 行.column()
        if 偏好.自动查找预设:
            列.operator("import_xiaoer.select_all_meshes", text="全选模型", icon='SELECT_EXTEND')
        else:
            列.operator("import_xiaoer.select_model", text="选中模型", icon='RESTRICT_SELECT_OFF')
        # 列 = 行.column()
        # 列.prop(偏好, "重命名资产", text="重命名资产",icon='ASSET_MANAGER')

        # 导入按钮
        行 = self.layout.row()
        行.scale_y = 2
        if 偏好.自动查找预设:  # 自动导入
            行.operator("import_xiaoer.import_presets_auto", text="炒飞小二", icon='IMPORT')
        else:  #手动导入
            行.operator("import_xiaoer.import_presets_hand", text="手动导入", icon='IMPORT')

        # 1.1.0灯光方向
        灯光控制 = bpy.data.objects.get("小二预设灯光控制")
        if 灯光控制:
            行 = self.layout.row(align=True)
            列 = 行.column()
            列.label(icon='OUTLINER_OB_LIGHT')
            列 = 行.column()
            列.prop(灯光控制, "delta_rotation_euler", index=2, text="灯光方向")

        if not 偏好.开启制作预设:  # 1.0.3新增
            行 = self.layout.row()
            行.operator("import_xiaoer.open_addon_prefs", text="打开偏好设置", icon='PREFERENCES')
            # 导出预设
            行 = self.layout.row()
            行.scale_y = 2
            行.operator("import_xiaoer.export_mat_presets", text="导出预设", icon='EXPORT')
