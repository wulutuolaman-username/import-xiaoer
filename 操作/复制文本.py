import bpy

# 定义一个操作符（点击按钮时调用）
class XiaoerAddon_OT_copy_to_clipboard(bpy.types.Operator):
    bl_idname = "import_xiaoer.copy_to_clipboard"
    bl_label = "复制借物表"

    def execute(self, context):
        借物表 = "渲染：小二今天吃啥啊\n插件：五路拖拉慢"
        context.window_manager.clipboard = 借物表
        self.report({'INFO'}, f"已复制 {借物表.replace(chr(10), ' ')}")
        return {'FINISHED'}