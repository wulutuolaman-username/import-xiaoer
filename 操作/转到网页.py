import bpy
import webbrowser

class OpenWebsite(bpy.types.Operator):
    bl_idname = "xiaoer.open_website"
    bl_label = "打开网站"
    bl_description = "点击跳转到指定网站"

    url: bpy.props.StringProperty(name="URL", default="")  # 接收 URL 参数

    def execute(self, context):
        if self.url:
            webbrowser.open(self.url)  # 使用 webbrowser 打开链接
            self.report({'INFO'}, f"已打开: {self.url}")
        else:
            self.report({'ERROR'}, "未提供 URL")
        return {'FINISHED'}

# 1.0.7查看更新历史
class UpdateHistory(OpenWebsite):
    bl_idname = "xiaoer.update_history"
    bl_label = "查看更新历史"
    bl_description = "各版本Releases插件包附有更新说明"
    url: bpy.props.StringProperty(default="https://github.com/wulutuolaman-username/import-xiaoer/releases")

class XiaoerBilibiliOpenWebsite(OpenWebsite):
    bl_idname = "xiaoer.open_website_bilibili"
    bl_label = " 小二新教程啥时候更新捏"
    bl_description = "点击前往小二主页催更"
    url: bpy.props.StringProperty(default="https://space.bilibili.com/437528440?spm_id_from=333.337.0.0")
class XiaoerAfdianOpenWebsite(OpenWebsite):
    bl_idname = "xiaoer.open_website_afdian"
    bl_label = ""
    bl_description = "点击前往小二爱发电主页获取预设"
    url: bpy.props.StringProperty(default="https://afdian.com/a/xiaoer?tab=feed")
class XiaoerAplayboxOpenWebsite(OpenWebsite):
    bl_idname = "xiaoer.open_website_aplaybox"
    bl_label = ""
    bl_description = "点击前往小二模之屋主页获取预设"
    url: bpy.props.StringProperty(default="https://www.aplaybox.com/u/872092888")