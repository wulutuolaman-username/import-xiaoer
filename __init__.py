# coding: utf-8

bl_info = {
    "name": "导入小二",
    "description": "基于小二节点，用于特定游戏模型预设的Blender插件",
    "author": "五路拖拉慢",
    "version": (1, 0, 3),
    "blender": (3, 6, 0),
    "location": "View3D UI",
    "doc_url": "https://github.com/wulutuolaman-username/import-xiaoer/blob/main/README.md",
    "tracker_url": "https://github.com/wulutuolaman-username/import-xiaoer/issues/new",
    "category": "Import-Export"
}
IMPORT_XIAOER_VERSION = '.'.join(map(str,bl_info['version']))

import bpy
import os
import sys
import subprocess
import webbrowser
from bpy.props import CollectionProperty, StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.utils import previews
from mmd_tools.core import model

from .通用.查找 import 查找预设, 查找贴图
from .核心.导入模型预设 import 炒飞小二
from .核心.加载预设模板 import 干翻小二
from .核心.导出模型预设 import 透透小二
from .通用.清理 import 清理MMD刚体材质
from .xiaoer_updater import AddonUpdaterConfig, UpdateCandidateInfo, AddonUpdaterManager, CheckAddonUpdate, UpdateAddon
from .xiaoer_updater import register_updater

# Python（包括 Blender 的 API）不允许类名使用中文或非 ASCII 字符作为标识符
# 操作符基类
class SetTemplatePathBaseOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "xiaoer.set_path"
    bl_label = "Set Path"  # 这个属性是必须的
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(
        default="*.blend",
        options={'HIDDEN'},
        maxlen=255
    )
    属性: StringProperty()

    def execute(self, context):
        偏好 = context.preferences.addons[__name__].preferences
        setattr(偏好, self.属性, self.filepath)
        return {'FINISHED'}
# 具体操作符类
class SetUserPathOperator(SetTemplatePathBaseOperator):
    """设置用户路径"""
    bl_idname = "xiaoer.set_user_path"  # 操作符的唯一标识符
    bl_label = "选择预设目录"
    属性 = "预设目录"
class SetImagePathOperator(bpy.types.Operator, ImportHelper):
    """设置贴图路径"""
    bl_idname = "xiaoer.set_image_path"  # 操作符的唯一标识符
    bl_label = "选择贴图目录"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(
        default="*.png;*.jpg;*.jpeg;*.tga;*.exr;*.tif;*.tiff",
        options={'HIDDEN'},
        maxlen=255
    )
    # 目标属性名称
    属性: bpy.props.StringProperty()

    def execute(self, context):
        # 获取偏好设置对象
        偏好 = context.preferences.addons[__name__].preferences

        # 将选择的路径保存到目标属性
        setattr(偏好, self.属性, self.filepath)
        return {'FINISHED'}

class SetHonkai3PathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_honkai3_path"
    bl_label = "选择崩坏三模板文件"
    属性 = "honkai3_path"
class SetGenshinPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_genshin_path"
    bl_label = "选择原神模板文件"
    属性 = "genshin_path"
class SetHonkaiStarRailPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_honkai_star_rail_path"
    bl_label = "选择崩坏：星穹铁道模板文件"
    属性 = "honkai_star_rail_path"
class SetZenlessZoneZeroPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_zenless_zone_zero_path"
    bl_label = "选择绝区零模板文件"
    属性 = "zenless_zone_zero_path"
class SetWutheringwavesPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_wuthering_waves_path"
    bl_label = "选择鸣潮模板文件"
    属性 = "wuthering_waves_path"

class GameTemplateItem(bpy.types.PropertyGroup):  # 必须在偏好前定义
    """存储单个游戏模板数据"""
    名称: StringProperty(
        name="",
        description="游戏名称"
    )

