import bpy

# 打开偏好设置
class OPEN_PREFERENCES_OT_open_addon_prefs(bpy.types.Operator):
    """打开插件偏好设置"""
    bl_idname = "import_xiaoer.open_addon_prefs"
    bl_label = "打开偏好"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 打开用户偏好设置窗口
        bpy.ops.screen.userpref_show()
        # 切换到Add-ons选项卡
        context.preferences.active_section = 'ADDONS'
        # 获取当前插件的显示名称
        小二插件 = context.preferences.addons.get("导入小二")
        if 小二插件:
            addon_name = "导入小二"
            context.window_manager.addon_search = addon_name  # 设置搜索过滤
        else:
            self.report({'ERROR'}, f'"{小二插件}"插件未找到，请确保已启用。')
        return {'FINISHED'}