import bpy,webbrowser

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

class WulutuolamanTiktokOpenWebsite(OpenWebsite):
    bl_idname = "wulutuolaman.open_website_tiktok"
    bl_label = ""
    bl_description = "点击前往插件作者抖音主页反馈插件问题"
    url: bpy.props.StringProperty(default="https://www.douyin.com/user/MS4wLjABAAAAFquoHuLepdMMZ42a9DF96CSYclTKxd3zFkQrP9yl8GSZU6LOxrhanY-pLE_ESDqN?from_tab_name=main&vid=7522913200401075482")
class WulutuolamanBilibiliOpenWebsite(OpenWebsite):
    bl_idname = "wulutuolaman.open_website_bilibili"
    bl_label = ""
    bl_description = "点击前往插件作者B站主页反馈插件问题"
    url: bpy.props.StringProperty(default="https://space.bilibili.com/230130803?spm_id_from=333.1007.0.0")

class TemplateExampleOpenWebsite(OpenWebsite):
    bl_idname = "wulutuolaman.open_website_template_example"
    bl_label = ""
    bl_description = "查看预设模板示范，可参考设置"
    url: bpy.props.StringProperty(default="https://www.douyin.com/user/self?modal_id=7526943600450620682")
