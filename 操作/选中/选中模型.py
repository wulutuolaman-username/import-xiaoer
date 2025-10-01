import bpy

# 1.0.4全选模型
class SelectModel(bpy.types.Operator):
    """选中一个需要导入/导出预设或加载模板的模型，如果模型导入预设，需要在物体属性面板取消导入完成状态"""
    bl_idname = "import_xiaoer.select_model"
    bl_label = "选中模型"
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
                        if 模型.小二预设模型.导入完成:
                            self.report({"INFO"}, f'{模型.name}已导入预设，如需选中，在物体属性面板取消导入完成状态')
                            continue
                        模型.select = True
                        # 模型.select_set(True)  # 推荐使用新 API
                        context.view_layer.objects.active = 模型  # ✅ 设置为激活对象
                        self.report({"INFO"}, f'已选中 {模型.name}')
                        return {'FINISHED'}  # ✅ 必须是 set 类型！
        return {'FINISHED'}  # ✅ 必须是 set 类型！