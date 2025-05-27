import bpy

MMD_TOOLS_INSTALLED = False
try:
    from mmd_tools.core import model  # 延迟导入，避免未安装时报错
    MMD_TOOLS_INSTALLED = True
except ImportError:
    MMD_TOOLS_INSTALLED = False
class MMDtoolsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "mmd_tools"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import2"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    @classmethod  # 1.0.7检查是否安装mmd_tools
    def poll(cls, context):
        return MMD_TOOLS_INSTALLED

    # 定义一个绘制函数
    def draw(self, context):
        if MMD_TOOLS_INSTALLED:
            # 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/panels/sidebar.py
            def check_operator_exists(op_id):
                try:
                    # 分割操作符ID为模块和操作符名（例如："mmd_tools.import_model"）
                    module_name, operator_name = op_id.split('.', 1)
                    # 检查 bpy.ops 模块中是否存在对应的操作符
                    op_module = getattr(bpy.ops, module_name)
                    getattr(op_module, operator_name)
                    return True
                except (AttributeError, ValueError):
                    return False

            exist = check_operator_exists('mmd_tools.import_model')
            if exist:  # 如果存在mmd_tools操作符
                行 = self.layout.row()
                col = 行.column(align=True)
                col.operator('mmd_tools.import_model', text="导入模型", icon='OUTLINER_OB_ARMATURE')
                col = 行.column(align=True)
                col.operator('mmd_tools.import_vmd', text='导入动作', icon='ANIM')
                col = 行.column(align=True)
                col.operator('mmd_tools.import_vpd', text='导入姿态', icon='POSE_HLT')
            if context.object:
                行 = self.layout.row()
                col = 行.column(align=True)
                active_object: bpy.types.Object = context.active_object
                mmd_root_object = model.Model.findRoot(active_object)
                if mmd_root_object:
                    mmd_root = mmd_root_object.mmd_root
                    if not mmd_root.is_built:
                        col.operator('mmd_tools.build_rig', text='物理', icon='PHYSICS', depress=False)
                    else:
                        col.operator('mmd_tools.clean_rig', text='物理', icon='PHYSICS', depress=True)
                    col = 行.column(align=True)
                    rigidbody_world = context.scene.rigidbody_world
                    if rigidbody_world:
                        point_cache = rigidbody_world.point_cache
                        if point_cache.is_baked is True:
                            col.operator("mmd_tools.ptcache_rigid_body_delete_bake", text="删除烘培", icon='TRASH')
                        else:
                            col.operator("mmd_tools.ptcache_rigid_body_bake", text="烘培", icon='MEMORY')
