import bpy

class ModelObjectPanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_import_xiaoer_model_object_1'
    bl_label = '小二预设模型'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.小二预设模型.使用插件

    def draw(self, context):
        layout = self.layout
        物体 = context.active_object

        属性 = 物体.小二预设模型

        列 = layout.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        if 物体.type == 'MESH':
            列.prop(属性, '导入完成')
        列.prop(属性, '文件')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')

class TemplateObjectPanel(bpy.types.Panel):
    bl_idname = 'OBJECT_PT_import_xiaoer_model_object_2'
    bl_label = '小二预设模板'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        return context.active_object and (context.active_object.小二预设模板.使用插件 or context.active_object.小二预设模板.加载完成)

    def draw(self, context):
        layout = self.layout
        物体 = context.active_object

        属性 = 物体.小二预设模板

        列 = layout.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        if 物体.type == 'MESH':
            列.prop(属性, '加载完成')
        列.prop(属性, '文件')
        列.prop(属性, '贴图')
        列.prop(属性, '游戏')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')
        if 物体.type == 'MESH':
            列.prop(属性, '显示导入节点组')
        if 属性.显示导入节点组:
            for 群组 in 属性.导入节点组:
                列.prop(群组, '节点组', text='')
        if 属性.完成导入贴图:
            列.prop(属性, '显示导入贴图')
            if 属性.显示导入贴图:
                列.prop(属性, '显示基础贴图')
                if 属性.显示基础贴图:
                    for 图像 in 属性.基础贴图:
                        列.prop(图像, '贴图', text='')
                else:
                    for 图像 in 属性.导入贴图:
                        列.prop(图像, '贴图', text='')