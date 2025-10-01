import bpy
from bpy.props import BoolProperty, StringProperty, CollectionProperty, IntProperty
from .更新状态 import 更新基础贴图alpha连接, 更新通过点乘混合法向
from ..列表 import GameTemplateItem
from ..图标 import 加载图标

图标预览 = 加载图标()

class XiaoerAddonOpenMakingAssets:

    开启制作预设: BoolProperty(
        name="开启制作预设",
        description="开启后激活制作预设面板",
        default=True
    )  # 1.0.3新增

    def 更新状态(self, context, 当前选项, 选项列表):
        if hasattr(self, 当前选项) and getattr(self, 当前选项, True):
            for 选项 in 选项列表:
                setattr(self, 选项, False)  # 动态设置属性
            # 强制标记属性为已修改
            context.scene.update_tag()
        return None  # 显式返回 None

    贴图目录: StringProperty(
        name="贴图目录",
        description="设置贴图文件的搜索根目录",
        # subtype='DIR_PATH',
        # update=lambda self, context: None,
    )

    导入贴图: BoolProperty(
        name="导入贴图",
        description="先在偏好设置中设置包含贴图文件的目录，开启后可以导入贴图",
        default=True
    )

    搜索贴图文件夹: BoolProperty(
        name="搜索贴图文件夹",
        description="先在偏好设置中设置包含所有贴图文件的目录，开启后可以根据模型名称和贴图文件夹名称，搜索模型对应的贴图所在文件夹，关闭后需要直接指定模型贴图所在文件夹",
        default=True,
        # update=更新搜索贴图文件夹
        update=lambda self, context: self.更新状态(context, '搜索贴图文件夹', ['指定贴图文件夹', '使用模型路径'])
    )
    指定贴图文件夹: BoolProperty(
        name="指定贴图文件夹",
        description="临时指定的贴图文件夹，直接导入其中的贴图",
        default=False,
        # update=更新指定贴图文件夹
        update=lambda self, context: self.更新状态(context, '指定贴图文件夹', ['搜索贴图文件夹', '使用模型路径'])
    )
    使用模型路径: BoolProperty(
        name="使用模型路径",
        description="mmd_tools导入的模型可以获取模型路径，可将贴图放在pmx模型位置，导入其中的贴图",
        default=False,
        # update=更新使用模型路径
        update=lambda self, context: self.更新状态(context, '使用模型路径', ['搜索贴图文件夹', '指定贴图文件夹'])
    )

    贴图文件夹: StringProperty(
        name="贴图文件夹",
        description="直接导入贴图的路径",
        subtype='DIR_PATH',
        # update=lambda self, context: None,
    )

    基础贴图快速匹配: BoolProperty(
        name="快速匹配",
        description="直接简单的匹配逻辑，耗时也少",
        default=True,
        # update=更新基础贴图快速匹配
        update=lambda self, context: self.更新状态(context, '基础贴图快速匹配', ['基础贴图精确匹配'])
    )
    基础贴图精确匹配: BoolProperty(
        name="精确匹配",
        description="针对从基础色分离出来的皮肤、金属、布料贴图，快速匹配可能不准确。精确匹配会显著增加运行时间（bpy无法使用多线程）",
        default=False,
        # update=更新基础贴图精确匹配
        update=lambda self, context: self.更新状态(context, '基础贴图精确匹配', ['基础贴图快速匹配'])
    )

    哈希尺寸: IntProperty(
        name="哈希尺寸",
        default=8,
        description = "图像感知哈希尺寸，越大图像匹配越准确，但会增加运行时间",
        subtype='PIXEL',
        min = 8,  # 最小值
        max = 32,  # 最大值
    )

    # 贴图名称严格匹配: BoolProperty(
    #     name="贴图名称严格匹配",
    #     description="严格按照“前缀_部件_贴图类型.文件扩展名”格式，通过基础贴图名称中的前缀（如Avatar_Kiana_C2_Texture）、部件（如Body）和文件扩展名（如.png）找到其他类型贴图（如LightMap）",
    #     default=True,
    #     update=更新贴图名称严格匹配
    # )
    #
    # 贴图名称宽松匹配: BoolProperty(
    #     name="贴图名称宽松匹配",
    #     description="只通过“部件“和”贴图类型”两个条件，通过基础贴图名称找到其他贴图。如丝柯克部分新贴图仍使用旧名，建议使用宽松匹配。绝区零必须严格匹配。",
    #     default=False,
    #     update=更新贴图名称宽松匹配
    # )

    通过alpha混合贴图: BoolProperty(
        name="通过alpha混合贴图",
        description="针对原始贴图和解包贴图的alpha不一致情况，通过原始贴图alpha混合贴图进行校正",
        default=False
    )

    通过alpha混合透明: BoolProperty(
        name="通过alpha混合透明",
        description="从基础色分离出来的皮肤、金属、布料贴图，需要通过alpha混合透明",
        default=False
    )

    # 1.1.0检测透明材质
    检测透明材质: BoolProperty(
        name="检测透明材质",
        description="默认只通过MMD的alpha（<1）判断透明。开启后进一步检测五官、头发、皮肤、衣服之中可能透明的材质的UV区域是否包含了贴图的透明像素(alpha<1)，如有则混合透明着色、混合材质模式。需要注意的是基础贴图的alpha通道不一定用于透明，也可能用于调整亮度。",
        default=False
    )
    检测透明分辨率: IntProperty(
        name="",
        default=512,
    )
    射线法检测透明: BoolProperty(
        name="射线法检测透明",
        description="使用射线法判断透明像素中心是否在材质面UV区域内。检测速度较快, 但是个别面可能检测不准确。建议对模型整体检测时使用。",
        default=True,
        update = lambda self, context: self.更新状态(context, '射线法检测透明', ['面积法检测透明'])
    )
    面积法检测透明: BoolProperty(
        name="面积法检测透明",
        description="使用面积法判断透明像素和材质面UV是否相交。检测速度较慢, 对材质面UV的像素检测更加准确。建议对单个材质检测时使用。",
        default=False,
        update=lambda self, context: self.更新状态(context, '面积法检测透明', ['射线法检测透明'])
    )

    连接基础贴图alpha: BoolProperty(
        name="连接alpha",
        description="点按自动更新连接状态，可能影响原神的神之眼亮度",
        default=True,
        update=lambda self, context: 更新基础贴图alpha连接(self, context),
    )

    通过点乘混合法向: BoolProperty(
        name="通过点乘混合法向",
        description="针对法向贴图方向相反情况，通过点乘混合法向进行校正",
        default=False,
        update=更新通过点乘混合法向
    )

    游戏列表: CollectionProperty(
        type=GameTemplateItem,
        name="游戏列表",
    )
    当前列表选项索引: IntProperty(
        name="",
        default=0,
    )

    # 定义每个模板的独立路径属性 # 不能使用中文冒号：
    崩坏三模板路径: StringProperty(name="崩坏三模板路径", description="设置崩坏三模板文件路径")
    原神模板路径: StringProperty(name="原神模板路径", description="设置原神模板文件路径")
    崩坏星穹铁道模板路径: StringProperty(name="崩坏：星穹铁道模板路径", description="设置崩坏：星穹铁道模板文件路径")
    绝区零模板路径: StringProperty(name="绝区零模板路径", description="设置绝区零模板文件路径")
    鸣潮模板路径: StringProperty(name="鸣潮模板路径", description="设置鸣潮模板文件路径")

    def 开启制作(self,layout):
        行 = layout.row()  # 1.0.3新增
        列 = 行.column()
        列.prop(self, "开启制作预设", text="  开启制作预设面板 需自备贴图和预设模板")
        列 = 行.column()
        列.operator("wulutuolaman.open_website_template_example", text="查看预设模板示范", icon='URL')  # 1.1.0新增
        行 = layout.row(align=True)
        行.label(text="可使用近期公开预设制作模板：崩坏三、原神、崩坏：星穹铁道", icon='CHECKMARK')
        行 = layout.row(align=True)
        行.label(text="注意预设模板不是预设！注意预设模板不是预设！注意预设模板不是预设！", icon='ERROR')
        行 = layout.row(align=True)
        行.label(text="建议熟悉着色节点、几何节点和小二节点结构，再使用制作预设功能", icon='ERROR')
        行 = layout.row(align=True)
        行.label(text="早期预设的节点组结构不同，无法适用", icon='ERROR')
        if self.开启制作预设:  # 1.0.3新增
            # layout.label(text="贴图目录设置")
            行 = layout.row(align=True)
            行.prop(self, "贴图目录", text="贴图目录", icon='FILE_IMAGE')
            行.scale_x = 0.5
            键 = 行.operator("xiaoer.set_image_path", text="选择贴图目录", icon='FILE_IMAGE')
            键.属性 = "贴图目录"  # 将路径属性名传递给操作符
            行 = layout.row(align=True)
            行.label(text="开启导入贴图后，插件代码会先匹配基础贴图，再通过基础贴图的名称找到其他贴图", icon='INFO')
            # 行 = layout.row(align=True)
            # 行.label(text="如果基础贴图和其他贴图名称不一致（如新版丝柯克的头发贴图），需要手动修改贴图名称", icon='ERROR')

            # 模板路径设置
            def 设置模板路径(游戏,操作):
                行 = layout.row(align=True)  # 关键点：align=True 确保子元素对齐
                左侧 = 行.split(factor=0.1)  # 分割行，左侧占10%宽度
                左侧.template_icon(icon_value=图标预览[游戏].icon_id, scale=2)  # 图标放在左侧
                右侧 = 左侧.column(align=True)  # 右侧子行
                路径 = f'{游戏.replace("：", "")}模板路径'  # 崩坏：星穹铁道变量名不能有冒号
                右侧.prop(bpy.context.preferences.addons["导入小二"].preferences, 路径, text=游戏, icon='BLENDER')
                键 = 右侧.operator(操作, icon='BLENDER')
                键.属性 = 路径  # 将路径属性名传递给操作符
            设置模板路径("崩坏三", "xiaoer.set_honkai3_path")
            设置模板路径("原神", "xiaoer.set_genshin_path")
            设置模板路径("崩坏：星穹铁道", "xiaoer.set_honkai_star_rail_path")
            设置模板路径("绝区零", "xiaoer.set_zenless_zone_zero_path")
            设置模板路径("鸣潮", "xiaoer.set_wuthering_waves_path")
