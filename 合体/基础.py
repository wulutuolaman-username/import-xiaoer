import bpy  # noqa: F401
from ..偏好.偏好设置 import *
from ..更新 import CheckAddonUpdate, UpdateAddon
from ..列表 import GameTemplateItem, GAME_UL_TemplateList
from ..操作.设置路径 import *
from ..操作.转到网页 import *
from ..操作.打开偏好 import OPEN_PREFERENCES_OT_open_addon_prefs
from ..操作.选中.全选模型 import SelectAllMeshes
from ..操作.选中.选中模型 import SelectModel
from ..操作.复制文本 import XiaoerAddon_OT_copy_to_clipboard
from ..操作.检查透明 import XiaoerAddonCheckTransparent
from ..操作.重启软件 import IMPORT_XIAOER_OT_restart_blender
from ..操作.模块.安装模块 import Install_Packages
from ..操作.模块.卸载模块 import Uninstall_Packages
from ..操作.核心.导入模型预设 import XiaoerAddonImportMatPresets, XiaoerAddonImportMatPresetsFilebrowser
from ..操作.核心.加载预设模板 import XiaoerAddonExecuteTemplate
from ..操作.核心.导出模型预设 import XiaoerAddonExportMatPresets
from ..面板.视图.小二 import XiaoerUI
from ..面板.视图.反馈 import InformationFeedbackUI
from ..面板.视图.引用 import MMDtoolsUI, BetterFBXUI
from ..面板.视图.使用 import ImportMatPresetsUI
from ..面板.视图.获取 import GetMatPresetsUI
from ..面板.视图.制作 import ExecuteTemplateUI
from ..面板.视图.调整 import MaterialListUI
from ..面板.图像.UV import UVPanel

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

    XiaoerAddonPreferences,
    OPEN_PREFERENCES_OT_open_addon_prefs,

    SelectAllMeshes,
    SelectModel,
    XiaoerAddon_OT_copy_to_clipboard,
    XiaoerAddonCheckTransparent,
    IMPORT_XIAOER_OT_restart_blender,

    XiaoerAddonImportMatPresets,
    XiaoerAddonImportMatPresetsFilebrowser,

    # GameTemplateItem,
    # GAME_UL_TemplateList,

    XiaoerAddonExecuteTemplate,

    XiaoerAddonExportMatPresets,

    XiaoerBilibiliOpenWebsite,
    XiaoerAfdianOpenWebsite,
    XiaoerAplayboxOpenWebsite,
    WulutuolamanTiktokOpenWebsite,
    WulutuolamanBilibiliOpenWebsite,
    TemplateExampleOpenWebsite,

    Install_Packages,
    Uninstall_Packages,

    XiaoerUI,
    InformationFeedbackUI,
    MMDtoolsUI,
    BetterFBXUI,
    GetMatPresetsUI,
    ImportMatPresetsUI,
    ExecuteTemplateUI,
    MaterialListUI,
    UVPanel,
)

def 注册类():
    for clss in classes:
        try:  # 1.0.8避免重复注册
            bpy.utils.register_class(clss)
        except:
            pass

def 注销类():
    for clss in classes:
        try:
            bpy.utils.unregister_class(clss)
        except:
            pass