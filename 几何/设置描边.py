import bpy
from .几何节点 import 几何节点
from .输入材质 import 输入材质
from .打包材质 import 打包材质
from ..通用.信息 import 报告信息
from ..着色.贴图.空白贴图 import 获取空白贴图

def 分类设置描边(self, 一级节点组, 五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质):
    已输入头发材质 = False
    已输入皮肤材质 = False
    for 二级节点 in 一级节点组.nodes:
        # if 二级节点.type != 'GROUP':  # 确保节点不是节点数里的节点组，后续能够正确访问名称属性
        if 二级节点.type == "DELETE_GEOMETRY":
            报告信息(self, '正常', f"无描边材质 删除几何体")
            输入材质(self, 二级节点, 五官材质 + 表情材质 + 透明材质)
            continue
        if 二级节点.type == "SET_MATERIAL":
            # self.report({"INFO"}, f"设置材质节点名称:"+str(node_level_2))
            # AttributeError: 'GeometryNodeSetMaterial' object has no attribute 'material'
            材质接口 = 二级节点.inputs[2]
            if 材质接口 and 材质接口.default_value:
                # self.report({"INFO"}, f"接口:" + str(input_socket))
                描边材质 = 材质接口.default_value  # 找到描边材质，根据描边材质名称输入模型材质
                报告信息(self, '正常', f"描边材质 {描边材质.name}")
                if "头发" in 描边材质.name or "hair" in 描边材质.name:
                    输入材质(self, 二级节点, 头发材质)
                    已输入头发材质 = True
                    continue
                if "皮肤" in 描边材质.name or "skin" in 描边材质.name:
                    输入材质(self, 二级节点, 脸部材质 + 皮肤材质)
                    已输入皮肤材质 = True
                    continue
                if 已输入头发材质 and 已输入皮肤材质:
                    break  # 如果材质都已输入，提前结束循环for node_level_2 in node_level_1.nodes:

def 设置描边(self, 模型, 节点组列表, 五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质):
    for 材质 in 模型.data.materials:
        if 材质.小二预设模板.透明材质 == True and 材质 not in 透明材质 and 材质.小二预设模板.材质分类 != "脸部":  # 颜+
            透明材质.append(材质)
    for 节点组 in 节点组列表:
        # self.report({"INFO"}, f"正在遍历:" + str(node_group))
        if 节点组.type == 'GEOMETRY' and (节点组.小二预设模板.应用修改器 or 节点组.users == 0+1):  # 未被使用的几何节点组
            几何节点(模型, 节点组)  # 应用几何节点
        # 设置描边材质
        if 节点组.type == 'GEOMETRY' and "实体化描边" in 节点组.name:
            一级节点组 = 节点组
            # self.report({"INFO"}, f"找到了:"+str(node_level_1))
            打包材质(self, 节点组, 衣服材质)  # 打包衣服材质
            分类设置描边(self, 一级节点组, 五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质)
        # 根据脸描边遮罩设置脸材质
        elif 节点组.type == 'GEOMETRY' and "描边权重" in 节点组.name:
            二级节点 = 节点组
            # self.report({"INFO"}, f"描边权重:" + str(node_group))
            for 图像节点 in 二级节点.nodes:
                if 图像节点.type == "IMAGE_TEXTURE":  # 查找图像纹理节点:
                    图像接口 = 图像节点.inputs[0]
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
                                                        if 材质选择节点 and 材质选择节点.type == 'MATERIAL_SELECTION':
                                                            材质接口 = 材质选择节点.inputs[0]
                                                            if 材质接口:
                                                                材质接口.default_value = 脸
                                                                self.report({"INFO"},f'设置脸描边遮罩["{描边遮罩.name}"]脸材质["{脸.name}"]')
                                                else:
                                                    # 如果切换节点没有连接布尔接口，创建材质选择节点
                                                    材质选择节点 = 二级节点.nodes.new(type='GeometryNodeMaterialSelection')
                                                    材质选择节点.location = (360, 360)  # 设置节点位置
                                                    材质接口 = 材质选择节点.inputs[0]
                                                    材质接口.default_value = 脸
                                                    输出 = 材质选择节点.outputs['Selection']
                                                    二级节点.links.new(输出, 输入)  # 创建连接
                                                break
                    elif 图像接口 and not 图像接口.default_value:
                        描边遮罩 = 获取空白贴图("小二插件：空白描边遮罩", 1024)
                        图像接口.default_value = 描边遮罩  # 应用描边遮罩