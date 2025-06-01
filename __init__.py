# coding: utf-8

bl_info = {
    "name": "导入小二",
    "description": "基于小二节点，用于特定游戏模型预设的Blender插件",
    "author": "五路拖拉慢",
    "version": (1, 0, 8),
    "blender": (3, 6, 0),
    "location": "View3D UI",
    "doc_url": "https://github.com/wulutuolaman-username/import-xiaoer/blob/main/README.md",
    "tracker_url": "https://github.com/wulutuolaman-username/import-xiaoer/issues/new",
    "category": "Import-Export"
}

import bpy
import sys
import subprocess
from bpy.utils import previews

from .更新 import CheckAddonUpdate, UpdateAddon
from .更新 import register_updater
from .偏好.检查更新 import CheckUpdate
from .偏好.导入设置 import ImortSettings
from .偏好.重命名项 import RenameAssets
from .偏好.开启制作 import OpenMakingAssets
from .图标 import 加载图标
from .列表 import 游戏列表添加, GameTemplateItem, GAME_UL_TemplateList
from .操作.设置路径 import SetUserPathOperator, SetImagePathOperator, SetHonkai3PathOperator, SetGenshinPathOperator, SetHonkaiStarRailPathOperator, SetZenlessZoneZeroPathOperator, SetWutheringwavesPathOperator
from .操作.转到网页 import UpdateHistory, XiaoerAfdianOpenWebsite, XiaoerAplayboxOpenWebsite, XiaoerBilibiliOpenWebsite
from .操作.打开偏好 import OPEN_PREFERENCES_OT_open_addon_prefs
from .操作.全选模型 import SelectAllMeshes
from .操作.核心.导入模型预设 import ImportMatPresets, ImportMatPresetsFilebrowser
from .操作.核心.加载预设模板 import ExecuteTemplate
from .操作.核心.导出模型预设 import ExportMatPresets
from .面板.小二 import XiaoerUI
from .面板.引用 import MMDtoolsUI
from .面板.使用 import ImportMatPresetsUI
from .面板.获取 import GetMatPresetsUI
from .面板.制作 import ExecuteTemplateUI

# Python（包括 Blender 的 API）不允许类名使用中文或非 ASCII 字符作为标识符
class XiaoerPreferences(bpy.types.AddonPreferences,
                        CheckUpdate,
                        ImortSettings,
                        RenameAssets,
                        OpenMakingAssets,
                        ):
    bl_idname = __name__

    def draw(self, context):  # 仅在偏好设置显示路径设置
        layout = self.layout
        self.更新面板(layout)
        self.预设目录设置(layout)
        self.重命名可选项(layout)
        self.开启制作(layout)

classes = (
    # SetTemplatePathBaseOperator,
    SetUserPathOperator,
    SetImagePathOperator,

    SetHonkai3PathOperator,
    SetGenshinPathOperator,
    SetHonkaiStarRailPathOperator,
    SetZenlessZoneZeroPathOperator,
    SetWutheringwavesPathOperator,

    GameTemplateItem,  #  必须在偏好前
    GAME_UL_TemplateList,

    UpdateHistory,

    # AddonUpdaterConfig,
    # UpdateCandidateInfo,
    # AddonUpdaterManager,
    CheckAddonUpdate,
    UpdateAddon,

    XiaoerPreferences,
    OPEN_PREFERENCES_OT_open_addon_prefs,

    SelectAllMeshes,

    ImportMatPresets,
    ImportMatPresetsFilebrowser,

    # GameTemplateItem,
    # GAME_UL_TemplateList,

    ExecuteTemplate,

    ExportMatPresets,

    XiaoerBilibiliOpenWebsite,
    XiaoerAfdianOpenWebsite,
    XiaoerAplayboxOpenWebsite,

    XiaoerUI,
    MMDtoolsUI,
    ImportMatPresetsUI,
    GetMatPresetsUI,
    ExecuteTemplateUI,
)

