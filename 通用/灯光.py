import bpy, traceback

# 1.1.0控制灯光
def 灯光驱动(self, 灯光):
    if not 灯光.parent:
        # 灯光控制 = bpy.context.scene.collection.objects.get("小二预设灯光控制")
        灯光控制 = bpy.data.objects.get("小二预设灯光控制")
        if 灯光控制:
            灯光.parent = 灯光控制
        else:
            bpy.data.objects.new("小二预设灯光控制", None)
            灯光控制 = bpy.data.objects["小二预设灯光控制"]
            bpy.context.scene.collection.objects.link(灯光控制)
            灯光.parent = 灯光控制
            灯光控制.use_fake_user = True
            # 设置该对象为活动对象并选中
            bpy.ops.object.select_all(action='DESELECT')
            灯光控制.select_set(True)
            bpy.context.view_layer.objects.active = 灯光控制
            # 逐个将该对象从集合中移除（通过 operator）
            for 集合 in 灯光控制.users_collection[:]:
                # 将集合设为当前活动集合（context.collection）
                # override = {
                #     "object": 灯光控制,
                #     "selected_objects": [灯光控制],
                #     "selected_editable_objects": [灯光控制],
                #     "active_object": 灯光控制,
                #     "collection": 集合,
                #     "view_layer": bpy.context.view_layer,
                #     "scene": bpy.context.scene,
                #     "window": bpy.context.window,
                #     "area": next(area for area in bpy.context.screen.areas if area.type == 'OUTLINER'),
                #     "region": next(region for region in bpy.context.screen.areas[0].regions if region.type == 'WINDOW'),
                # }
                try:
                    # bpy.ops.outliner.id_operation(override, type='ADD_FAKE')
                    灯光控制.use_fake_user = True
                    # bpy.ops.object.collection_remove(override)
                    集合.objects.unlink(灯光控制)
                except Exception as e:
                    错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                    self.report({"ERROR"}, f"{错误信息}")