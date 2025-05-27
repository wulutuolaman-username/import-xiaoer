import bpy
from bpy.props import BoolProperty, StringProperty, CollectionProperty, IntProperty
from ..列表 import GameTemplateItem
from ..图标 import 加载图标
图标预览 = 加载图标()

class OpenMakingAssets:
    开启制作预设: BoolProperty(
        name="开启制作预设",
        description="开启后激活制作预设面板",
        default=True
    )  # 1.0.3新增

    贴图目录: StringProperty(
        name="贴图目录",
        description="设置贴图文件的搜索根目录",
        subtype='DIR_PATH'
    )

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

    汉明距离: IntProperty(
        name="",
        default=7,
        description="汉明距离越小匹配越严格",
        min = 1,  # 最小值
        max = 15,  # 最大值
    )

    游戏列表: CollectionProperty(
        type=GameTemplateItem,
        name="游戏列表"
    )

    当前列表选项索引: IntProperty(
        name="",
        default=0
    )

    # 定义每个模板的独立路径属性 # 不能使用中文冒号：
    崩坏三模板路径: StringProperty(name="崩坏三模板路径", description="设置崩坏三模板文件路径",subtype='FILE_PATH')
    原神模板路径: StringProperty(name="原神模板路径", description="设置原神模板文件路径", subtype='FILE_PATH')
    崩坏星穹铁道模板路径: StringProperty(name="崩坏：星穹铁道模板路径", description="设置崩坏：星穹铁道模板文件路径", subtype='FILE_PATH')
    绝区零模板路径: StringProperty(name="绝区零模板路径", description="设置绝区零模板文件路径", subtype='FILE_PATH')
    鸣潮模板路径: StringProperty(name="鸣潮模板路径", description="设置鸣潮模板文件路径", subtype='FILE_PATH')

    def 开启制作(self,layout):
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
                右侧.prop(bpy.context.preferences.addons["导入小二"].preferences, 路径, text=游戏, icon='BLENDER')
                键 = 右侧.operator(操作, icon='BLENDER')
                键.属性 = 路径  # 将路径属性名传递给操作符
            设置模板路径("崩坏三", "xiaoer.set_honkai3_path")
            设置模板路径("原神", "xiaoer.set_genshin_path")
            设置模板路径("崩坏：星穹铁道", "xiaoer.set_honkai_star_rail_path")
            设置模板路径("绝区零", "xiaoer.set_zenless_zone_zero_path")
            设置模板路径("鸣潮", "xiaoer.set_wuthering_waves_path")