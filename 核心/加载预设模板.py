# coding: utf-8

import bpy
from ..通用.设置 import 渲染设置
from ..图像.导入匹配 import 导入匹配
from ..材质.材质分类 import 材质分类
from ..着色.脸部着色 import 脸部着色
from ..着色.眼口着色 import 眼口着色
from ..着色.表情着色 import 表情着色
from ..着色.小二着色 import 小二好色
from ..着色.混合.混合法向 import 混合法向
from ..几何.设置描边 import 设置描边
from ..通用.绑定 import 绑定

def 干翻小二(self, 偏好, 模型, 游戏, 文件路径, 贴图路径):
    # 设置辉光属性和色彩管理
    渲染设置()

    # 追加预设文件的所有资产
    self.report({"INFO"}, f"开始加载预设模板" + str(文件路径) + r"=================================================")
    with bpy.data.libraries.load(文件路径) as (数据源, 数据流):
        # 仅加载物体、材质和节点组
        数据流.objects = 数据源.objects
        数据流.materials = 数据源.materials
        数据流.node_groups = 数据源.node_groups

    # 计算贴图哈希和导入贴图，鸣潮可根据名称直接匹配无需哈希
    匹配贴图 = None
    alpha贴图 = None
    if 偏好.导入贴图:  # 如果开启了导入贴图
        匹配贴图,alpha贴图 = 导入匹配(self, 偏好, 模型, 贴图路径)

    # 材质按名称分组，不一定分对
    眼口材质, 表情材质, 头发材质, 脸, 脸材质, 皮肤材质, 衣服材质 = 材质分类(模型)
    self.report({"INFO"}, f"材质按名称分组结果----------------------------------------------------------------------------------")
    self.report({"INFO"}, f"眉、睫、眼、口、舌、齿等材质分组: " + " ".join(材质.name for 材质 in 眼口材质))
    self.report({"INFO"}, f"表情材质分组: " + " ".join(材质.name for 材质 in 表情材质))
    self.report({"INFO"}, f"头发材质分组: " + " ".join(材质.name for 材质 in 头发材质))
    # self.report({"INFO"}, f"脸材质: " + str(face_材质.name))
    self.report({"INFO"}, f"脸材质分组: " + " ".join(材质.name for 材质 in 脸材质))
    self.report({"INFO"}, f"皮肤材质分组: " + " ".join(材质.name for 材质 in 皮肤材质))
    self.report({"INFO"}, f"衣服材质分组: " + " ".join(材质.name for 材质 in 衣服材质))

    # 1.0.9先处理材质着色器，再处理几何节点组

    # 处理材质着色器
    self.report({"INFO"}, f"处理材质着色器-------------------------------------------------------------------------------------------")
    基础贴图匹配的节点组 = {}  # 记录基础贴图和节点组的对应信息
    透明材质 = []  # 1.0.9检测透明材质
    self.report({"INFO"}, f'脸材质')
    for 材质 in 脸材质:  # 脸材质
        脸部着色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图)
    self.report({"INFO"}, f'眉、睫、眼、口、舌、齿等材质')
    for 材质 in 眼口材质:  # 眉、睫、眼、口、舌、齿等材质
        眼口着色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图)
    self.report({"INFO"}, f'表情材质')
    for 材质 in 表情材质:
        材质.blend_method = 'BLEND'  # 材质模式
        # material.show_transparent_back = False  # 不显示背面
        表情着色(self, 偏好, 数据源, 材质, 匹配贴图)
    self.report({"INFO"}, f'头发材质')
    for 材质 in 头发材质:
        小二好色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图, 基础贴图匹配的节点组, "头发", "hair", 游戏, 透明材质)
    self.report({"INFO"}, f'皮肤材质')
    for 材质 in 皮肤材质:
        小二好色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图, 基础贴图匹配的节点组, "皮肤", "clothes", 游戏, 透明材质)
    self.report({"INFO"}, f'衣服材质')
    for 材质 in 衣服材质:
        小二好色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图, 基础贴图匹配的节点组, "衣服", "clothes", 游戏, 透明材质)

    # 1.0.10通过点乘混合法向
    混合法向(self, 偏好)

    # 处理几何节点组
    self.report({"INFO"}, f"处理几何节点组------------------------------------------------------------------------------------------")
    设置描边(self, 模型, 数据源, 眼口材质, 表情材质, 头发材质, 脸, 脸材质, 皮肤材质, 衣服材质, 透明材质)

    # 追加物体移入选中网格的集合
    if 模型.users_collection:  # 检查选中模型是否在集合中
        for 物 in 数据源.objects:
            模型.users_collection[0].objects.link(物)  # 将驱动物体移入新集合

    # 绑定头骨
    绑定(偏好, 模型, self)

