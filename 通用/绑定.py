# coding: utf-8

import bpy

# 绑定头骨
def 绑定(偏好, 模型, self):
    if 偏好.默认姿态:  # 如果模型是默认姿态
        if 模型.parent and 模型.parent.type == 'ARMATURE':  # 选中网格具有父级骨架
            骨架 = 模型.parent  # 获取父级骨架对象

            if not 骨架:  # 1.0.6调试点
                self.report({'ERROR'}, "未找到模型骨架")

            bpy.ops.object.select_all(action='DESELECT')  # 清空选中
            # 切换回对象模式并选中子物体
            bpy.ops.object.mode_set(mode='OBJECT')
            定位 = bpy.data.objects.get("面部定位")

            if not 定位:  # 1.0.6调试点
                self.report({'ERROR'}, "未找到面部定位定位")

            定位.select_set(True)
            # 选中骨骼父级对象并设置为活动对象
            骨架.select_set(True)
            bpy.context.view_layer.objects.active = 骨架

            # 1.0.6调试点
            if bpy.context.view_layer.objects.active != 骨架:
                self.report({'ERROR'}, f"无法设置{骨架.name}为活动对象")

            # 切换到姿态模式
            try:
                bpy.ops.object.mode_set(mode='POSE')
            except RuntimeError:
                print("错误：无法进入姿态模式")
                return

            for 骨骼 in 骨架.pose.bones:
                if 骨骼.name == "頭":

                    骨骼.bone.select = True  # 选中目标骨骼
                    # 1.0.6调试点
                    if not 骨骼.bone.select:
                        self.report({'ERROR'}, f"{骨骼.name}选择状态设置失败:")

                    骨架.data.bones.active = 骨骼.bone  # 显式设置活动骨骼
                    # 1.0.6调试点
                    if 骨架.data.bones.active != 骨骼.bone:
                        self.report({'ERROR'}, f"无法设置{骨骼.name}为活动对象")

                    # 1.0.6如果骨骼不在当前骨架可见层，临时加入可见层，最后移除
                    骨骼可见层 = 骨骼.bone.layers[:]
                    当前可见层 = [i for i, v in enumerate(骨架.data.layers) if v]
                    不在可见层 = not any(骨骼可见层[i] for i in 当前可见层)
                    if 不在可见层:
                        # 切到 OBJECT 模式才能改 bone.layers
                        bpy.ops.object.mode_set(mode='OBJECT')
                        for i in 当前可见层:
                            骨骼.bone.layers[i] = True

                    # 获取骨骼头部和尾部的世界坐标
                    头 = 骨架.matrix_world @ 骨骼.head
                    尾 = 骨架.matrix_world @ 骨骼.tail
                    # 将面部定位设置为头骨中点
                    定位.location = (头 + 尾) / 2

                    # 执行父级绑定操作
                    bpy.ops.object.parent_set(type='BONE', xmirror=False, keep_transform=True)
                    bpy.ops.object.mode_set(mode='OBJECT')  # 切换回对象模式

                    # 1.0.6移出可见层
                    if 不在可见层:
                        骨骼.bone.layers[:] = 骨骼可见层

                    bpy.ops.object.select_all(action='DESELECT')  # 清空选中

                    return
            # 1.0.6调试点
            self.report({'ERROR'}, "未找到名为'頭'的骨骼")

    else:  # 如果模型不是默认姿态  # 代码来源：峰峰居士
        for m in 模型.modifiers:  # 原版代码的绑定方法，可以精准定位，但是通过矩阵变换改变了面部定位的属性
            if m.type == 'ARMATURE':
                if m.object:
                    Pos_object = bpy.data.objects.get("面部定位")
                    Pos_object.parent = m.object
                    Pos_object.parent_type = 'BONE'
                    for 骨骼 in m.object.pose.bones:
                        if 骨骼.name == "頭":
                            Pos_object.parent_bone = 骨骼.name
                            Rot = 骨骼.matrix @ m.object.data.bones[骨骼.name].matrix_local.inverted()
                            Pos_object.matrix_world = m.object.matrix_world @ Rot @ Pos_object.matrix_world