class GAME_UL_TemplateList(bpy.types.UIList):
    """自定义游戏模板列表"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        # 紧凑模式布局
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            行 = layout.row(align=True)
            行.alignment = 'LEFT'

            # 显示图标
            icon_id = 图标预览[item.名称].icon_id
            行.label(text=item.名称, icon_value=icon_id)

# 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/preferences.py
def _get_update_candidate_branches(_, __):
    updater = AddonUpdaterManager.get_instance()
    if not updater.candidate_checked():
        return []

    return [(name, name, "") for name in updater.get_candidate_branch_names()]

# 设置面板开关属性和偏好设置文件路径
class XiaoerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    # 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/preferences.py
    # for add-on updater
    updater_branch_to_update: EnumProperty(
        name='Branch',
        description='Target branch to update add-on',
        items=_get_update_candidate_branches
    )

    自动查找预设: BoolProperty(
        name="自动查找预设",
        description="先在偏好设置中设置包含所有预设文件的目录，启用自动查找预设文件",
        default=True
    )

    预设目录: StringProperty(
        name="预设目录",
        description="设置预设文件的搜索根目录",
        subtype='DIR_PATH'
    )

    默认姿态: BoolProperty(
        name="默认姿态",
        description="若当前模型是默认的姿态，开启则继承面部定位属性；关闭后可以精准定位，但是调整变换属性",
        default=True
    )

    重命名资产: BoolProperty(
        name="重命名资产",
        description="建议在连续导入时开启,开启后可以对材质、节点组、贴图、驱动物体等对象的名称添加角色名重命名,以防止混淆，并放在单独的集合",
        default=False
    )

    独立集合: BoolProperty(
        name="集合",
        description="",
        default=True
    )  # 1.0.4新增

    重命名材质: BoolProperty(
        name="材质",
        description="",
        default=True
    )  # 1.0.4新增

    重命名贴图: BoolProperty(
        name="贴图",
        description="",
        default=True
    )  # 1.0.4新增

    重命名动作: BoolProperty(
        name="动作",
        description="",
        default=True
    )  # 1.0.4新增

    重命名节点组: BoolProperty(
        name="节点组",
        description="",
        default=True
    )  # 1.0.4新增

    重命名形态键: BoolProperty(
        name="形态键",
        description="",
        default=True
    )  # 1.0.4新增

    重命名驱动物体: BoolProperty(
        name="驱动物体",
        description="",
        default=True
    )  # 1.0.4新增

    重命名刚体和关节: BoolProperty(
        name="刚体和关节",
        description="",
        default=True
    )  # 1.0.4新增

    开启制作预设: BoolProperty(
        name="开启制作预设",
        description="开启后激活制作预设面板",
        default=True
    )  # 1.0.3新增

    导入贴图: BoolProperty(
        name="导入贴图",
        description="先在偏好设置中设置包含贴图文件的目录，开启后可以导入贴图",
        default=True
    )

    匹配基础贴图: BoolProperty(
        name="匹配基础贴图",
        description="图像感知哈希，先在偏好设置中设置包含所有贴图文件的目录，启用自动查找匹配基础贴图",
        default=True
    )

    搜索贴图文件夹: BoolProperty(
        name="搜索贴图文件夹",
        description="先在偏好设置中设置包含所有贴图文件的目录，开启后可以根据模型名称和贴图文件夹名称，搜索对应的贴图所在文件夹，关闭后需要直接指定模型贴图所在文件夹",
        default=True
    )

    汉明距离: bpy.props.IntProperty(
        name="",
        default=7,
        description="汉明距离越小匹配越严格",
        min = 1,  # 最小值
        max = 15,  # 最大值
    )

    贴图目录: StringProperty(
        name="贴图目录",
        description="设置贴图文件的搜索根目录",
        subtype='DIR_PATH'
    )

    游戏列表: bpy.props.CollectionProperty(
        type=GameTemplateItem,
        name="游戏列表"
    )

    当前列表选项索引: bpy.props.IntProperty(
        name="",
        default=0
    )

    # 定义每个模板的独立路径属性 # 不能使用中文冒号：
    崩坏三模板路径: StringProperty(name="崩坏三模板路径", description="设置崩坏三模板文件路径",subtype='FILE_PATH')
    原神模板路径: StringProperty(name="原神模板路径", description="设置原神模板文件路径", subtype='FILE_PATH')
    崩坏星穹铁道模板路径: StringProperty(name="崩坏：星穹铁道模板路径", description="设置崩坏：星穹铁道模板文件路径", subtype='FILE_PATH')
    绝区零模板路径: StringProperty(name="绝区零模板路径", description="设置绝区零模板文件路径", subtype='FILE_PATH')
    鸣潮模板路径: StringProperty(name="鸣潮模板路径", description="设置鸣潮模板文件路径", subtype='FILE_PATH')

    def draw(self, context):  # 仅在偏好设置显示路径设置
        layout = self.layout

        # 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/preferences.py
        updater = AddonUpdaterManager.get_instance()
        update_col = layout.column(align=False)
        if updater.updated():
            col = update_col.column()
            col.scale_y = 2
            col.alert = True
            col.operator(
                "wm.quit_blender",
                text="重启Blender完成更新",
                icon="ERROR"
            )
            return

        if not updater.candidate_checked():
            col = update_col.column()
            col.scale_y = 2
            col.operator(
                "xiaoer.check_addon_update",
                text="检查插件更新（测试）",
                icon='FILE_REFRESH'
            )
        else:
            row = update_col.row(align=True)
            row.scale_y = 2
            col = row.column()
            col.operator(
                "xiaoer.check_addon_update",
                text="检查插件更新（测试）",
                icon='FILE_REFRESH'
            )
            col = row.column()
            if updater.update_ready():
                col.enabled = True
                col.operator(
                    "xiaoer.update_addon",
                    text=bpy.app.translations.pgettext_iface("安装最新版本({})").format(updater.latest_version()),
                    icon='TRIA_DOWN_BAR'
                ).branch_name = updater.latest_version()

                # 1.02增加版本更新说明
                latest_version = updater.latest_version()
                latest_body = ""
                for candidate in updater._AddonUpdaterManager__update_candidate:
                    if candidate.name == latest_version and candidate.group == 'RELEASE':
                        latest_body = candidate.body
                        break

                box = update_col.box()
                box.label(text="更新说明：", icon='TEXT')
                lines = latest_body.split('\n')
                for line in lines:
                    if line.strip():
                        box.label(text=line)

            else:
                col.enabled = False
                col.operator(
                    "xiaoer.update_addon",
                    text="没有更新可用"
                )

            update_col.separator()
            update_col.label(text="(Danger) Manual Update:")
            row = update_col.row(align=True)
            row.prop(self, "updater_branch_to_update", text="Target")
            row.operator(
                "xiaoer.update_addon", text="更新",
                icon='TRIA_DOWN_BAR'
            ).branch_name = self.updater_branch_to_update

            update_col.separator()
            if updater.has_error():
                box = update_col.box()
                box.label(text=updater.error(), icon='CANCEL')
            elif updater.has_info():
                box = update_col.box()
                box.label(text=updater.info(), icon='ERROR')
            # 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/preferences.py

        # layout.label(text="预设目录设置")
        行 = layout.row(align=True)
        行.prop(self, "预设目录", text="预设目录", icon='FILE_FOLDER')
        行.scale_x = 0.5
        键 = 行.operator("xiaoer.set_user_path", text="选择预设目录", icon='FILE_FOLDER')
        键.属性 = "预设目录"  # 将路径属性名传递给操作符

        列 = layout.column(align=True)  # 1.0.4新增
        行 = 列.row(align=True)
        分割 = 行.split(factor=0.3)
        左侧 = 分割.column()  # 分割行，左侧占30%宽度
        左侧.prop(self, "重命名资产", text="重命名资产可选项： ", icon='ASSET_MANAGER')
        左侧.scale_y = 2
        右侧 = 分割.column()  # 右侧子行
        右侧.enabled = self.重命名资产
        右行 = 右侧.row(align=True)
        右行.prop(self, "独立集合", icon='OUTLINER_COLLECTION')
        右行.prop(self, "重命名材质", icon='MATERIAL')
        右行.prop(self, "重命名贴图", icon='IMAGE_DATA')
        右行.prop(self, "重命名节点组", icon='NODETREE')
        右行 = 右侧.row(align=True)
        右行.prop(self, "重命名动作", icon='ACTION')
        右行.prop(self, "重命名形态键", icon='SHAPEKEY_DATA')
        右行.prop(self, "重命名驱动物体", icon='OBJECT_DATA')
        右行.prop(self, "重命名刚体和关节", icon='RIGID_BODY')

        行 = layout.row(align=True)  # 1.0.3新增
        行.prop(self, "开启制作预设", text="  开启制作预设面板 需自备贴图和预设模板")
        行 = layout.row(align=True)
        行.label(text="已适配公开预设：崩坏三、原神、崩坏：星穹铁道", icon='CHECKMARK')

        if self.开启制作预设:  # 1.0.3新增
            # layout.label(text="贴图目录设置")
            行 = layout.row(align=True)
            行.prop(self, "贴图目录", text="贴图目录", icon='FILE_IMAGE')
            行.scale_x = 0.5
            键 = 行.operator("xiaoer.set_image_path", text="选择贴图目录", icon='FILE_IMAGE')
            键.属性 = "贴图目录"  # 将路径属性名传递给操作符

            # 模板路径设置
            def 设置模板路径(游戏,操作):
                行 = layout.row(align=True)  # 关键点：align=True 确保子元素对齐
                左侧 = 行.split(factor=0.1)  # 分割行，左侧占10%宽度
                左侧.template_icon(icon_value=图标预览[游戏].icon_id, scale=2)  # 图标放在左侧
                右侧 = 左侧.column(align=True)  # 右侧子行
                路径 = f'{游戏.replace("：", "")}模板路径'
                右侧.prop(bpy.context.preferences.addons[__name__].preferences, 路径, text=游戏, icon='BLENDER')
                键 = 右侧.operator(操作, icon='BLENDER')
                键.属性 = 路径  # 将路径属性名传递给操作符
            设置模板路径("崩坏三", "xiaoer.set_honkai3_path")
            设置模板路径("原神", "xiaoer.set_genshin_path")
            设置模板路径("崩坏：星穹铁道", "xiaoer.set_honkai_star_rail_path")
            设置模板路径("绝区零", "xiaoer.set_zenless_zone_zero_path")
            设置模板路径("鸣潮", "xiaoer.set_wuthering_waves_path")

# 打开偏好设置
class OPEN_PREFERENCES_OT_open_addon_prefs(bpy.types.Operator):
    """打开插件偏好设置"""
    bl_idname = "import_xiaoer.open_addon_prefs"
    bl_label = "设置偏好路径"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 打开用户偏好设置窗口
        bpy.ops.screen.userpref_show()
        # 切换到Add-ons选项卡
        context.preferences.active_section = 'ADDONS'
        # 获取当前插件的显示名称
        小二插件 = context.preferences.addons.get(__name__)
        if 小二插件:
            addon_name = bl_info["name"]
            context.window_manager.addon_search = addon_name  # 设置搜索过滤
        else:
            self.report({'WARNING'}, "插件未找到，请确保已启用。")
        return {'FINISHED'}

# 全选模型  # 1.0.4新增
class SelectAllMeshes(bpy.types.Operator):
    """全选模型"""
    bl_idname = "import_xiaoer.select_all_meshes"
    bl_label = "全选模型"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return context.mode == 'OBJECT'  # 必须是物体模式
    def execute(self, context):
        # 取消所有选择
        bpy.ops.object.select_all(action='DESELECT')
        # 遍历所有对象，找到骨架及其子网格模型
        for 骨架 in bpy.data.objects:
            if 骨架.type == 'ARMATURE':
                for 模型 in 骨架.children:
                    if 模型.type == 'MESH':
                        模型.select = True
                        # 模型.select_set(True)  # 推荐使用新 API
                        context.view_layer.objects.active = 模型  # ✅ 设置为激活对象
        for 物 in bpy.context.selected_objects:
            self.report({"INFO"}, f'{物.name}')
        return {'FINISHED'}  # ✅ 必须是 set 类型！

class ImportMatPresets(bpy.types.Operator):
    """ 选择对应模型预设导入 """
    bl_idname = "import_test.import_mat_presets"
    bl_label = "导入材质到模型"
    bl_options = {"UNDO"}

    file_path: StringProperty(
        name="文件路径",
        description="预设文件路径",
        default="",
        subtype='FILE_PATH'
    )

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context):
        偏好 = context.preferences.addons[__name__].preferences
        if 偏好.预设目录:
            if os.path.exists(偏好.预设目录):
                for 模型 in bpy.context.selected_objects:  # 可能选择了多个物体
                    文件路径, 角色 = 查找预设(偏好, 模型)  # 读取文件路径和文件名称
                    if 文件路径 and 角色:
                        self.report({"INFO"}, "匹配名称："+str(角色))
                        炒飞小二(偏好, 模型, 文件路径, 角色, self)
                    else:
                        self.report({"WARNING"}, f"未找到{模型.name}匹配预设，请在偏好设置预设目录，检查模型名称和预设文件名是否正确对应，或关闭自动查找预设手动导入")
                if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
                    清理MMD刚体材质()  # 整理MMD刚体材质
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, f"预设目录不存在")
                return {'CANCELLED'}  # 确保返回有效结果
        else:
            self.report({'WARNING'}, f"未设置预设目录")
            return {'CANCELLED'}  # 确保返回有效结果

class ImportMatPresetsFilebrowser(bpy.types.Operator, ImportHelper):
    bl_idname = "import_test.import_mat_presets_filebrowser"
    bl_label = "选择预设文件"

    files: CollectionProperty(type=bpy.types.PropertyGroup)
    filter_glob: StringProperty(
        default="*.blend",
        options={'HIDDEN'},
        maxlen=255,
    )

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context):
        偏好 = context.preferences.addons[__name__].preferences
        文件路径 = self.filepath  # 手动选择的文件路径
        角色 = os.path.splitext(os.path.basename(文件路径))[0]  # 获取文件名（去掉路径和扩展名）
        角色 = 角色.replace("渲染", "")  # 去掉“渲染”字样（如果有）
        角色 = 角色.replace("预设", "")  # 去掉“预设”字样（如果有）
        self.report({"INFO"}, f"匹配名称：" + str(角色))
        模型 = bpy.context.object  # 获取当前选中的模型
        炒飞小二(偏好, 模型, 文件路径, 角色, self)
        if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
            清理MMD刚体材质()  # 整理MMD刚体材质
        return {'FINISHED'}

class ExecuteTemplate(bpy.types.Operator):
    """ 选择游戏加载预设模板，设置描边材质，连接节点组 """
    bl_idname = "import_xiaoer.execute_template"
    bl_label = "加载预设模板"

    # 定义两个路径属性
    模板路径: StringProperty(subtype='FILE_PATH')
    贴图路径: StringProperty(subtype='FILE_PATH')  # 重命名为image_path

    @classmethod
    def poll(self, context):

        return context.object is not None and context.object.type == 'MESH'

    def invoke(self, context, event):
        偏好 = bpy.context.preferences.addons[__name__].preferences
        选中项 = 偏好.游戏列表[偏好.当前列表选项索引]
        偏好名称 = 选中项.名称.replace("：", "")
        文件路径 = getattr(偏好, f"{偏好名称}模板路径", None)
        if 文件路径 and os.path.exists(文件路径):
            self.模板路径 = 文件路径  # 传递模板路径
            if 偏好.导入贴图:
                贴图路径 = 偏好.贴图目录
                if 贴图路径 and os.path.exists(贴图路径):
                    pass
                elif not 贴图路径:
                    self.report({"WARNING"}, f"未设置贴图路径")
                    return {'CANCELLED'}  # 确保返回有效结果
                elif not os.path.exists(贴图路径):
                    self.report({"WARNING"}, f"贴图路径不存在")
                    return {'CANCELLED'}  # 确保返回有效结果
            return self.execute(context)
        elif not 文件路径:
            self.report({"WARNING"}, f"未设置{选中项.名称}预设模板路径")
            return {'CANCELLED'}  # 确保返回有效结果
        elif not os.path.exists(文件路径):
            self.report({"WARNING"}, f"{选中项.名称}预设模板路径不存在")
            return {'CANCELLED'}  # 确保返回有效结果

    def execute(self, context):
        偏好 = bpy.context.preferences.addons[__name__].preferences
        选中项 = 偏好.游戏列表[偏好.当前列表选项索引]
        游戏 = 选中项.名称
        模型 = bpy.context.object
        文件路径 = self.模板路径
        # self.report({"INFO"}, f"再次检查偏好路径：" + str(file_path))
        贴图路径 = None  # 初始化
        if 偏好.导入贴图:
            if 偏好.搜索贴图文件夹: # 如果开启了自动搜索贴图文件夹
                if not 偏好.贴图目录 and not os.path.exists(偏好.贴图目录):
                    self.report({"WARNING"}, f"未设置贴图路径或贴图路径不存在")
                    return None
                贴图路径, 角色 = 查找贴图(偏好, 模型)
                if 贴图路径 and 角色:
                    self.report({"INFO"}, "搜索到贴图文件夹名称："+str(角色))
                else:
                    self.report({"WARNING"}, f"未搜索到{模型.name}贴图")
                    return {'CANCELLED'}  # 确保返回有效结果
            else:  # 如果没有开启搜索贴图路径，那就是导入偏好路径下的贴图
                贴图路径 = 偏好.贴图目录
        if 文件路径:
            干翻小二(self, 偏好, 模型, 游戏, 文件路径, 贴图路径)
        return {'FINISHED'}

class ExportMatPresets(bpy.types.Operator,ExportHelper):
    """ 选择对应模型导出预设 """
    bl_idname = "export_test.export_mat_presets"
    bl_label = "导出模型预设"
    bl_options = {"UNDO"}

    # 文件类型过滤
    filename_ext = ".blend"
    filter_glob: StringProperty(
        default="*.blend",
        options={'HIDDEN'},
        maxlen=255,
    )

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH'

    # 动态设置默认路径和文件名
    def invoke(self, context, event):
        # 获取用户预设路径
        偏好 = context.preferences.addons[__name__].preferences
        if 偏好.预设目录:
            self.filepath = os.path.join(
                偏好.预设目录,  # 从偏好设置获取路径
                self.generate_filename(context)  # 自动生成文件名
            )
            return super().invoke(context, event)
        else:
            self.report({'WARNING'}, f"未设置预设目录")
            return {'CANCELLED'}  # 确保返回有效结果

    def generate_filename(self, context):
        """生成默认文件名逻辑"""
        模型 = context.object
        if 模型:
            名称 = 模型.name.replace("_mesh", "")
            return f"{名称}预设.blend"
        return "untitled.blend"

    def execute(self, context):

        # 最终保存路径处理
        保存路径 = os.path.normpath(self.filepath)
        保存信息 = os.path.dirname(保存路径)

        # 路径有效性检查
        if not os.path.exists(保存信息):
            os.makedirs(保存信息)

        if not os.access(保存信息, os.W_OK):
            self.report({'WARNING'}, f"无写入权限: {保存信息}")
            return {'CANCELLED'}

        # try:
        # 执行保存操作
        bpy.ops.wm.save_as_mainfile(
            filepath=保存路径,
            check_existing=True,  # 检查文件存在
            copy=True  # 保持原文件不受影响
        )
        self.report({'INFO'}, f"导出预设: {保存路径}")
        模型 = context.object
        模型名称 = 模型.name
        bpy.ops.wm.open_mainfile(filepath=保存路径)
        模型 = bpy.data.objects[模型名称]
        模型.select_set(True)
        透透小二(self, 模型)
        # 保存最终文件
        bpy.ops.wm.save_mainfile(filepath=self.filepath)
        # except Exception as e:
        #     self.report({'ERROR'}, f"导出失败: {str(e)}")
        #     return {'CANCELLED'}
        # 删除备份文件 (blend1)  #1.0.3新增
        备份文件 = f"{保存路径}1"  # Blender自动创建的备份文件
        if os.path.exists(备份文件):
            try:
                os.remove(备份文件)
                self.report({'INFO'}, f"已删除备份文件: {备份文件}")
            except Exception as e:
                self.report({'WARNING'}, f"删除备份文件失败: {str(e)}")
        return {'FINISHED'}

class OpenWebsite(bpy.types.Operator):
    bl_idname = "xiaoer.open_website"
    bl_label = "打开网站"
    bl_description = "点击跳转到指定网站"

    url: bpy.props.StringProperty(name="URL", default="")  # 接收 URL 参数

    def execute(self, context):
        if self.url:
            webbrowser.open(self.url)  # 使用 webbrowser 打开链接
            self.report({'INFO'}, f"已打开: {self.url}")
        else:
            self.report({'ERROR'}, "未提供 URL")
        return {'FINISHED'}

class XiaoerBilibiliOpenWebsite(OpenWebsite):
    bl_idname = "xiaoer.open_website_bilibili"
    bl_label = " 小二新教程啥时候更新捏"
    bl_description = "点击前往小二主页催更"
    url: bpy.props.StringProperty(default="https://space.bilibili.com/437528440?spm_id_from=333.337.0.0")
class XiaoerAfdianOpenWebsite(OpenWebsite):
    bl_idname = "xiaoer.open_website_afdian"
    bl_label = ""
    bl_description = "点击前往小二爱发电主页获取预设"
    url: bpy.props.StringProperty(default="https://afdian.com/a/xiaoer?tab=feed")
class XiaoerAplayboxOpenWebsite(OpenWebsite):
    bl_idname = "xiaoer.open_website_aplaybox"
    bl_label = ""
    bl_description = "点击前往小二模之屋主页获取预设"
    url: bpy.props.StringProperty(default="https://www.aplaybox.com/u/872092888")

class XiaoerUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "小二主页"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import1"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        layout = self.layout

        # 添加按钮
        行 = layout.row(align=True)
        行.operator(
            "xiaoer.open_website_bilibili",  # 操作符 ID
            icon_value=图标预览["小二"].icon_id,   # 按钮图标
            emboss=False  # 隐藏按钮背景
        )
        左侧 = 行.split(factor=0.08, align=True)
        右端 = 左侧.column(align=True)
        右端.label(icon='FUND')

# 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/panels/sidebar.py
class MMDtoolsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "mmd_tools"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import2"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    # 定义一个绘制函数
    def draw(self, context):
        def check_operator_exists(op_id):
            try:
                # 分割操作符ID为模块和操作符名（例如："mmd_tools.import_model"）
                module_name, operator_name = op_id.split('.', 1)
                # 检查 bpy.ops 模块中是否存在对应的操作符
                op_module = getattr(bpy.ops, module_name)
                getattr(op_module, operator_name)
                return True
            except (AttributeError, ValueError):
                return False

        exist = check_operator_exists('mmd_tools.import_model')
        if exist:  # 如果存在mmd_tools操作符
            行 = self.layout.row()
            col = 行.column(align=True)
            col.operator('mmd_tools.import_model', text="导入模型", icon='OUTLINER_OB_ARMATURE')
            col = 行.column(align=True)
            col.operator('mmd_tools.import_vmd', text='导入动作', icon='ANIM')
            col = 行.column(align=True)
            col.operator('mmd_tools.import_vpd', text='导入姿态', icon='POSE_HLT')
        if context.object:
            行 = self.layout.row()
            col = 行.column(align=True)
            active_object: bpy.types.Object = context.active_object
            mmd_root_object = model.Model.findRoot(active_object)
            if mmd_root_object:
                mmd_root = mmd_root_object.mmd_root
                if not mmd_root.is_built:
                    col.operator('mmd_tools.build_rig', text='物理', icon='PHYSICS', depress=False)
                else:
                    col.operator('mmd_tools.clean_rig', text='物理', icon='PHYSICS', depress=True)
                col = 行.column(align=True)
                rigidbody_world = context.scene.rigidbody_world
                if rigidbody_world:
                    point_cache = rigidbody_world.point_cache
                    if point_cache.is_baked is True:
                        col.operator("mmd_tools.ptcache_rigid_body_delete_bake", text="删除烘培", icon='TRASH')
                    else:
                        col.operator("mmd_tools.ptcache_rigid_body_bake", text="烘培", icon='MEMORY')

class ImportMatPresetsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "使用预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import3"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    # 定义一个绘制函数
    def draw(self, context):

        偏好 = context.preferences.addons[__name__].preferences

        # 导入按钮
        行 = self.layout.row()
        行.scale_y = 2
        if 偏好.自动查找预设:  # 自动导入
            行.operator("import_test.import_mat_presets", text="炒飞小二", icon='IMPORT')
        else:  #手动导入
            行.operator("import_test.import_mat_presets_filebrowser", text="手动导入", icon='IMPORT')

        # 自动查找开关
        行 = self.layout.row()
        行.prop(偏好, "自动查找预设", text="自动查找预设", icon='VIEWZOOM')

        # 默认姿态开关
        行 = self.layout.row()
        行.prop(偏好, "默认姿态", text="默认姿态",icon='OUTLINER_DATA_ARMATURE')

        # 连续导入开关
        行 = self.layout.row(align=True)
        列 = 行.column()
        列.operator("import_xiaoer.select_all_meshes", text="全选模型", icon='SELECT_EXTEND')
        列 = 行.column()
        列.prop(偏好, "重命名资产", text="重命名资产",icon='ASSET_MANAGER')

        if not 偏好.开启制作预设:  # 1.0.3新增
            行 = self.layout.row()
            行.operator("import_xiaoer.open_addon_prefs", text="打开偏好设置", icon='PREFERENCES')
            # 导出预设
            行 = self.layout.row()
            行.scale_y = 2
            行.operator("export_test.export_mat_presets", text="导出预设", icon='EXPORT')

class GetMatPresetsUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "获取预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import4"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        行 = self.layout.row()
        列 = 行.column(align=True)
        列.operator(
            "xiaoer.open_website_afdian",  # 操作符 ID
            text="爱发电",
            icon_value=图标预览["爱发电"].icon_id   # 按钮图标
        )
        列 = 行.column(align=True)
        列.operator(
            "xiaoer.open_website_aplaybox",  # 操作符 ID
            text="模之屋",
            icon_value=图标预览["模之屋"].icon_id   # 按钮图标
        )

class ExecuteTemplateUI(bpy.types.Panel):
    bl_category = "导入小二"  # 侧边栏标签
    bl_label = "制作预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import5"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    @classmethod  # 1.0.3新增
    def poll(cls, context):
        偏好 = context.preferences.addons[__name__].preferences
        return 偏好.开启制作预设

    # 定义一个绘制函数
    def draw(self, context):
        偏好 = context.preferences.addons[__name__].preferences

        # 选择预设模板
        行 = self.layout.row()
        左侧 = 行.split(factor=0.4)  # 分割行，左侧占40%宽度
        左侧.label(text = "选择游戏")
        右侧 = 左侧.column(align=True)  # 右侧子行
        右侧.operator("import_xiaoer.open_addon_prefs", text="打开偏好设置", icon='PREFERENCES')

        框 = self.layout.box()
        框.template_list(
            "GAME_UL_TemplateList",  # UIList类名
            "template_list",         # 列表ID
            偏好, "游戏列表", # 数据集合
            偏好, "当前列表选项索引" # 当前选中索引
        )

        # 导入贴图开关
        行 = self.layout.row()
        左侧 = 行.split(align=True)  # 分割行
        左侧.prop(偏好, "导入贴图", text="导入贴图", icon='IMPORT')
        # 搜索贴图路径开关
        右侧 = 行.split(align=True)
        右侧.prop(偏好, "搜索贴图文件夹", text="搜索贴图", icon='VIEWZOOM')
        右侧.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用

        # 自动匹配贴图开关
        行 = self.layout.row()
        左侧 = 行.split(align=True)  # 分割行
        左侧.prop(偏好, "匹配基础贴图", text="匹配基础贴图", icon='XRAY')  #1.0.3
        左侧.enabled = 偏好.导入贴图  # 根据 导入贴图 启用/禁用
        # 汉明距离
        右侧 = 行.split(align=True)  # 分割行
        右侧.prop(偏好, "汉明距离", text="<=汉明距离", slider=True, icon='MOD_LENGTH')
        右侧.enabled = 偏好.导入贴图 and 偏好.匹配基础贴图  # 双重依赖条件

        # 导入预设模板
        行 = self.layout.row()
        行.scale_y = 2
        行.operator("import_xiaoer.execute_template", text="加载预设模板", icon='NODE')

        # 导出预设
        行 = self.layout.row()
        行.scale_y = 2
        行.operator("export_test.export_mat_presets", text="导出预设", icon='EXPORT')

classes = (
    # SetTemplatePathBaseOperator,
    SetUserPathOperator,
    SetImagePathOperator,

    SetHonkai3PathOperator,
    SetGenshinPathOperator,
    SetHonkaiStarRailPathOperator,
    SetZenlessZoneZeroPathOperator,
    SetWutheringwavesPathOperator,

    GameTemplateItem,  #  必须在偏好前定义
    GAME_UL_TemplateList,

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

def 游戏列表添加(游戏):
    偏好 = bpy.context.preferences.addons[__name__].preferences
    for 东西 in 偏好.游戏列表:
        if 东西.名称 == 游戏:
            return
    东西 = 偏好.游戏列表.add()
    东西.名称 = 游戏

def 加载图标():
    图标预览 = previews.new()
    图标文件夹 = os.path.join(os.path.dirname(__file__), "图标")
    for 文件名 in os.listdir(图标文件夹):
        图标路径 = os.path.join(os.path.dirname(__file__), "图标", 文件名)
        图标名称 = 文件名[:-4]
        if os.path.exists(图标路径):
            try:
                图标预览.load(图标名称,图标路径,'IMAGE')  # 使用显示名作为键
            except KeyError as e:
                if "already exists" in str(e):
                    continue  # 如果已经加载则跳过
                raise  # 其他错误继续抛出
    return 图标预览

def register():

    # 初始化更新器
    register_updater(bl_info, __file__)  # ✅ 确保这行存在

    for clss in classes:
        bpy.utils.register_class(clss)

    游戏列表添加("崩坏三")
    游戏列表添加("原神")
    游戏列表添加("崩坏：星穹铁道")
    游戏列表添加("绝区零")
    游戏列表添加("鸣潮")

    global 图标预览
    图标预览 = 加载图标()  # 使用游戏列表检查，必须在注册之后

    轮子路径 = os.path.join(os.path.dirname(__file__), "轮子", "ImageHash-4.3.2-py2.py3-none-any.whl")
    subprocess.run([sys.executable, "-m", "pip", "install", 轮子路径])

    python_exe = sys.executable  # 1.01更新：注册安装/升级Pillow
    try:
        # 安装/升级Pillow
        subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pillow"])
        # 验证安装
        try:
            from PIL import Image
            print(f"🟢 Pillow版本: {Image.__version__}")
        except ImportError:
            raise Exception("Pillow安装成功但无法导入，请关闭blender，删除缓存文件后重新启动")
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