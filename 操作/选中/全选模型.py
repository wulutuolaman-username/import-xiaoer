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
        # 取消活动对象（激活对象）
        bpy.context.view_layer.objects.active = None
        # 遍历所有对象，找到骨架及其子网格模型
        for 骨架 in bpy.data.objects:
            if 骨架.type == 'ARMATURE':
                for 模型 in 骨架.children:
                    if 模型.type == 'MESH' and 模型.data.shape_keys: #1.1.0增加形态键判断
                        # 1.1.1检查Blender版本是否小于4.0
                        if bpy.app.version[0] < 4:
                            模型.select = True
                        else:
                            模型.select_set(True)
                        context.view_layer.objects.active = 模型  # ✅ 设置为激活对象
                        self.report({"INFO"}, f'已选中 {模型.name}')
                    elif 模型.type != 'MESH':
                        self.report({"WARNING"}, f'{模型.name}非网格类型')
                    elif not 模型.data.shape_keys:
                        self.report({"WARNING"}, f'{模型.name}无形态键，可能不是角色模型')
        # for 物 in bpy.context.selected_objects:
        #     self.report({"INFO"}, f'已选中 {物.name}')
        return {'FINISHED'}  # ✅ 必须是 set 类型！