def register():

    # 初始化更新器
    register_updater(bl_info, __file__)  # ✅ 确保这行存在

    for clss in classes:
        try:  # 1.0.8避免重复注册
            bpy.utils.register_class(clss)
        except:
            pass

    global 图标预览
    图标预览 = 加载图标()  # 使用游戏列表检查，必须在注册之后

    游戏列表添加("崩坏三")
    游戏列表添加("原神")
    游戏列表添加("崩坏：星穹铁道")
    游戏列表添加("绝区零")
    游戏列表添加("鸣潮")

    python_exe = sys.executable

    # 1.0.7注册安装/升级imagehash
    try:
        subprocess.check_call(
            [python_exe, "-m", "pip", "install", "--force-reinstall", "ImageHash", "--disable-pip-version-check"],
            stdout=subprocess.DEVNULL
        )
        import imagehash
        version = getattr(imagehash, '__version__', '未知版本')
        print(f"🟢 ImageHash 安装成功 (版本: {version})")
    except Exception as e:
        raise Exception(f"❌ ImageHash 安装失败: {str(e)}")

    # 1.0.1注册安装/升级Pillow
    try:
        # 安装/升级Pillow
        subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pillow"])
        # 验证安装
        try:
            from PIL import Image
            # print(f"🟢 pillow版本: {Image.__version__}")
        except ImportError:
            raise Exception("pillow安装成功但无法导入，请关闭blender，删除缓存文件后重新启动")
    except Exception:
        raise Exception("pillow安装失败")

def unregister():

    for clss in classes:
        bpy.utils.unregister_class(clss)

    global 图标预览
    previews.remove(图标预览)
    图标预览 = None

    # subprocess.run([sys.executable, "-m", "pip", "uninstall", "imagehash"])  # 卸载或关闭插件会卡死

if __name__ == "__main__":
    register()

# ------------------------------------------------------------------
# 我要成为bpy高手
# import boy
# import xiao_er
# import love
#
# bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
# cube = bpy.context.active_object
# cube.scale[0] = 10 / 2
# cube.scale[1] = 5 / 2
# cube.scale[2] = 2 / 2
# my_big_bed = bpy.context.active_object
# my_big_bed.name = "my_big_bed"
#
# my_big_bed = bpy.data.collections.new(name="my_big_bed")
# bpy.context.scene.collection.children.link(my_big_bed)
#
# bpy.context.scene.collection.children.link(xiao_er)
#
# bpy.ops.mesh.primitive_cone_add(radius=1, location=(0, 0, 0))
# xian_xun = bpy.context.active_object
# xian_xun.name = "xiang_xun"
# my_big_bed.objects.link(xiang_xun)
#
# bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=(2, 0, 0))
# la_zhu_pi_bian = bpy.context.active_object
# la_zhu_pi_bian.name = "la_zhu"
# my_big_bed.objects.link(la_zhu)
#
# bpy.ops.mesh.primitive_curve_add(radius=0.5, depth=2, location=(2, 0, 0))
# la_zhu_pi_bian = bpy.context.active_object
# la_zhu_pi_bian.name = "pi_bian"
# my_big_bed.objects.link(pi_bian)
#
# bpy.ops.curve.primitive_bezier_circle_add(major_radius=1, minor_radius=0.25, location=(4, 0, 0))
# xiang_quan = bpy.context.active_object
# xiang_quan.name = "xiang_quan"
# my_big_bed.objects.link(xiang_quan)
#
# bpy.ops.mesh.primitive_torus_add(radius1=0.5, depth=2, location=(6, 0, 0))
# ku_cha_zi = bpy.context.active_object
# ku_cha_zi.name = "ku_cha_zi"
# my_big_bed.objects.link(ku_cha_zi)
#
# while xiao_er not in my_big_bed
#   bpy.context.scene.collection.children.link(xiao_er)
# love_with(xiao_er)
# love_with(xiao_er).again
# love_with(xiao_er).again_and_again