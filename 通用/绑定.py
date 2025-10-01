# coding: utf-8

import bpy

# 绑定头骨
def 手动绑定(self, 模型):
    if 模型.parent and 模型.parent.type == 'ARMATURE':  # 选中网格具有父级骨架
        骨架 = 模型.parent  # 获取父级骨架对象

        if not 骨架:  # 1.0.6调试点
            self.report({'ERROR'}, "未找到模型骨架")

        bpy.ops.object.select_all(action='DESELECT')  # 清空选中
        模型.select_set(True)
        bpy.context.view_layer.objects.active = 模型
        # 切换回对象模式并选中子物体
        bpy.ops.object.mode_set(mode='OBJECT')
        定位 = bpy.data.objects.get("面部定位")

        if not 定位:  # 1.0.6调试点
            self.report({'ERROR'}, "未找到面部定位")

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
            if 骨骼.name == "頭" or "Head" in 骨骼.name:  # 1.1.0FBX骨骼
                定位.小二预设模板.绑定骨骼 = 骨骼.name  # 1.1.0记录定位绑定骨骼名称
                骨骼.bone.select = True  # 选中目标骨骼
                # 1.0.6调试点
                if not 骨骼.bone.select:
                    self.report({'ERROR'}, f"{骨骼.name}选择状态设置失败:")

                骨架.data.bones.active = 骨骼.bone  # 显式设置活动骨骼
                # 1.0.6调试点
                if 骨架.data.bones.active != 骨骼.bone:
                    self.report({'ERROR'}, f"无法设置{骨骼.name}为活动对象")

                # 1.0.6如果骨骼不在当前骨架可见层，临时加入可见层，最后移除
                不在可见层 = None
                try:
                    骨骼可见层 = 骨骼.bone.layers[:]
                    当前可见层 = [i for i, v in enumerate(骨架.data.layers) if v]
                    不在可见层 = not any(骨骼可见层[i] for i in 当前可见层)
                    if 不在可见层:
                        # 切到 OBJECT 模式才能改 bone.layers
                        bpy.ops.object.mode_set(mode='OBJECT')
                        for i in 当前可见层:
                            骨骼.bone.layers[i] = True
                except:
                    pass

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
                    try:
                        骨骼.bone.layers[:] = 骨骼可见层
                    except:
                        pass

                bpy.ops.object.select_all(action='DESELECT')  # 清空选中
                模型.select_set(True)
                bpy.context.view_layer.objects.active = 模型
                return
        # 1.0.6调试点
        self.report({'ERROR'}, "未找到名为'頭'的骨骼")

def 矩阵绑定(self, 模型, 定位):
    # self.report({'INFO'}, f"{定位.name} 1")
    if not 定位.parent:
        # self.report({'INFO'}, f"{定位.name} 2")
        # self.report({'INFO'}, f"{模型.name} {模型.modifiers}")
        # 代码来源：峰峰居士
        for 修改器 in 模型.modifiers:
            # self.report({'INFO'}, f"{修改器.type}")
            if 修改器.type == 'ARMATURE':
                # self.report({'INFO'}, f"{定位.name} 3")
                if 修改器.object:
                    # self.report({'INFO'}, f"{定位.name} 4")
                    骨架 = 修改器.object
                    定位.parent = 骨架
                    定位.parent_type = 'BONE'
                    for 姿态骨骼 in 骨架.pose.bones:
                        if 姿态骨骼.name == "頭" or "Head" in 姿态骨骼.name or (定位.小二预设模板.绑定骨骼 and 姿态骨骼.name == 定位.小二预设模板.绑定骨骼):  # 1.1.0FBX骨骼
                            # self.report({'INFO'}, f"{定位.name} 5")
                            定位.parent_bone = 姿态骨骼.name
                            编辑骨骼 = 骨架.data.bones[姿态骨骼.name]
                            # 可以精准定位，但是此种矩阵变换改变了面部定位的属性
                            # Rot = 姿态骨骼.matrix @ 编辑骨骼.matrix_local.inverted()
                            # 定位.matrix_world = 骨架.matrix_world @ Rot @ 定位.matrix_world

                            # 1.1.0优化矩阵计算方式，不再出现X旋转-90°
                            定位.matrix_parent_inverse = 编辑骨骼.matrix_local.inverted()
                            # 骨骼头尾高度差校正
                            定位.matrix_parent_inverse[1][3] += 姿态骨骼.head.z - 姿态骨骼.tail.z
                            # # 分解编辑骨骼的局部矩阵，只提取旋转部分
                            # 位置, 旋转, 缩放 = 编辑骨骼.matrix_local.decompose()
                            # # 只抵消旋转，不抵消位置
                            # 定位.matrix_parent_inverse = 旋转.to_matrix().to_4x4().inverted()

                            # # 如果没有父级
                            # 定位.matrix_world = 定位.matrix_local
                            # # 如果有父级物体
                            # 定位.matrix_world = 父级.matrix_world @ 定位.matrix_local
                            # # 如果父级是骨骼
                            # 定位.matrix_world = 骨架.matrix_world @ 骨骼.matrix @ 定位.matrix_parent_inverse @ 定位.matrix_local
                            return
                    self.report({'ERROR'}, f"{定位.name}未找到绑定骨骼")
                    break
