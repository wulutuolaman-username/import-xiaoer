bl_info = {
    "name": "导入小二",
    "description": "",
    "author": "五路拖拉慢",
    "version": (1, 0, 0),
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

from .general.find import find_preset, find_texture
from .main.ImportMatPresets import chaofei_xiaoer
from .main.ExecuteTemplate import ganfan_xiaoer
from .main.ExportMatPresets import toutou_xiaoer
from .general.clean import clean_mmd_tools_rigid_material, clean_mmd_tools_node_group
from .updater import AddonUpdaterConfig, UpdateCandidateInfo, AddonUpdaterManager, CheckAddonUpdate, UpdateAddon
from .updater import register_updater

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
    target_property: StringProperty()

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        setattr(prefs, self.target_property, self.filepath)
        return {'FINISHED'}
# 具体操作符类
class SetUserPathOperator(SetTemplatePathBaseOperator):
    """设置用户路径"""
    bl_idname = "xiaoer.set_user_path"  # 操作符的唯一标识符
    bl_label = "选择预设目录"
    target_property = "user_path"
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
    target_property: bpy.props.StringProperty()

    def execute(self, context):
        # 获取偏好设置对象
        prefs = context.preferences.addons[__name__].preferences

        # 将选择的路径保存到目标属性
        setattr(prefs, self.target_property, self.filepath)
        return {'FINISHED'}

# class SetHonkai3Part1PathOperator(SetTemplatePathBaseOperator):
#     bl_idname = "xiaoer.set_honkai3_part1_path"
#     bl_label = "选择崩坏三第一部模板文件"
#     target_property = "honkai3_part1_path"
# class SetHonkai3Part2PathOperator(SetTemplatePathBaseOperator):
#     bl_idname = "xiaoer.set_honkai3_part2_path"
#     bl_label = "选择崩坏三第二部模板文件"
#     target_property = "honkai3_part2_path"
class SetHonkai3PathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_honkai3_path"
    bl_label = "选择崩坏三模板文件"
    target_property = "honkai3_path"
class SetGenshinPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_genshin_path"
    bl_label = "选择原神模板文件"
    target_property = "genshin_path"
class SetHonkaiStarRailPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_honkai_star_rail_path"
    bl_label = "选择崩坏：星穹铁道模板文件"
    target_property = "honkai_star_rail_path"
class SetZenlessZoneZeroPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_zenless_zone_zero_path"
    bl_label = "选择绝区零模板文件"
    target_property = "zenless_zone_zero_path"
class SetWutheringwavesPathOperator(SetTemplatePathBaseOperator):
    bl_idname = "xiaoer.set_wuthering_waves_path"
    bl_label = "选择鸣潮模板文件"
    target_property = "wuthering_waves_path"

class GameTemplateItem(bpy.types.PropertyGroup):  # 必须在偏好前定义
    """存储单个游戏模板数据"""
    identifier: StringProperty(
        name="",
        description="匹配路径"
    )
    name: StringProperty(
        name="",
        description="游戏名称"
    )

class GAME_UL_TemplateList(bpy.types.UIList):
    """自定义游戏模板列表"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        # 紧凑模式布局
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.alignment = 'LEFT'

            # 显示图标（从gcoll获取）
            icon_id = pcoll[item.name].icon_id
            row.label(text=item.name, icon_value=icon_id)

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

    auto_find: BoolProperty(
        name="自动查找预设",
        description="先在偏好设置中设置包含所有预设文件的目录，启用自动查找预设文件",
        default=True
    )

    user_path: StringProperty(
        name="预设目录",
        description="设置预设文件的搜索根目录",
        subtype='DIR_PATH'
    )

    import_image: BoolProperty(
        name="导入贴图",
        description="先在偏好设置中设置包含贴图文件的目录，开启后可以导入贴图",
        default=True
    )

    auto_match_image: BoolProperty(
        name="自动查找匹配基础贴图",
        description="图像感知哈希，先在偏好设置中设置包含所有贴图文件的目录，启用自动查找匹配基础贴图",
        default=True
    )

    search_image: BoolProperty(
        name="搜索贴图文件夹",
        description="先在偏好设置中设置包含所有贴图文件的目录，开启后可以根据模型名称搜索对应的贴图所在文件夹，关闭后需要直接指定模型贴图所在文件夹",
        default=True
    )

    Hamming_distance: bpy.props.IntProperty(
        name="",
        default=7,
        description="汉明距离越小匹配越严格",
        min = 1,  # 最小值
        max = 15,  # 最大值
    )

    texture_path: StringProperty(
        name="贴图目录",
        description="设置贴图文件的搜索根目录",
        subtype='DIR_PATH'
    )

    default_pose: BoolProperty(
        name="默认姿态",
        description="若当前模型是默认的姿态，开启则继承面部定位属性；关闭后可以精准定位，但是调整变换属性",
        default=True
    )

    continuous_importer: BoolProperty(
        name="连续导入（重命名资产）",
        description="开启后可以对材质、节点组、贴图、驱动物体等对象的名称添加角色名重命名,以防止混淆，并放在单独的集合",
        default=False
    )

    game_templates: bpy.props.CollectionProperty(
        type=GameTemplateItem,
        name="游戏列表"
    )

    active_template_index: bpy.props.IntProperty(
        name="",
        default=0
    )

    # 定义每个模板的独立路径属性
    # honkai3_part1_path: StringProperty(name="崩坏三第一部模板路径", description="设置崩坏三第一部模板文件路径",subtype='FILE_PATH')
    # honkai3_part2_path: StringProperty(name="崩坏三第二部模板路径", description="设置崩坏三第二部模板文件路径", subtype='FILE_PATH')
    honkai3_path: StringProperty(name="崩坏三模板路径", description="设置崩坏三模板文件路径",subtype='FILE_PATH')
    genshin_path: StringProperty(name="原神模板路径", description="设置原神模板文件路径", subtype='FILE_PATH')
    honkai_star_rail_path: StringProperty(name="崩坏：星穹铁道模板路径", description="设置崩坏：星穹铁道模板文件路径", subtype='FILE_PATH')
    zenless_zone_zero_path: StringProperty(name="绝区零模板路径", description="设置绝区零模板文件路径", subtype='FILE_PATH')
    wuthering_waves_path: StringProperty(name="鸣潮模板路径", description="设置鸣潮模板文件路径", subtype='FILE_PATH')

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
        row = layout.row(align=True)
        row.prop(self, "user_path", text="预设目录", icon='FILE_FOLDER')
        row.scale_x = 0.5
        op = row.operator("xiaoer.set_user_path", text="选择预设目录", icon='FILE_FOLDER')
        op.target_property = "user_path"  # 将路径属性名传递给操作符

        # layout.label(text="贴图目录设置")
        row = layout.row(align=True)
        row.prop(self, "texture_path", text="贴图目录", icon='FILE_IMAGE')
        row.scale_x = 0.5
        op = row.operator("xiaoer.set_image_path", text="选择贴图目录", icon='FILE_IMAGE')
        op.target_property = "texture_path"  # 将路径属性名传递给操作符

        # 模板路径设置
        def Set_Template_Path(path,game,operator):
            row = layout.row(align=True)  # 关键点：align=True 确保子元素对齐
            split = row.split(factor=0.1)  # 分割行，左侧占10%宽度
            split.template_icon(icon_value=pcoll[game].icon_id, scale=2)  # 图标放在左侧
            split_right = split.column(align=True)  # 右侧子行
            split_right.prop(bpy.context.preferences.addons[__name__].preferences, path, text=game, icon='BLENDER')
            op = split_right.operator(operator, icon='BLENDER')
            op.target_property = path  # 将路径属性名传递给操作符
        # Set_Template_Path("honkai3_part1_path", "崩坏三第一部", "xiaoer.set_honkai3_part1_path")
        # Set_Template_Path("honkai3_part2_path", "崩坏三第二部", "xiaoer.set_honkai3_part2_path")
        Set_Template_Path("honkai3_path", "崩坏三", "xiaoer.set_honkai3_path")
        Set_Template_Path("genshin_path", "原神", "xiaoer.set_genshin_path")
        Set_Template_Path("honkai_star_rail_path", "崩坏：星穹铁道", "xiaoer.set_honkai_star_rail_path")
        Set_Template_Path("zenless_zone_zero_path", "绝区零", "xiaoer.set_zenless_zone_zero_path")
        Set_Template_Path("wuthering_waves_path", "鸣潮", "xiaoer.set_wuthering_waves_path")

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
        addon_prefs = context.preferences.addons.get(__name__)
        if addon_prefs:
            addon_name = bl_info["name"]
            context.window_manager.addon_search = addon_name  # 设置搜索过滤
        else:
            self.report({'WARNING'}, "插件未找到，请确保已启用。")
        return {'FINISHED'}

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
        prefs = context.preferences.addons[__name__].preferences
        if prefs.user_path:
            if os.path.exists(prefs.user_path):
                for model in bpy.context.selected_objects:  # 可能选择了多个物体
                    result = find_preset(prefs, model)  # 读取文件路径和文件名称
                    if result:
                        file_path, file_name = result  # 分别赋值文件路径和文件名称
                        self.report({"INFO"}, "匹配名称："+str(file_name))
                        chaofei_xiaoer(prefs, model, file_path, file_name, self)
                    else:
                        self.report({"WARNING"}, f"未找到{model.name}匹配预设，请在偏好设置预设目录，检查模型名称和预设文件名是否正确对应，或关闭自动查找预设手动导入")
                if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
                    clean_mmd_tools_rigid_material()  # 整理MMD刚体材质
                    clean_mmd_tools_node_group()  # 整理MMD固有节点组
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
        prefs = context.preferences.addons[__name__].preferences
        file_path = self.filepath  # 手动选择的文件路径
        file_name = os.path.splitext(os.path.basename(file_path))[0]  # 获取文件名（去掉路径和扩展名）
        file_name = file_name.replace("渲染", "")  # 去掉“渲染”字样（如果有）
        file_name = file_name.replace("预设", "")  # 去掉“预设”字样（如果有）
        self.report({"INFO"}, f"匹配名称：" + str(file_name))
        model = bpy.context.object  # 获取当前选中的模型
        chaofei_xiaoer(prefs, model, file_path, file_name, self)
        if prefs.continuous_importer:  ############### 如果开启了连续导入 ###############
            clean_mmd_tools_rigid_material()  # 整理MMD刚体材质
            clean_mmd_tools_node_group()  # 整理MMD固有节点组
        return {'FINISHED'}

class ExecuteTemplate(bpy.types.Operator):
    """ 选择游戏加载预设模板，设置描边材质，连接节点组 """
    bl_idname = "import_xiaoer.execute_template"
    bl_label = "加载预设模板"

    # 定义两个路径属性
    template_path: StringProperty(subtype='FILE_PATH')
    image_path: StringProperty(subtype='FILE_PATH')  # 重命名为image_path

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH'

    def invoke(self, context, event):
        prefs = context.preferences.addons[__name__].preferences

        active_item = prefs.game_templates[prefs.active_template_index]
        file_path = getattr(prefs, f"{active_item.identifier}_path", None)

        if file_path and os.path.exists(file_path):
            self.template_path = file_path  # 传递模板路径
            if prefs.import_image:
                image_path = prefs.texture_path
                if image_path and os.path.exists(image_path):
                    pass
                elif not image_path:
                    self.report({"WARNING"}, f"未设置贴图路径")
                    return {'CANCELLED'}  # 确保返回有效结果
                elif not os.path.exists(image_path):
                    self.report({"WARNING"}, f"贴图路径不存在")
                    return {'CANCELLED'}  # 确保返回有效结果
            return self.execute(context)
        elif not file_path:
            self.report({"WARNING"}, f"未设置{active_item.name}预设模板路径")
            return {'CANCELLED'}  # 确保返回有效结果
        elif not os.path.exists(file_path):
            self.report({"WARNING"}, f"{active_item.name}预设模板路径不存在")
            return {'CANCELLED'}  # 确保返回有效结果

    def execute(self, context):
        model = bpy.context.object
        file_path = self.template_path
        # self.report({"INFO"}, f"再次检查偏好路径：" + str(file_path))
        image_path = None  # 初始化
        prefs = context.preferences.addons[__name__].preferences
        if prefs.import_image:
            if prefs.search_image: # 如果开启了自动搜索贴图文件夹
                if not prefs.texture_path and not os.path.exists(prefs.texture_path):
                    self.report({"WARNING"}, f"未设置贴图路径或贴图路径不存在")
                    return None
                result = find_texture(prefs, model)
                if result:
                    image_path, dir_name = result
                    self.report({"INFO"}, "搜索到贴图文件夹名称："+str(dir_name))
                else:
                    self.report({"WARNING"}, f"未搜索到{model.name}贴图")
                    return {'CANCELLED'}  # 确保返回有效结果
            else:  # 如果没有开启搜索贴图路径，那就是导入偏好路径下的贴图
                image_path = prefs.texture_path
        if file_path:
            ganfan_xiaoer(self, prefs, model, file_path, image_path)
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
        prefs = context.preferences.addons[__name__].preferences
        if prefs.user_path:
            self.filepath = os.path.join(
                prefs.user_path,  # 从偏好设置获取路径
                self.generate_filename(context)  # 自动生成文件名
            )
            return super().invoke(context, event)
        else:
            self.report({'WARNING'}, f"未设置预设目录")
            return {'CANCELLED'}  # 确保返回有效结果

    def generate_filename(self, context):
        """生成默认文件名逻辑"""
        model = context.object
        if model:
            clean_name = model.name.replace("_mesh", "")
            return f"{clean_name}预设.blend"
        return "untitled.blend"

    def execute(self, context):

        # 最终保存路径处理
        save_path = os.path.normpath(self.filepath)
        save_dir = os.path.dirname(save_path)

        # 路径有效性检查
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        if not os.access(save_dir, os.W_OK):
            self.report({'WARNING'}, f"无写入权限: {save_dir}")
            return {'CANCELLED'}

        # try:
        # 执行保存操作
        bpy.ops.wm.save_as_mainfile(
            filepath=save_path,
            check_existing=True,  # 检查文件存在
            copy=True  # 保持原文件不受影响
        )
        self.report({'INFO'}, f"导出预设: {save_path}")
        model = context.object
        model_name = model.name
        bpy.ops.wm.open_mainfile(filepath=save_path)
        model = bpy.data.objects[model_name]
        model.select_set(True)
        toutou_xiaoer(self, model)
        # 保存最终文件
        bpy.ops.wm.save_mainfile(filepath=self.filepath)
        # except Exception as e:
        #     self.report({'ERROR'}, f"导出失败: {str(e)}")
        #     return {'CANCELLED'}
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
    bl_label = "小二新教程啥时候更新捏"
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
class FengfengBilibiliOpenWebsite(OpenWebsite):
    bl_idname = "fengfeng.open_website"
    bl_label = ""
    bl_description = "峰峰居士主页"
    url: bpy.props.StringProperty(default="https://space.bilibili.com/373134990?spm_id_from=333.337.0.0")
class FushengBilibiliOpenWebsite(OpenWebsite):
    bl_idname = "fusheng.open_website"
    bl_label = ""
    bl_description = "芙生一梦主页"
    url: bpy.props.StringProperty(default="https://space.bilibili.com/449654059?spm_id_from=333.337.0.0")
class ChatGPTOpenWebsite(OpenWebsite):
    bl_idname = "chatgpt.open_website"
    bl_label = ""
    bl_description = "chatgpt.com"
    url: bpy.props.StringProperty(default="https://chatgpt.com/")
class DeepseekOpenWebsite(OpenWebsite):
    bl_idname = "deepseek.open_website"
    bl_label = ""
    bl_description = "deepseek.com"
    url: bpy.props.StringProperty(default="https://chat.deepseek.com/")
class WuluBilibiliOpenWebsite(OpenWebsite):
    bl_idname = "wulu.open_website"
    bl_label = ""
    bl_description = "五路拖拉慢主页"
    url: bpy.props.StringProperty(default="https://space.bilibili.com/230130803?spm_id_from=333.1007.0.0")

class XiaoerUI(bpy.types.Panel):
    bl_category = "XiaoerTools"  # 侧边栏标签
    bl_label = "小二主页"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        layout = self.layout

        # 添加按钮
        row = layout.row(align=True)
        row.operator(
            "xiaoer.open_website_bilibili",  # 操作符 ID
            icon_value=pcoll["小二"].icon_id,   # 按钮图标
            emboss=False  # 隐藏按钮背景
        )
        split = row.split(factor=0.08, align=True)
        col = split.column(align=True)
        col.label(icon='FUND')

# 代码来源：https://github.com/MMD-Blender/blender_mmd_tools/blob/blender-v3/mmd_tools/panels/sidebar.py
class MMDtoolsUI(bpy.types.Panel):
    bl_category = "XiaoerTools"  # 侧边栏标签
    bl_label = "mmd_tools"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import0"  # 工具ID
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
            row = self.layout.row()
            col = row.column(align=True)
            col.operator('mmd_tools.import_model', text="导入模型", icon='OUTLINER_OB_ARMATURE')
            col = row.column(align=True)
            col.operator('mmd_tools.import_vmd', text='导入动作', icon='ANIM')
            col = row.column(align=True)
            col.operator('mmd_tools.import_vpd', text='导入姿态', icon='POSE_HLT')
        if context.object:
            row = self.layout.row()
            col = row.column(align=True)
            active_object: bpy.types.Object = context.active_object
            mmd_root_object = model.Model.findRoot(active_object)
            if mmd_root_object:
                mmd_root = mmd_root_object.mmd_root
                if not mmd_root.is_built:
                    col.operator('mmd_tools.build_rig', text='物理', icon='PHYSICS', depress=False)
                else:
                    col.operator('mmd_tools.clean_rig', text='物理', icon='PHYSICS', depress=True)
                col = row.column(align=True)
                rigidbody_world = context.scene.rigidbody_world
                if rigidbody_world:
                    point_cache = rigidbody_world.point_cache
                    if point_cache.is_baked is True:
                        col.operator("mmd_tools.ptcache_rigid_body_delete_bake", text="删除烘培", icon='TRASH')
                    else:
                        col.operator("mmd_tools.ptcache_rigid_body_bake", text="烘培", icon='MEMORY')

class ImportMatPresetsUI(bpy.types.Panel):
    bl_category = "XiaoerTools"  # 侧边栏标签
    bl_label = "使用预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import1"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    # 定义一个绘制函数
    def draw(self, context):

        prefs = context.preferences.addons[__name__].preferences

        # 导入按钮
        row = self.layout.row()
        row.scale_y = 2
        if prefs.auto_find:  # 自动导入
            row.operator("import_test.import_mat_presets", text="炒飞小二", icon='IMPORT')
        else:  #手动导入
            row.operator("import_test.import_mat_presets_filebrowser", text="手动导入", icon='IMPORT')

        # 自动查找开关
        row = self.layout.row()
        row.prop(prefs, "auto_find", text="自动查找预设", icon='VIEWZOOM')

        # 默认姿态开关
        row = self.layout.row()
        row.prop(prefs, "default_pose", text="默认姿态",icon='OUTLINER_DATA_ARMATURE')

        # 连续导入开关
        row = self.layout.row()
        row.prop(prefs, "continuous_importer", text="连续导入（重命名资产）",icon='ASSET_MANAGER')

class GetMatPresetsUI(bpy.types.Panel):
    bl_category = "XiaoerTools"  # 侧边栏标签
    bl_label = "获取预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import2"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        row = self.layout.row()
        col = row.column(align=True)
        col.operator(
            "xiaoer.open_website_afdian",  # 操作符 ID
            text="爱发电",
            icon_value=pcoll["爱发电"].icon_id   # 按钮图标
        )
        col = row.column(align=True)
        col.operator(
            "xiaoer.open_website_aplaybox",  # 操作符 ID
            text="模之屋",
            icon_value=pcoll["模之屋"].icon_id   # 按钮图标
        )

class ExecuteTemplateUI(bpy.types.Panel):
    bl_category = "XiaoerTools"  # 侧边栏标签
    bl_label = "制作预设"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import3"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    # 定义一个绘制函数
    def draw(self, context):
        prefs = context.preferences.addons[__name__].preferences

        # 选择预设模板
        row = self.layout.row()
        split = row.split(factor=0.4)  # 分割行，左侧占40%宽度
        split.label(text = "选择游戏")
        split_right = split.column(align=True)  # 右侧子行
        split_right.operator("import_xiaoer.open_addon_prefs", text="打开偏好设置", icon='PREFERENCES')

        box = self.layout.box()
        box.template_list(
            "GAME_UL_TemplateList",  # UIList类名
            "template_list",         # 列表ID
            prefs, "game_templates", # 数据集合
            prefs, "active_template_index" # 当前选中索引
        )

        # 导入贴图开关
        row = self.layout.row()
        split = row.split(align=True)  # 分割行
        split.prop(prefs, "import_image", text="导入贴图", icon='IMPORT')
        # 搜索贴图路径开关
        split = row.split(align=True)
        split.prop(prefs, "search_image", text="搜索贴图", icon='VIEWZOOM')
        split.enabled = prefs.import_image  # 根据 import_image 启用/禁用

        # 自动匹配贴图开关
        row = self.layout.row()
        split = row.split(align=True)  # 分割行
        split.prop(prefs, "auto_match_image", text="匹配贴图", icon='XRAY')
        split.enabled = prefs.import_image  # 根据 import_image 启用/禁用
        # 汉明距离
        split = row.split(align=True)  # 分割行
        split.prop(prefs, "Hamming_distance", text="汉明距离", slider=True, icon='MOD_LENGTH')
        split.enabled = prefs.import_image and prefs.auto_match_image  # 双重依赖条件

        # 导入预设模板
        row = self.layout.row()
        row.scale_y = 2
        row.operator("import_xiaoer.execute_template", text="加载预设模板", icon='NODE')

        # 导出预设
        row = self.layout.row()
        row.scale_y = 2
        row.operator("export_test.export_mat_presets", text="导出预设", icon='EXPORT')

class DeveloperUI(bpy.types.Panel):
    bl_category = "XiaoerTools"  # 侧边栏标签
    bl_label = "插件开发"  # 工具卷展栏标签
    bl_idname = "OBJECT_PT_import4"  # 工具ID
    bl_space_type = 'VIEW_3D'  # 空间类型():3D视图
    bl_region_type = 'UI'  # 区域类型:右边侧栏

    def draw(self, context):
        layout = self.layout
        row = layout.row(align = True)
        # row = layout.scale_x = 2
        # 添加按钮
        row.operator(
            "fengfeng.open_website",  # 操作符 ID
            # text="",
            icon_value=pcoll["峰峰居士"].icon_id,   # 按钮图标
            emboss=False  # 隐藏按钮背景
        )
        # 添加按钮
        row.operator(
            "fusheng.open_website",  # 操作符 ID
            # text="",
            icon_value=pcoll["芙生一梦"].icon_id,   # 按钮图标
            emboss=False  # 隐藏按钮背景
        )
        # 添加按钮
        row.operator(
            "chatgpt.open_website",  # 操作符 ID
            # text="",
            icon_value=pcoll["ChatGPT"].icon_id,  # 按钮图标
            emboss=False  # 隐藏按钮背景
        )
        # 添加按钮
        row.operator(
            "deepseek.open_website",  # 操作符 ID
            # text="",
            icon_value=pcoll["DeepSeek"].icon_id,   # 按钮图标
            emboss=False  # 隐藏按钮背景
        )
        # 添加按钮
        row.operator(
            "wulu.open_website",  # 操作符 ID
            # text="",
            icon_value=pcoll["五路拖拉慢"].icon_id,   # 按钮图标
            emboss=False  # 隐藏按钮背景
        )

classes = (
            # SetTemplatePathBaseOperator,
            SetUserPathOperator,
            SetImagePathOperator,

            # SetHonkai3Part1PathOperator,
            # SetHonkai3Part2PathOperator,
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

            ImportMatPresets,
            ImportMatPresetsFilebrowser,

            # GameTemplateItem,
            # GAME_UL_TemplateList,

            ExecuteTemplate,
            # ExecuteTemplateFilebrowser,
            # ImportTextureFilebrowser,

            ExportMatPresets,

            XiaoerBilibiliOpenWebsite,
            XiaoerAfdianOpenWebsite,
            XiaoerAplayboxOpenWebsite,
            FengfengBilibiliOpenWebsite,
            FushengBilibiliOpenWebsite,
            ChatGPTOpenWebsite,
            DeepseekOpenWebsite,
            WuluBilibiliOpenWebsite,

            XiaoerUI,
            MMDtoolsUI,
            ImportMatPresetsUI,
            GetMatPresetsUI,
            ExecuteTemplateUI,
            DeveloperUI,
)

icon_map = [  # 图标文件名，引用图标，模板偏好路径
    ('xiaoer.jpg', '小二', ''),
    ('afdian.png', '爱发电', ''),
    ('aplaybox.png', '模之屋', ''),
    ('fengfeng.jpg', '峰峰居士', ''),
    ('fusheng.jpg', '芙生一梦', ''),
    ('ChatGPT.jpeg', 'ChatGPT', ''),
    ('deepseek.png', 'DeepSeek', ''),
    ('wulu.png', '五路拖拉慢', ''),
    # ('Honkai3Part1.png', '崩坏三第一部', 'honkai3_part1'),
    # ('Honkai3Part2.jpg', '崩坏三第二部', 'honkai3_part2'),
    ('Honkai3Part1.png', '崩坏三', 'honkai3'),
    ('Genshin.png', '原神','genshin'),
    ('HonkaiStarRail.png', '崩坏：星穹铁道', 'honkai_star_rail'),
    ('ZenlessZoneZero.png', '绝区零', 'zenless_zone_zero'),
    ('WutheringWaves.png', '鸣潮', 'wuthering_waves'),
]
no_game = ('xiaoer.jpg','afdian.png','aplaybox.png','fengfeng.jpg','fusheng.jpg','ChatGPT.jpeg','deepseek.png','wulu.png')
def get_icon_path():
    prefs = bpy.context.preferences.addons[__name__].preferences
    pcoll = previews.new()
    for filename, name, identifier in icon_map:
        icon_path = os.path.join(os.path.dirname(__file__), "icon", filename)
        if filename not in no_game and name not in prefs.game_templates:
            item = prefs.game_templates.add()
            item.identifier = identifier
            item.name = name
        if os.path.exists(icon_path):
            try:
                pcoll.load(name,icon_path,'IMAGE')  # 使用显示名作为键
            except KeyError as e:
                if "already exists" in str(e):
                    continue  # 如果已经加载则跳过
                raise  # 其他错误继续抛出
    return pcoll

def register():

    # 初始化更新器
    register_updater(bl_info, __file__)  # ✅ 确保这行存在

    for clss in classes:
        bpy.utils.register_class(clss)

    global pcoll
    pcoll = get_icon_path()  # 使用game_templates检查，必须在注册之后

    _whl_path = os.path.join(os.path.dirname(__file__), "wheels", "ImageHash-4.3.2-py2.py3-none-any.whl")
    subprocess.run([sys.executable, "-m", "pip", "install", _whl_path])

def unregister():

    for clss in classes:
        bpy.utils.unregister_class(clss)

    global pcoll
    previews.remove(pcoll)
    pcoll = None

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