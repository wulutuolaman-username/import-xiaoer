# coding: utf-8

# import bpy
# import re
from .贴图.基础贴图 import 获取基础贴图
from .贴图.光照贴图 import 获取光照贴图
from .贴图.法线贴图 import 获取法线贴图
from .贴图节点组.光照贴图节点组 import 获取光照贴图节点组
from .贴图节点组.Ramp贴图节点组 import ramp节点组
from .贴图节点组.我的贴图节点组 import 我的贴图节点组
from .贴图节点组.重命名节点组 import 重命名节点组

# 材质处理
def 小二好色(self, 偏好, 数据来源, 材质, 匹配贴图, alpha贴图, 基础贴图匹配的节点组, 材质类型, 小二材质类型, 游戏):
    材质输出节点 = (材质.node_tree.nodes.get("材质输出") or 材质.node_tree.nodes.get("Material Output"))  # 找到材质输出节点
    # MMDShaderDev = material.node_tree.nodes["mmd_shader"]  # 设为透明需要在计算描边时删除该材质
    # if MMDShaderDev.inputs[12].default_value == 0:
    #     transparent_node = material.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')  # 新建透明节点
    #     transparent_node.location = (-200, 1600)  # 定位透明节点
    #     material.node_tree.links.new(
    #         transparent_node.outputs[0],  # 节点组的输出插槽
    #         output_node.inputs['Surface']  # 输出节点的输入插槽
    #     )
    #     self.report({"INFO"}, f'材质Material["{material.name}"]根据MMDShaderDev的alpha值为0设为透明"]')
    #     return  # 如果MMD节点组设置为透明，直接输出透明，然后进入下一个循环
    材质节点组 = 材质.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    for 节点组 in 数据来源.node_groups:  # 设置材质节点组
        if 节点组.type == 'SHADER' and (  # 搜索材质节点组
                节点组.name == f"{游戏}{材质类型}" or
                (小二材质类型 in 节点组.name and "小二" in 节点组.name)
        ):
            材质节点组.node_tree = 节点组  # 应用材质节点组
            材质节点组.location = (-200, 1500)  # 定位材质节点组
            材质.node_tree.links.new(
                材质节点组.outputs[0],  # 材质节点组的输出插槽
                材质输出节点.inputs['Surface']  # 材质输出节点的输入插槽
            )
            break  # 找到后立即退出循环，提高效率
    if 偏好.导入贴图:  # 如果开启了导入贴图
        图像节点,基础贴图 = 获取基础贴图(self, 材质, 匹配贴图)  # 基础贴图
        if not 基础贴图:
            # 如果没有匹配基础贴图，尝试根据材质分类指定基础贴图，出错概率较大
            if 材质类型 == "皮肤" or 材质类型 == "衣服":
                if 游戏 != "鸣潮":
                    基础贴图 = next((基础图 for 原始图,基础图 in 匹配贴图.items() if "Body" in 基础图.name), None)
                if 游戏 == "鸣潮":
                    基础贴图 = next((基础图 for 原始图,基础图 in 匹配贴图.items() if "Up" in 基础图.name), None)
            elif 材质类型 == "头发":
                基础贴图 = next((基础图 for 原始图,基础图 in 匹配贴图.items() if "Hair" in 基础图.name), None)
            else:  # 如果没有检索到材质的匹配贴图，材质节点组连接原始贴图
                材质.node_tree.links.new(
                    图像节点.outputs[0],  # 节点的输出插槽
                    材质节点组.inputs[0]  # 节点组的输入插槽
                )
        if 基础贴图:  # 如果检索到材质的匹配贴图
            if 材质节点组.node_tree.name == f"{游戏}{材质类型}":  # 如果是我的中文名节点组模板
                我的贴图节点组(self, 数据来源, 材质, 材质节点组, 游戏, 基础贴图, 基础贴图匹配的节点组, 材质类型, alpha贴图)
            elif "小二" in 材质节点组.node_tree.name:  # 小二的英文名节点组模板
                # self.report({"INFO"}, f'小二')
                if 基础贴图:  # 如果材质查找到匹配贴图
                    图像节点 = 材质.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
                    图像节点.image = 基础贴图  # 应用贴图
                    if alpha贴图 and 基础贴图 in alpha贴图:
                        图像节点.image.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
                    self.report({"INFO"}, f'材质Material["{材质.name}"]输入基础贴图:Texture["{基础贴图.name}"]')
                    图像节点.location = (-500, 1500)  # 定位图像节点
                    # 光照贴图
                    光照贴图节点组 = None  # 初始化
                    if 基础贴图 in 基础贴图匹配的节点组:  # 检查贴图和材质节点组的使用情况
                        材质节点组.node_tree = 基础贴图匹配的节点组[基础贴图]  # 字典匹配
                        # self.report({"INFO"},f'材质Material["{material.name}"]应用材质节点组:ShaderNodeNodeTree["{材质节点组.node_tree.name}"]')
                        光照贴图节点组 = 获取光照贴图节点组(游戏, 材质节点组) # 找到ligthmap节点组
                        # self.report({"INFO"}, f'材质Material["{material.name}"]应用光照贴图节点组{光照贴图节点组.node_tree.name}')
                    elif 基础贴图 not in 基础贴图匹配的节点组 and 材质节点组.node_tree.users == 1:
                        # self.report({"INFO"},f'材质Material["{material.name}"]应用节点组:ShaderNodeNodeTree["{材质节点组.node_tree.name}"]')
                        基础贴图匹配的节点组[基础贴图] = 材质节点组.node_tree  # 存储贴图和材质节点组对应信息
                        光照贴图节点组 = 获取光照贴图节点组(游戏, 材质节点组) # 找到ligthmap节点组
                        self.report({"INFO"},f'材质Material["{材质.name}"]第一个应用光照贴图节点组{光照贴图节点组.node_tree.name}')
                    elif 基础贴图 not in 基础贴图匹配的节点组 and 材质节点组.node_tree.users > 1:
                        材质节点组.node_tree = 材质节点组.node_tree.copy()  # 应用节点组副本
                        重命名节点组(self, 材质节点组.node_tree)  # 重命名材质节点组副本
                        self.report({"INFO"},f'材质Material["{材质.name}"]创建材质节点组副本:ShaderNodeNodeTree["{材质节点组.node_tree.name}"]')
                        基础贴图匹配的节点组[基础贴图] = 材质节点组.node_tree  # 存储贴图和材质节点组对应信息
                        光照贴图节点组 = 获取光照贴图节点组(游戏, 材质节点组)  # 找到ligthmap节点组
                        光照贴图节点组.node_tree = 光照贴图节点组.node_tree.copy()  # 应用节点组副本
                        重命名节点组(self, 光照贴图节点组.node_tree)  # 重命名光照贴图节点组副本
                        self.report({"INFO"}, f'材质Material["{材质.name}"创建光照贴图节点组副本{光照贴图节点组.node_tree.name}')
                    光照贴图节点 = next((node for node in 光照贴图节点组.node_tree.nodes if node.type == 'TEX_IMAGE'),None)  # 找到ligthmap贴图节点
                    光照贴图 = 获取光照贴图(游戏, 基础贴图)
                    if 光照贴图:
                        光照贴图节点.image = 光照贴图  # 应用光照贴图
                        self.report({"INFO"}, f'材质Material["{材质.name}"]输入光照贴图:Texture["{光照贴图.name}"]')
                        光照贴图.colorspace_settings.name = 'Non-Color'  # 非彩色
                    # 法线贴图
                    法线贴图 = 获取法线贴图(游戏, 基础贴图)
                    # self.report({"INFO"}, f'材质Material["{material.name}"]调试法线贴图["{法线贴图}"]')
                    if 法线贴图:
                        法线贴图节点 = 材质.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
                        法线贴图节点.image = 法线贴图  # 应用法线贴图
                        self.report({"INFO"},f'材质Material["{材质.name}"]输入法线贴图:Texture["{法线贴图.name}"]')
                        法线贴图节点.location = (-500, 1000)
                        法线贴图.colorspace_settings.name = 'Non-Color'  # 非彩色
                        材质.node_tree.links.new(  # 法线贴图颜色
                            法线贴图节点.outputs[0],  # 图像节点的输出插槽
                            材质节点组.inputs[2]  # 输出节点的输入插槽
                        )
                    # Ramp贴图
                    ramp节点组(self, 游戏, 材质, 材质节点组, 基础贴图)
                    # 节点相连
                    材质.node_tree.links.new(  # 基础贴图颜色
                        图像节点.outputs[0],  # 图像节点的输出插槽
                        材质节点组.inputs[0]  # 输出节点的输入插槽
                    )
                    if len(材质节点组.inputs) > 1 and "Alpha" in 材质节点组.inputs[1].name:
                        材质.node_tree.links.new(  # 基础贴图Alpha
                            图像节点.outputs[1],  # 图像节点的输出插槽
                            材质节点组.inputs[1]  # 输出节点的输入插槽
                        )
                # else:
                #     self.report({"WARNING"}, f'材质Material["{材质.name}"]未找到匹配的基础贴图')
                #     if 图像节点:  # 薇塔的眼睛2材质没有基础贴图
                #         材质.node_tree.links.new(
                #             图像节点.outputs[0],  # 图像节点的输出插槽
                #             材质节点组.inputs[0]  # 输出节点的输入插槽
                #         )