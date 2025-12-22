# coding: utf-8

import bpy
from ..指针 import XiaoerObject

# 绑定头骨
def 矩阵绑定(self:bpy.types.Operator, 模型, 定位:XiaoerObject):
    if not 定位.parent:
        # 代码来源：峰峰居士
        for 修改器 in 模型.modifiers:
            if 修改器.type == 'ARMATURE':
                骨架 = 修改器.object
                if 骨架:
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
                            return
                    self.report({'ERROR'}, f"{定位.name}未找到绑定骨骼")
                    break