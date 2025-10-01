import bpy

class ImagePanel(bpy.types.Panel):
    bl_idname = 'IMAGE_PT_import_xiaoer_image_1'
    bl_label = '小二预设贴图'
    bl_space_type = 'IMAGE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = 'Image'        # 侧边栏分类标签

    @classmethod
    def poll(cls, context):
        return context.space_data.image and context.space_data.image.小二预设贴图.使用插件

    def draw(self, context):
        layout = self.layout
        贴图 = context.space_data.image

        属性 = 贴图.小二预设贴图

        列 = layout.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        列.prop(属性, '文件')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')

class TemplateImagePanel(bpy.types.Panel):
    bl_idname = 'IMAGE_PT_import_xiaoer_image_2'
    bl_label = '小二预设模板'
    bl_space_type = 'IMAGE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = 'Image'        # 侧边栏分类标签

    @classmethod
    def poll(cls, context):
        return context.space_data.image and context.space_data.image.小二预设模板.使用插件

    def draw(self, context):
        layout = self.layout
        贴图 = context.space_data.image

        属性 = 贴图.小二预设模板

        列 = layout.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        if 属性.类型:
            列.prop(属性, '前缀')
            列.prop(属性, '部件')
            列.prop(属性, '类型')
        列.prop(属性, '文件')
        列.prop(属性, '贴图')
        列.prop(属性, '游戏')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')
        if 属性.匹配节点组:
            列.prop(属性, '匹配节点组')