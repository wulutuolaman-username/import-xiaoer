# coding: utf-8

import bpy
from ..通用.设置 import 渲染设置
from ..图像.导入匹配 import 导入匹配
from ..材质.材质分类 import 材质分类
from ..几何.几何节点 import 几何节点
from ..几何.输入材质 import 输入材质
from ..几何.打包材质 import 打包材质
from ..着色.脸部着色 import 脸部着色
from ..着色.眼口着色 import 眼口着色
from ..着色.表情着色 import 表情着色
from ..着色.小二着色 import 小二好色
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

    # 处理几何节点组
    self.report({"INFO"}, f"处理几何节点组------------------------------------------------------------------------------------------")
    for 节点组 in 数据源.node_groups:
        # self.report({"INFO"}, f"正在遍历:" + str(node_group))
        if 节点组.type == 'GEOMETRY' and 节点组.users == 0:  # 未被使用的几何节点组
            几何节点(模型, 节点组)  # 应用几何节点
        # 设置描边材质
        if 节点组.type == 'GEOMETRY' and "实体化描边" in 节点组.name:
            一级节点组 = 节点组
            # self.report({"INFO"}, f"找到了:"+str(node_level_1))
            打包材质(节点组, 衣服材质)  # 打包衣服材质
            已输入头发材质 = False
            已输入皮肤材质 = False
            for 二级节点 in 一级节点组.nodes:
                if 二级节点.type != 'GROUP':  # 确保节点不是节点数里的节点组，后续能够正确访问名称属性
                    if any(二级节点.name.startswith(suffix) for suffix in ["删除几何体", "Delete Geometry"]):
                        self.report({"INFO"}, f"无描边材质 删除几何体")
                        输入材质(self, 二级节点, 眼口材质)
                        输入材质(self, 二级节点, 表情材质)
                        continue
                    if any(二级节点.name.startswith(suffix) for suffix in ["设置材质", "Set Material"]):
                        # self.report({"INFO"}, f"设置材质节点名称:"+str(node_level_2))
                        设置材质节点 = 二级节点
                        # AttributeError: 'GeometryNodeSetMaterial' object has no attribute 'material'
                        材质接口 = next((s for s in 设置材质节点.inputs if s.name == 'Material'), None)
                        if 材质接口 and 材质接口.default_value:
                            # self.report({"INFO"}, f"接口:" + str(input_socket))
                            描边材质 = 材质接口.default_value  # 找到描边材质，根据描边材质名称输入模型材质
                            if "头发" in 描边材质.name or "hair" in 描边材质.name:
                                self.report({"INFO"}, f"描边材质 " + str(描边材质.name))
                                输入材质(self, 二级节点, 头发材质)
                                已输入头发材质 = True
                                continue
                            if "皮肤" in 描边材质.name or "skin" in 描边材质.name:
                                self.report({"INFO"}, f"描边材质 " + str(描边材质.name))
                                输入材质(self, 二级节点, 脸材质)
                                输入材质(self, 二级节点, 皮肤材质)
                                已输入皮肤材质 = True
                                continue
                            if 已输入头发材质 and 已输入皮肤材质:
                                break  # 如果材质都已输入，提前结束循环for node_level_2 in node_level_1.nodes:
        # 根据脸描边遮罩设置脸材质
        elif 节点组.type == 'GEOMETRY' and "描边权重" in 节点组.name:
            二级节点 = 节点组
            # self.report({"INFO"}, f"描边权重:" + str(node_group))
            for 图像节点 in 二级节点.nodes:
                if 图像节点.name.startswith("Image Texture"):  # 查找图像纹理节点:
                    图像接口 = next((s for s in 图像节点.inputs if s.name == 'Image'), None)
                    # self.report({"INFO"}, f"找到描边遮罩:" + str(input_socket.default_value))
                    if 图像接口 and 图像接口.default_value:
                        # self.report({"INFO"}, f"图像接口:" + str(input_socket))
                        描边遮罩 = 图像接口.default_value
                        if "face" or "脸" in 描边遮罩.name:
                            # self.report({"INFO"}, f"找到脸描边遮罩")
                            for 输出 in 图像节点.outputs:
                                if 输出.is_linked:
                                    for link in 输出.links:
                                        切换节点 = link.to_node
                                        # self.report({"INFO"}, f"切换节点"+str(switch_node))
                                        for 输入 in 切换节点.inputs:
                                            if 输入.type == 'BOOLEAN':
                                                if 输入.is_linked:
                                                    for link in 输入.links:
                                                        材质选择节点 = link.from_node
                                                        if 材质选择节点:
                                                            材质接口 = next((s for s in 材质选择节点.inputs if s.name == 'Material'),None)
                                                            if 材质接口:
                                                                材质接口.default_value = 脸
                                                                self.report({"INFO"},f'设置脸描边遮罩["{描边遮罩.name}"]脸材质["{脸.name}"]')
                                                else:
                                                    # 如果切换节点没有连接布尔接口，创建材质选择节点
                                                    材质选择节点 = 二级节点.nodes.new(type='GeometryNodeMaterialSelection')
                                                    材质选择节点.location = (360, 360)  # 设置节点位置
                                                    材质输入 = next((s for s in 材质选择节点.inputs if s.name == 'Material'),None)
                                                    材质输入.default_value = 脸
                                                    输出 = 材质选择节点.outputs['Selection']
                                                    二级节点.links.new(输出, 输入)  # 创建连接

    # 处理材质
    self.report({"INFO"}, f"处理材质着色器-------------------------------------------------------------------------------------------")
    基础贴图匹配的节点组 = {}  # 记录基础贴图和节点组的对应信息
    self.report({"INFO"}, f'脸材质')
    for 材质 in 脸材质:  # 脸材质
        脸部着色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图)
    self.report({"INFO"}, f'眉、睫、眼、口、舌、齿等材质')
    for 材质 in 眼口材质:  # 眉、睫、眼、口、舌、齿等材质
        眼口着色(self, 偏好, 数据源, 材质, 匹配贴图)
    self.report({"INFO"}, f'表情材质')
    for 材质 in 表情材质:
        材质.blend_method = 'BLEND'  # 材质模式
        # material.show_transparent_back = False  # 不显示背面
        表情着色(self, 偏好, 数据源, 材质, 匹配贴图)
    self.report({"INFO"}, f'头发材质')
    for 材质 in 头发材质:
        小二好色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图, 基础贴图匹配的节点组, "头发", "hair", 游戏)
    self.report({"INFO"}, f'皮肤材质')
    for 材质 in 皮肤材质:
        小二好色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图, 基础贴图匹配的节点组, "皮肤", "clothes", 游戏)
    self.report({"INFO"}, f'衣服材质')
    for 材质 in 衣服材质:
        小二好色(self, 偏好, 数据源, 材质, 匹配贴图, alpha贴图, 基础贴图匹配的节点组, "衣服", "clothes", 游戏)

    # 追加物体移入选中网格的集合
    if 模型.users_collection:  # 检查选中模型是否在集合中
        for 物 in 数据源.objects:
            模型.users_collection[0].objects.link(物)  # 将驱动物体移入新集合

    # 绑定头骨
    绑定(偏好, 模型)

