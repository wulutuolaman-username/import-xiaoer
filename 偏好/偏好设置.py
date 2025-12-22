import bpy
from ..偏好.检查更新 import XiaoerAddonCheckUpdate
from ..偏好.使用预设 import XiaoerAddonImortSettings
from ..偏好.重命名项 import XiaoerAddonRenameAssets
from ..偏好.制作预设 import XiaoerAddonOpenMakingAssets

# Python（包括 Blender 的 API）不允许类名使用中文或非 ASCII 字符作为标识符
class XiaoerAddonPreferences(bpy.types.AddonPreferences,
                             XiaoerAddonCheckUpdate,
                             XiaoerAddonImortSettings,
                             XiaoerAddonRenameAssets,
                             XiaoerAddonOpenMakingAssets,
                             ):

    def draw(self, context):  # 仅在偏好设置显示路径设置
        布局 = self.layout
        self.更新面板(布局)
        self.设置目录(布局)
        self.重命名项(布局)
        self.开启制作(布局)