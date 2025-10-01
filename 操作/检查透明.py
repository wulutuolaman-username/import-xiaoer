import os
import bpy
import numpy as np
from collections import defaultdict
from ..材质.检测透明.检测透明 import 通过UV和像素检测透明材质
from ..材质.检测透明.材质面 import 获取材质面
from ..材质.检测透明.判断透明 import 判断透明
from ..着色.贴图.基础贴图 import 筛选贴图
from ..着色.贴图.空白贴图 import 获取空白贴图
from ..图像.像素处理 import 检查透明

global Image  #  1.0.1更新：不再直接导入PIL
try:
    from PIL import Image
except ImportError:
    pass

class XiaoerAddonCheckTransparent(bpy.types.Operator):
    """检查透明"""
    bl_idname = "import_xiaoer.check_transparent"
    bl_label = "检查透明"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        模型 = context.active_object
        return 模型 and 模型.type == 'MESH' and 模型.active_material

    def execute(self, context):
        # # self.report({"DEBUG"}, 'DEBUG')
        # self.report({"INFO"}, 'INFO')
        # self.report({"OPERATOR"}, 'OPERATOR')
        # self.report({"PROPERTY"}, 'PROPERTY')
        # self.report({"WARNING"}, 'WARNING')
        # self.report({"ERROR"}, 'ERROR')
        # # self.report({"ERROR_INVALID_INPUT"}, 'ERROR_INVALID_INPUT')
        # # self.report({"ERROR_INVALID_CONTEXT"}, 'ERROR_INVALID_CONTEXT')
        # # self.report({"ERROR_OUT_OF_MEMORY"}, 'ERROR_OUT_OF_MEMORY')
        偏好 = bpy.context.preferences.addons["导入小二"].preferences
        模型 = context.active_object
        材质面 = 获取材质面(self, 偏好, 模型)
        材质 = 模型.active_material
        图像, 节点 = 筛选贴图(self, 材质)
        if not 图像:
            self.report({"ERROR"}, f'材质Material["{材质.name}"]未找到贴图')
            return {'CANCELLED'}  # 确保返回有效结果
        if not 图像.filepath:
            self.report({"ERROR"}, f'["{图像.name}"]非本地图像')
            return {'CANCELLED'}  # 确保返回有效结果
        if not os.path.exists(图像.filepath):
            self.report({"ERROR"}, f'["{图像.name}"]未找到本地路径{图像.filepath}')
            return {'CANCELLED'}  # 确保返回有效结果
        贴图 = Image.open(图像.filepath).convert("RGBA")
        像素 = np.array(贴图)
        透明贴图 = defaultdict(list)  # 记录带有透明像素的贴图
        检查透明(偏好, 图像, 像素, 透明贴图)
        面像素点, 透明像素点, 完全透明像素点, 像素面索引 = 通过UV和像素检测透明材质(self, 偏好, 材质, 图像, 透明贴图, 材质面)
        # self.report({"INFO"}, f'材质Material["{材质.name}"]\n'
        #                       f'面像素点：{面像素点}\n'
        #                       f'透明像素点：{透明像素点}\n'
        #                       f'完全透明像素点：{完全透明像素点,}\n'
        #                       f'透明面索引：{像素面索引}')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='DESELECT')
        if 透明像素点 and 面像素点 and 像素面索引:
            def 输出检测结果(名称, 集合):
                检测结果 = 获取空白贴图(名称, 偏好.检测透明分辨率, True)
                # 将图像像素数据转为numpy数组方便操作
                像素数组 = np.array(检测结果.pixels[:]).reshape(偏好.检测透明分辨率, 偏好.检测透明分辨率, 4)
                # 设置指定像素为黑色透明 (0,0,0,0)
                for x, y in 集合:
                    if 0 <= x < 偏好.检测透明分辨率 and 0 <= y < 偏好.检测透明分辨率:  # 确保坐标有效
                        像素数组[y, x] = [0.0, 0.0, 0.0, 0.0]  # Blender中y轴是从下到上
                # 将修改后的数据写回Blender图像
                检测结果.pixels = 像素数组.flatten().tolist()
                检测结果.update()
            # 输出检测结果(f'{图像.name}透明像素检测结果', 透明像素点)
            输出检测结果(f'材质Material["{材质.name}"]UV像素检测结果', 面像素点)
            # 透明占比 = len(透明像素点 & 面像素点) / len(面像素点)
            # self.report({"INFO"}, f'{图像.name}透明像素数量{len(透明像素点)}\n材质Material["{材质.name}"]面像素数量{len(面像素点)} 其中透明像素数量{len(透明像素点 & 面像素点)}\n透明占比 {透明占比:.3%}')
            # if 透明像素点 & 面像素点 and not 面像素点 < 完全透明像素点:  # 材质面区域存在像素，并且材质非完全透明
            if 判断透明(self, 材质, 图像, 面像素点, 透明像素点, 完全透明像素点):
                # self.report({"INFO"}, f'材质Material["{材质.name}"] 透明像素点{透明像素点}')
                # self.report({"INFO"}, f'材质Material["{材质.name}"] 面像素点{面像素点}')
                # self.report({"INFO"}, f'材质Material["{材质.name}"] 透明像素{透明像素点 & 面像素点}')
                # if 透明占比 < 0.6:
                for 区域 in bpy.context.screen.areas:
                    if 区域.type == 'VIEW_3D':
                        区域.spaces.active.shading.type = 'RENDERED'
                    if 区域.type == 'IMAGE_EDITOR':
                        区域.spaces.active.image = 图像
                # bm = 材质面['bm'][0]
                # bm.faces.ensure_lookup_table()  # 访问索引前刷新
                bpy.ops.object.mode_set(mode='OBJECT')  # 必须切到 OBJECT 模式
                for 点 in 透明像素点 & 面像素点:
                    集合 = 像素面索引[点]
                    # self.report({"INFO"}, f'材质Material["{材质.name}"]\n {点} 像素面索引：{集合}')
                    for 索引 in 集合:
                        面 = 模型.data.polygons[索引]
                        if 模型.data.materials[面.material_index] is 材质:
                            面.select = True
                        # bm.faces[索引].select = True
                模型.data.update()
                # self.report({"INFO"}, f'材质Material["{材质.name}"]\n mesh.polygons:{len(模型.data.polygons)} bm.faces:{len(bm.faces)}')
                # 回写到 mesh
                # bpy.ops.object.mode_set(mode='OBJECT')  # 必须切到 OBJECT 模式
                # bm.to_mesh(模型.data)  # 将 bmesh 同步回 mesh 数据
                模型.data.update()  # 通知 Blender 刷新
                bpy.ops.object.mode_set(mode='EDIT')  # 再切回 EDIT 模式
                self.report({"INFO"}, f'材质Material["{材质.name}"]已选中透明面')
                return {'FINISHED'}
        self.report({"INFO"}, f'材质Material["{材质.name}"]检测为非透明材质')
        return {'FINISHED'}