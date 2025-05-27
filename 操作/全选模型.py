import bpy

# 1.0.4全选模型
class SelectAllMeshes(bpy.types.Operator):
    """全选模型"""
    bl_idname = "import_xiaoer.select_all_meshes"
    bl_label = "全选模型"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return context.mode == 'OBJECT'  # 必须是物体模式
    def execute(self, context):
        # 取消所有选择
        bpy.ops.object.select_all(action='DESELECT')
        # 遍历所有对象，找到骨架及其子网格模型
        for 骨架 in bpy.data.objects:
            if 骨架.type == 'ARMATURE':
                for 模型 in 骨架.children:
                    if 模型.type == 'MESH':
                        模型.select = True
                        # 模型.select_set(True)  # 推荐使用新 API
                        context.view_layer.objects.active = 模型  # ✅ 设置为激活对象
        for 物 in bpy.context.selected_objects:
            self.report({"INFO"}, f'{物.name}')
        return {'FINISHED'}  # ✅ 必须是 set 类型！