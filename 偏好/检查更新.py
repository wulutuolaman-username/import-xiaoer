import bpy
from ..更新 import AddonUpdaterManager

# 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/preferences.py
class XiaoerAddonCheckUpdate:

    def 更新面板(self, layout):
        updater = AddonUpdaterManager.get_instance()
        row = layout.row()  # 1.1.0新增
        row.label(text="更新功能需要挂加速器。如因其他网络问题更新失败，可以等一段时间再尝试")
        update_col = layout.column(align=False)
        if updater.updated():
            col = update_col.column()
            col.scale_y = 2
            col.alert = True
            col.operator(
                "wm.quit_blender",
                text="重启Blender完成更新",
                icon="ERROR"
            )
            return

        if not updater.candidate_checked():
            col = update_col.column()
            col.scale_y = 2
            col.operator(
                "xiaoer.check_addon_update",
                text="检查插件更新",
                icon='FILE_REFRESH'
            )
        else:
            row = update_col.row(align=True)
            row.scale_y = 2
            col = row.column()
            col.operator(
                "xiaoer.check_addon_update",
                text="检查插件更新",
                icon='FILE_REFRESH'
            )
            col = row.column()
            if updater.update_ready():
                col.enabled = True
                col.operator(
                    "xiaoer.update_addon",
                    text=bpy.app.translations.pgettext_iface("安装最新版本({})").format(updater.latest_version()),
                    icon='TRIA_DOWN_BAR'
                ).branch_name = updater.latest_version()

                # 1.0.2增加版本更新说明
                latest_version = updater.latest_version()
                latest_body = ""
                for candidate in updater._AddonUpdaterManager__update_candidate:
                    if candidate.name == latest_version and candidate.group == 'RELEASE':
                        latest_body = candidate.body
                        break
                box = update_col.box()
                box.label(text="更新说明：", icon='TEXT')
                lines = latest_body.split('\n')
                for line in lines:
                    if line.strip():
                        box.label(text=line)

            else:
                col.enabled = False
                col.operator(
                    "xiaoer.update_addon",
                    text="没有更新可用"
                )

            # 1.0.7查看更新历史  # 1.1.0修改缩进
            col = row.column()
            col.operator("xiaoer.update_history", text="查看更新历史", icon="TIME")

            update_col.separator()
            if updater.has_error():
                box = update_col.box()
                box.label(text=updater.error(), icon='CANCEL')
            elif updater.has_info():
                box = update_col.box()
                box.label(text=updater.info(), icon='ERROR')