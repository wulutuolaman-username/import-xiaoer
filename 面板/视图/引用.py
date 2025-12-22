import os, bpy

class MMDtoolsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "mmd_tools"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_3_1"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    # 定义一个绘制函数
    def draw(self, context):
        布局 = self.layout
        行 = 布局.row()
        行.label(text=f"Blender " + ".".join(map(str, bpy.app.version)))
        行 = 布局.row()
        try:
            if bpy.app.version[:2] < (4, 2):  # 4.2及以上版本mmd_tools安装在extension路径下
                from mmd_tools import bl_info
                行.label(text=f"mmd_tools " + ".".join(map(str, bl_info["version"])))
            else:
                for 扩展id in ["bl_ext.user_default.mmd_tools", "bl_ext.blender_org.mmd_tools"]:  # 1.1.2 bl_ext.blender_org.mmd_tools
                    if 扩展id in bpy.context.preferences.addons:
                        import sys, importlib, tomllib
                        插件id = bpy.context.preferences.addons[扩展id].module
                        模块 = importlib.import_module(插件id)
                        sys.modules["mmd_tools"] = 模块
                        插件路径 = os.path.dirname(模块.__file__)
                        清单路径 = os.path.join(插件路径, "blender_manifest.toml")
                        if os.path.exists(清单路径):
                            with open(清单路径, "rb") as f:
                                清单 = tomllib.load(f)
                            行.label(text=f"mmd_tools {清单.get('version')}")
            # 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/panels/sidebar.py
            from mmd_tools.core import model  # 延迟导入，避免未安装时报错
            if 存在操作符('mmd_tools.import_model'):  # 如果存在mmd_tools操作符
                行 = 布局.row()
                col = 行.column(align=True)
                col.operator('mmd_tools.import_model', text="导入模型", icon='OUTLINER_OB_ARMATURE')
                col = 行.column(align=True)
                col.operator('mmd_tools.import_vmd', text='导入动作', icon='ANIM')
                col = 行.column(align=True)
                col.operator('mmd_tools.import_vpd', text='导入姿态', icon='POSE_HLT')
                if context.object:
                    行 = 布局.row()
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
            else:
                行.label(text=f"未启用mmd_tools")
        except ImportError:
            行.label(text=f"未安装mmd_tools")

class BetterFBXUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "Better_FBX"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import_xiaoer_3_2"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        布局 = self.layout
        行 = 布局.row()
        try:
            from better_fbx import bl_info
            行.label(text=f"better_fbx " + ".".join(map(str, bl_info["version"])))
            行 = 布局.row()
            if 存在操作符('better_import.fbx'):
                行.operator('better_import.fbx', text="better_fbx导入FBX模型", icon='OUTLINER_OB_ARMATURE')
            else:
                行.label(text=f"未启用better_fbx")
            行 = 布局.row()
            行.operator('import_scene.fbx', text="blender导入FBX模型", icon='OUTLINER_OB_ARMATURE')
        except ImportError:
            行.label(text=f"未安装better_fbx")

def 存在操作符(op_id):
    try:
        # 分割操作符ID为模块和操作符名（例如："mmd_tools.import_model"）
        模块名, 操作名 = op_id.split('.', 1)
        # 检查 bpy.ops 模块中是否存在对应的操作符
        操作模块 = getattr(bpy.ops, 模块名)
        getattr(操作模块, 操作名)
        return True
    except (AttributeError, ValueError):
        return False