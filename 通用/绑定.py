# coding: utf-8

import bpy

# 绑定头骨
def 绑定(prefs, model):
    if prefs.默认姿态:  # 如果模型是默认姿态
        if model.parent and model.parent.type == 'ARMATURE':  # 选中网格具有父级骨架
            armature = model.parent  # 获取父级骨架对象
            bpy.ops.object.select_all(action='DESELECT')  # 清空选中
            # 切换回对象模式并选中子物体
            bpy.ops.object.mode_set(mode='OBJECT')
            object = bpy.data.objects.get("面部定位")
            object.select_set(True)
            # 选中骨骼父级对象并设置为活动对象
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature
            # 切换到姿态模式
            try:
                bpy.ops.object.mode_set(mode='POSE')
            except RuntimeError:
                print("错误：无法进入姿态模式")
                return
            for bone in armature.pose.bones:
                if bone.name == "頭":
                    bone.bone.select = True  # 选中目标骨骼
                    armature.data.bones.active = bone.bone  # 显式设置活动骨骼
                    # 获取骨骼头部和尾部的世界坐标
                    head_world = armature.matrix_world @ bone.head
                    tail_world = armature.matrix_world @ bone.tail
                    # 将面部定位设置为头骨中点
                    object.location = (head_world + tail_world) / 2
            # 执行父级绑定操作
            bpy.ops.object.parent_set(type='BONE', xmirror=False, keep_transform=True)
            bpy.ops.object.mode_set(mode='OBJECT')  # 切换回对象模式
            bpy.ops.object.select_all(action='DESELECT')  # 清空选中
    else:  # 如果模型不是默认姿态
        for m in model.modifiers:  # 原版代码的绑定方法，可以精准定位，但是通过矩阵变换改变了面部定位的属性
            if m.type == 'ARMATURE':
                if m.object:
                    Pos_object = bpy.data.objects.get("面部定位")
                    Pos_object.parent = m.object
                    Pos_object.parent_type = 'BONE'
                    for bone in m.object.pose.bones:
                        if bone.name == "頭":
                            Pos_object.parent_bone = bone.name
                            Rot = bone.matrix @ m.object.data.bones[bone.name].matrix_local.inverted()
                            Pos_object.matrix_world = m.object.matrix_world @ Rot @ Pos_object.matrix_world