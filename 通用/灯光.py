import bpy, traceback

灯光名称 = "小二预设灯光控制"

# 1.1.0控制灯光
def 灯光驱动(self, 灯光):
    if not 灯光.parent:
        # 灯光控制 = bpy.context.scene.collection.objects.get("小二预设灯光控制")
        灯光控制 = bpy.data.objects.get(灯光名称)
        if 灯光控制:
            灯光.parent = 灯光控制
        else:
            灯光控制 = bpy.data.objects.new(灯光名称, None)
            bpy.context.scene.collection.objects.link(灯光控制)
            灯光.parent = 灯光控制
            灯光控制.use_fake_user = True
            # 设置该对象为活动对象并选中
            bpy.ops.object.select_all(action='DESELECT')
            灯光控制.select_set(True)
            bpy.context.view_layer.objects.active = 灯光控制
            # 逐个将该对象从集合中移除（通过 operator）
            for 集合 in 灯光控制.users_collection[:]:
                try:
                    灯光控制.use_fake_user = True
                    集合.objects.unlink(灯光控制)
                except Exception as e:
                    错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                    self.report({"ERROR"}, f"灯光移除集合失败\n{错误信息}")