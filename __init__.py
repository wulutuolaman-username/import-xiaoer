# coding: utf-8

bl_info = {
    "name": "导入小二",
    "description": "基于小二节点，用于特定游戏模型渲染预设的Blender插件",
    "author": "五路拖拉慢",
    "version": (1, 2, 1),
    "blender": (3, 6, 0),
    "location": "View3D UI",
    "doc_url": "https://github.com/wulutuolaman-username/import-xiaoer/blob/main/README.md",
    "tracker_url": "https://github.com/wulutuolaman-username/import-xiaoer/issues",
    "category": "Import-Export"
}

from .偏好.偏好设置 import *
XiaoerAddonPreferences.bl_idname = bl_info["name"]

from .更新 import register_updater
from .注册 import 注册, 注销


def register():
    # 初始化更新器
    register_updater(bl_info, __file__)  # ✅ 确保这行存在
    注册()

def unregister():
    注销()

if __name__ == "__main__":
    register()

# ------------------------------------------------------------------
# 我要成为bpy高手
# import boy
# import 小二
# import love
#
# bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
# cube = bpy.context.active_object
# cube.scale[0] = 10 / 2
# cube.scale[1] = 5 / 2
# cube.scale[2] = 2 / 2
# 我的大床 = bpy.context.active_object
# 我的大床.name = "我的大床"
#
# 我的大床 = bpy.data.collections.new(name="我的大床")
# bpy.context.scene.collection.children.link(我的大床)
#
# bpy.ops.mesh.primitive_cone_add(radius=1, location=(0, 0, 0))
# 香薰 = bpy.context.active_object
# 香薰.name = "香薰"
# 我的大床.objects.link(香薰)
#
# bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=(2, 0, 0))
# 蜡烛 = bpy.context.active_object
# 蜡烛.name = "蜡烛"
# 我的大床.objects.link(蜡烛)
#
# bpy.ops.mesh.primitive_curve_add(radius=0.5, depth=2, location=(2, 0, 0))
# 皮鞭 = bpy.context.active_object
# 皮鞭.name = "皮鞭"
# 我的大床.objects.link(皮鞭)
#
# bpy.ops.curve.primitive_bezier_circle_add(major_radius=1, minor_radius=0.25, location=(4, 0, 0))
# 项圈 = bpy.context.active_object
# 项圈.name = "项圈"
# 我的大床.objects.link(项圈)
#
# if not 小二:
#   小二 = boy.get("小二今天吃啥啊",衣服=None)
#   小二.clothes.remove("裤衩子")
# while 小二 not in 我的大床
#   我的大床.boys.link(小二)
# love.with(小二)
# love.with(小二).again()
# love.with(小二).again_and_again()