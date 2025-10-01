import bpy

class MaterialNodeTreePanel(bpy.types.Panel):
    bl_idname = 'NODE_PT_import_xiaoer_material_nodetree_1'
    bl_label = '小二预设材质'
    bl_space_type = 'NODE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = '材质'        # 侧边栏分类标签

    @classmethod
    def poll(cls, context):
        节点树 = context.space_data.edit_tree
        # if 节点树:
        #     for 节点组 in bpy.data.node_groups:
        #         if 节点组.name == 节点树.name:
        #             return False
        #     return 节点树.小二预设节点树.使用插件
        # return False
        return 节点树 and 节点树.小二预设节点树.使用插件 and not 节点树.name in bpy.data.node_groups

    def draw(self, context):
        layout = self.layout
        节点树 = context.space_data.edit_tree

        属性 = 节点树.小二预设节点树

        列 = layout.column()
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        列.prop(属性, '文件')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')

class TemplateMaterialNodeTreePanel(bpy.types.Panel):
    bl_idname = 'NODE_PT_import_xiaoer_material_nodetree_2'
    bl_label = '小二预设模板'
    bl_space_type = 'NODE_EDITOR'  # 图像编辑器
    bl_region_type = 'UI'          # 侧边栏 (N面板)
    bl_category = '材质'        # 侧边栏分类标签

    @classmethod
    def poll(cls, context):
        节点树 = context.space_data.edit_tree
        # if 节点树:
        #     for 节点组 in bpy.data.node_groups:
        #         if 节点组.name == 节点树.name:
        #             return False
        #     return 节点树.小二预设节点树.使用插件
        # return False
        return 节点树 and 节点树.小二预设模板.使用插件 and not 节点树.name in bpy.data.node_groups

    def draw(self, context):
        layout = self.layout
        材质 = context.material

        属性 = 材质.小二预设模板

        列 = layout.column()
        列.enabled = not context.active_object.小二预设模板.加载完成
        列.prop(属性, '渲染作者')
        列.prop(属性, '插件作者')
        if context.active_object.小二预设模板.加载完成:
            列.label(text="在模型的物体属性模板",icon='OBJECT_DATA')
            列.label(text="取消加载完成状态",icon='CHECKBOX_HLT')
            列.label(text="可修改材质分类、透明状态",icon='MATERIAL')
            列.label(text="第一次加载时，模板文件必须包含全部节点组",icon='ERROR')
            列.label(text="如果导入贴图，第一次加载时，贴图路径必须包含全部贴图", icon='ERROR')
            列.label(text="不要修改贴图、节点和节点组名称",icon='ERROR')
        if 属性.材质分类 != 属性.初始分类+'材质':
            列.prop(属性, '代码分类')
        列.prop(属性, '材质分类')
        if 属性.使用检测透明材质:
            列.prop(属性, '检测为透明材质')
        列.prop(属性, '透明材质')
        列.prop(属性, '文件')
        列.prop(属性, '贴图')
        列.prop(属性, '游戏')
        列.prop(属性, '角色')
        列.prop(属性, '时间')
        列.prop(属性, '版本')