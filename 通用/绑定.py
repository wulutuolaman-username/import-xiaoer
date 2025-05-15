# coding: utf-8

import bpy

# 绑定头骨
def 绑定(偏好, 模型):
    if 偏好.默认姿态:  # 如果模型是默认姿态
        if 模型.parent and 模型.parent.type == 'ARMATURE':  # 选中网格具有父级骨架
            骨架 = 模型.parent  # 获取父级骨架对象
            bpy.ops.object.select_all(action='DESELECT')  # 清空选中
            # 切换回对象模式并选中子物体
            bpy.ops.object.mode_set(mode='OBJECT')
            定位 = bpy.data.objects.get("面部定位")
            # 1.0.5确保对象在场景集合中
            if 定位.name not in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.link(定位)  # 手动加入场景
            if 模型.users_collection:  # 检查选中模型是否在集合中
                for 集合 in 定位.users_collection:
                    集合.objects.unlink(定位)
                模型.users_collection[0].objects.link(定位)  # 将面部定位移入模型集合
            定位.select_set(True)
            # 选中骨骼父级对象并设置为活动对象
            骨架.select_set(True)
            bpy.context.view_layer.objects.active = 骨架
            # 切换到姿态模式
            try:
                bpy.ops.object.mode_set(mode='POSE')
            except RuntimeError:
                print("错误：无法进入姿态模式")
                return
            for 骨骼 in 骨架.pose.bones:
                if 骨骼.name == "頭":
                    骨骼.bone.select = True  # 选中目标骨骼
                    骨架.data.bones.active = 骨骼.bone  # 显式设置活动骨骼
                    # 获取骨骼头部和尾部的世界坐标
                    头 = 骨架.matrix_world @ 骨骼.head
                    尾 = 骨架.matrix_world @ 骨骼.tail
                    # 将面部定位设置为头骨中点
                    定位.location = (头 + 尾) / 2
            # 执行父级绑定操作
            bpy.ops.object.parent_set(type='BONE', xmirror=False, keep_transform=True)
            bpy.ops.object.mode_set(mode='OBJECT')  # 切换回对象模式
            bpy.ops.object.select_all(action='DESELECT')  # 清空选中
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