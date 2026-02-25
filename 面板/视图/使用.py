import os, bpy  # noqa: F401
from ...偏好.获取偏好 import 获取偏好
from ...通用.灯光 import 灯光名称
from ...指针 import *

class ImportMatPresetsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "使用预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_4"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    # 定义一个绘制函数
    def draw(self, context):
        偏好 = 获取偏好()
        布局 = self.layout

        if bpy.app.version[:2] >= (4, 4):
            try:
                if bpy.app.version[:2] < (5, 0):
                    节点树 = bpy.context.scene.node_tree
                else:
                    节点树 = bpy.context.scene.compositing_node_group  # type:ignore
                if 节点树:
                    for 节点 in 节点树.nodes:  # type:小二节点
                        if 节点.判断类型.节点.合成.是辉光:
                            行 = 布局.row(align=True)
                            行.prop(节点.inputs['Strength'], 'default_value', text='辉光强度')
                            break
            except:
                pass

        # 自动查找开关
        行 = 布局.row(align=True)
        左侧 = 行.column()  # 分割行
        左侧.ui_units_x = 13  # 设置固定宽度单位
        左侧.prop(偏好, "自动查找预设", text="自动查找预设", icon='VIEWZOOM')
        右侧 = 行.column()  # 右侧子行
        右侧.enabled = 偏好.自动查找预设
        右侧.prop(偏好, "查找预设深度检索", text="深度检索", icon='SCRIPTPLUGINS')
        if 偏好.自动查找预设:
            行 = 布局.row()
            if 偏好.预设目录 and os.path.exists(偏好.预设目录):
                行.label(text=f"预设目录：{偏好.预设目录}", icon='VIEWZOOM')
                # 深度检测icon='SCRIPTPLUGINS'
            elif not 偏好.预设目录:
                行.alert = True
                行.label(text=f"偏好未设置预设目录", icon='ERROR')
            elif not os.path.exists(偏好.预设目录):  # 1.1.1 elif
                行.alert = True
                行.label(text=f"无效路径{偏好.预设目录}", icon='ERROR')

        框 = 布局.box()
        行 = 框.row()
        行.alert = True
        行.scale_y = 1.5
        行.operator("import_xiaoer.copy_to_clipboard", text="点击复制借物表", icon='COPYDOWN')
        行 = 框.row()
        行.label(text="渲染：小二今天吃啥啊", icon='SHADERFX')
        行 = 框.row()
        行.label(text="插件：五路拖拉慢", icon='SCRIPT')

        # 连续导入开关
        行 = 布局.row(align=True)
        行.scale_y = 2
        列 = 行.column()
        if 偏好.自动查找预设:
            列.operator("import_xiaoer.select_all_meshes", text="全选模型", icon='SELECT_EXTEND')
        else:
            列.operator("import_xiaoer.select_model", text="选中模型", icon='RESTRICT_SELECT_OFF')

        # 导入按钮
        行 = 布局.row()
        行.scale_y = 2
        if 偏好.自动查找预设:  # 自动导入
            行.operator("import_xiaoer.import_presets_auto", text="炒飞小二", icon='IMPORT')
        else:  #手动导入
            行.operator("import_xiaoer.import_presets_hand", text="手动导入", icon='IMPORT')

        # 1.1.0灯光方向
        灯光控制 = bpy.data.objects.get(灯光名称)
        if 灯光控制:
            行 = 布局.row(align=True)
            列 = 行.column()
            列.label(icon='OUTLINER_OB_LIGHT')
            列 = 行.column()
            列.prop(灯光控制, "delta_rotation_euler", index=2, text="灯光方向")

        # 1.2.0描边开关
        骨架 = None
        模型 = context.object  # type:小二物体|bpy.types.Object
        if 模型 and 模型.判断类型.物体.是网格 and 模型.modifiers:
            for 修改器 in 模型.modifiers:  # type:小二对象|bpy.types.Modifier
                if 修改器.判断类型.修改器.是几何节点修改器:
                    节点组 = 修改器.node_group  # type:ignore
                    if 节点组 and 节点组.name.startswith("Geometry Nodes"):
                        for 节点 in 节点组.nodes:  # type:小二节点
                            if 节点.判断类型.节点.是群组:
                                if 节点.node_tree and 节点.node_tree.name.startswith("实体化描边"):
                                    骨架 = 模型.parent  # type:小二物体|None
                                    if 骨架.判断类型.物体.是骨架:
                                        行 = 布局.row(align=True)
                                        行.prop(骨架.小二预设模型, "描边开关", icon='MOD_SOLIDIFY')
                                        break
                if 骨架:
                    break

        if not 偏好.开启制作预设:  # 1.0.3新增
            行 = 布局.row()
            行.operator("import_xiaoer.open_addon_prefs", text="打开偏好设置", icon='PREFERENCES')
            # 导出预设
            行 = 布局.row()
            行.scale_y = 2
            行.operator("import_xiaoer.export_mat_presets", text="导出预设", icon='EXPORT')
