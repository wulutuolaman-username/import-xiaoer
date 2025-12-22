import bpy
from .更新状态 import 更新基础贴图alpha连接
from ..列表 import GameTemplateItem
from ..图标 import 加载图标
图标预览 = 加载图标()

class XiaoerAddonOpenMakingAssets:

    开启制作预设: bpy.props.BoolProperty(
        name="开启制作预设",
        description="开启后激活制作预设面板",
        default=True
    )  # 1.0.3新增

    贴图目录: bpy.props.StringProperty(
        name="贴图目录",
        description="设置贴图文件的搜索根目录",
        # subtype='DIR_PATH',
        # update=lambda self, context: None,
    )

    导入贴图: bpy.props.BoolProperty(
        name="导入贴图",
        description="先在偏好设置中设置包含贴图文件的目录，开启后可以导入贴图",
        default=True
    )
    贴图来源: bpy.props.EnumProperty(  # 1.1.2改为枚举属性
        name="材质分类",
        description="材质分类结果，可修改类型重新查找节点组",
        items=[
        ('搜索', "搜索贴图", "先在偏好设置中设置包含所有贴图文件的目录，开启后可以根据模型名称和贴图文件夹名称，搜索模型对应的贴图所在文件夹，关闭后需要直接指定模型贴图所在文件夹"),
        ('指定', "指定路径", "临时指定的贴图文件夹，直接导入其中的贴图"),
        ('模型', "模型路径", "mmd_tools导入的模型可以获取模型路径，可将贴图放在pmx模型位置，导入其中的贴图"),
        ],
        default='指定',
    )

    贴图文件夹: bpy.props.StringProperty(
        name="贴图文件夹",
        description="直接导入贴图的路径",
        subtype='DIR_PATH',
    )

    # 1.1.0检测透明材质
    检测透明材质: bpy.props.BoolProperty(
        name="检测透明材质",
        description="默认只通过MMD的alpha（<1）判断透明。开启后进一步检测五官、头发、皮肤、衣服之中可能透明的材质的UV区域是否包含了贴图的透明像素(alpha<1)，如有则混合透明着色。需要注意的是基础贴图的alpha通道不一定用于透明，也可能用于调整亮度。",
        default=False
    )
    检测透明分辨率: bpy.props.IntProperty(
        name="",
        default=512,
    )
    检测方式: bpy.props.EnumProperty(  # 1.1.2改为枚举属性
        name="材质分类",
        description="材质分类结果，可修改类型重新查找节点组",
        items=[
        ('射线', "射线法", "使用射线法判断透明像素中心是否在材质面UV区域内。检测速度较快, 对单个材质检测结果与面积法基本相同，但是个别面可能检测不如面积法准确。建议对模型整体检测时使用。", "ORIENTATION_LOCAL", 0),
        ('面积', "面积法", "使用面积法断透明像素和材质面UV是否相交。检测速度较慢, 对单个材质检测结果与射线法基本相同, 对材质面UV的像素区域检测更加准确。建议对单个材质检测时使用。", "OVERLAY", 1),
        ],
        default='射线',
    )

    连接基础贴图alpha: bpy.props.BoolProperty(
        name="连接alpha",
        description="点按自动更新连接状态，可能影响原神的神之眼亮度",
        default=True,
        update=lambda self, context: 更新基础贴图alpha连接(self, context),
    )

    游戏列表: bpy.props.CollectionProperty(
        type=GameTemplateItem,
        name="游戏列表",
    )
    当前列表选项索引: bpy.props.IntProperty(
        name="",
        default=0,
    )

    # 定义每个模板的独立路径属性 # 不能使用中文冒号：
    崩坏三模板路径: bpy.props.StringProperty(name="崩坏三模板路径", description="设置崩坏三模板文件路径")
    原神模板路径: bpy.props.StringProperty(name="原神模板路径", description="设置原神模板文件路径")
    崩坏星穹铁道模板路径: bpy.props.StringProperty(name="崩坏：星穹铁道模板路径", description="设置崩坏：星穹铁道模板文件路径")
    绝区零模板路径: bpy.props.StringProperty(name="绝区零模板路径", description="设置绝区零模板文件路径")
    鸣潮模板路径: bpy.props.StringProperty(name="鸣潮模板路径", description="设置鸣潮模板文件路径")

    def 开启制作(self, 布局):
        行 = 布局.row()  # 1.0.3新增
        列 = 行.column()
        列.prop(self, "开启制作预设", text="  开启制作预设面板 需自备贴图和预设模板")
        列 = 行.column()
        列.operator("wulutuolaman.open_website_template_example", text="查看预设模板示范", icon='URL')  # 1.1.0新增
        行 = 布局.row(align=True)
        行.label(text="可使用近期公开预设制作模板：崩坏三、原神、崩坏：星穹铁道", icon='CHECKMARK')
        行 = 布局.row(align=True)
        行.alert = True
        行.label(text="注意预设模板不是预设！注意预设模板不是预设！注意预设模板不是预设！", icon='ERROR')
        行 = 布局.row(align=True)
        行.label(text="建议熟悉着色节点、几何节点和小二节点结构，再使用制作预设功能", icon='ERROR')
        行 = 布局.row(align=True)
        行.label(text="早期预设的节点组结构不同，无法适用", icon='ERROR')
        if self.开启制作预设:  # 1.0.3新增
            # layout.label(text="贴图目录设置")
            行 = 布局.row(align=True)
            行.prop(self, "贴图目录", text="贴图目录", icon='FILE_IMAGE')
            行.scale_x = 0.5
            键 = 行.operator("xiaoer.set_image_path", text="选择贴图目录", icon='FILE_IMAGE')
            键.属性 = "贴图目录"  # 将路径属性名传递给操作符
            行 = 布局.row(align=True)
            行.label(text="开启导入贴图后，插件代码会先匹配基础贴图，再通过基础贴图的名称找到其他贴图", icon='INFO')
            # 行 = layout.row(align=True)
            # 行.label(text="如果基础贴图和其他贴图名称不一致（如新版丝柯克的头发贴图），需要手动修改贴图名称", icon='ERROR')

            # 模板路径设置
            def 设置模板路径(游戏, 操作):
                from ..偏好.获取偏好 import 获取偏好
                行 = 布局.row(align=True)  # 关键点：align=True 确保子元素对齐
                左侧 = 行.split(factor=0.1)  # 分割行，左侧占10%宽度
                左侧.template_icon(icon_value=图标预览[游戏].icon_id, scale=2)  # 图标放在左侧
                右侧 = 左侧.column(align=True)  # 右侧子行
                路径 = f'{游戏.replace("：", "")}模板路径'  # 崩坏：星穹铁道变量名不能有冒号
                右侧.prop(获取偏好(), 路径, text=游戏, icon='BLENDER')
                键 = 右侧.operator(操作, icon='BLENDER')
                键.属性 = 路径  # 将路径属性名传递给操作符
            设置模板路径("崩坏三", "xiaoer.set_honkai3_path")
            设置模板路径("原神", "xiaoer.set_genshin_path")
            设置模板路径("崩坏：星穹铁道", "xiaoer.set_honkai_star_rail_path")
            设置模板路径("绝区零", "xiaoer.set_zenless_zone_zero_path")
            设置模板路径("鸣潮", "xiaoer.set_wuthering_waves_path")
