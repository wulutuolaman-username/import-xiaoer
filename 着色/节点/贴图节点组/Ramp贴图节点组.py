import bpy  # noqa: F401
from ...贴图.Ramp贴图 import 获取Ramp贴图
from ...贴图.空白贴图 import 获取空白贴图
from ....通用.编号 import 节点组编号
from ....通用.信息 import 报告信息
from ..判断类型 import *

# 1.1.0解决多个部件ramp问题
def ramp节点组(self:bpy.types.Operator, 游戏, 材质, 材质节点组, 基础贴图, 多部件, 记录次数):
###################################################################################################
    if 游戏 == "原神":
        Ramp贴图 = 获取Ramp贴图(self, 游戏, 基础贴图)
        Ramp材质节点组 = next((节点 for 节点 in 材质节点组.node_tree.nodes if 是群组(节点) and 节点.node_tree.name.startswith("ramp.")), None)
        Ramp贴图节点组 = next((节点 for 节点 in Ramp材质节点组.node_tree.nodes if 是群组(节点) and 节点.node_tree.name.startswith("ramptex.")), None)
        Ramp节点 = next((节点 for 节点 in Ramp贴图节点组.node_tree.nodes if 是图像(节点)), None)  # 找到ramp贴图节点
        # 报告信息(self, '正常', f'材质Material["{材质.name}"]Ramp贴图["{Ramp贴图.name}"]使用次数{Ramp贴图.users}, 记录次数{记录次数}')
        if Ramp贴图 and Ramp贴图.users == 0 + 记录次数:  # 1.1.0记录贴图
            if 多部件:  # 1.1.0解决一种材质类型多个部件ramp贴图（如丝柯克）
                Ramp材质节点组.node_tree = Ramp材质节点组.node_tree.copy()  # 应用节点组副本
                节点组编号(self, Ramp材质节点组.node_tree)  # 重命名材质节点组副本
                报告信息(self, '正常', f'材质Material["{材质.name}"]创建Ramp材质节点组副本:ShaderNodeNodeTree["{Ramp材质节点组.node_tree.name}"]')
                Ramp贴图节点组 = next((节点 for 节点 in Ramp材质节点组.node_tree.nodes if 是群组(节点) and 节点.node_tree.name.startswith("ramptex.")), None)
                Ramp贴图节点组.node_tree = Ramp贴图节点组.node_tree.copy()  # 应用节点组副本
                节点组编号(self, Ramp贴图节点组.node_tree)  # 重命名材质节点组副本
                报告信息(self, '正常', f'材质Material["{材质.name}"]创建Ramp贴图节点组副本:ShaderNodeNodeTree["{Ramp贴图节点组.node_tree.name}"]')
            Ramp节点 = next((节点 for 节点 in Ramp贴图节点组.node_tree.nodes if 是图像(节点)), None)  # 找到ramp贴图节点
            Ramp节点.image = Ramp贴图
            报告信息(self, '正常', f'材质Material["{材质.name}"]输入Ramp贴图:Texture["{Ramp贴图.name}"]')
        elif not Ramp贴图 and not Ramp节点.image:
            报告信息(self, '异常', f'材质Material["{材质.name}"]的基础贴图["{基础贴图.name}"]未找到Ramp贴图')
            # 1.1.0没有找到Ramp贴图贴图，新建空白图像
            Ramp贴图 = 获取空白贴图("小二插件：未找到Ramp贴图")
            Ramp节点.image = Ramp贴图  # 应用Ramp贴图贴图
###################################################################################################
    if 游戏 == "崩坏：星穹铁道":
        冷Ramp, 暖Ramp = 获取Ramp贴图(self, 游戏, 基础贴图)
        # self.report({"INFO"}, f'记录次数{记录次数}')
        # if 冷Ramp:
        #     self.report({"INFO"},f'材质Material["{材质.name}"]Ramp贴图["{冷Ramp.name}"]使用次数{冷Ramp.users}')
        # if 暖Ramp:
        #     self.report({"INFO"},f'材质Material["{材质.name}"]Ramp贴图["{暖Ramp.name}"]使用次数{暖Ramp.users}')
        Ramp贴图 = [暖Ramp,冷Ramp]
        Ramp节点组 = next((节点 for 节点 in 材质节点组.node_tree.nodes if 是群组(节点) and 节点.node_tree.name.startswith("ramp")), None)
        # if 多部件:  # 1.1.0解决一种材质类型多个部件ramp贴图（如丝柯克）
        #     Ramp节点组.node_tree = Ramp节点组.node_tree.copy()  # 应用节点组副本
        #     节点组编号(self, Ramp节点组.node_tree)  # 重命名材质节点组副本
        #     self.report({"INFO"},f'材质Material["{材质.name}"]创建Ramp节点组副本:ShaderNodeNodeTree["{Ramp节点组.node_tree.name}"]')
        贴图节点 = next((节点 for 节点 in Ramp节点组.node_tree.nodes if 是图像(节点)), None)
        Ramp贴图节点 = []
        if 贴图节点:  # 找到ramp贴图节点
            for Ramp节点 in sorted(Ramp节点组.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 从上到下
                if 是图像(Ramp节点):
                    Ramp贴图节点.append(Ramp节点)
        else:  # 头发和衣服ramp贴图节点位置不同
            Ramp贴图节点组 = next((节点 for 节点 in Ramp节点组.node_tree.nodes if 是群组(节点) and 节点.node_tree.name.startswith("ramp")), None)
            # if 多部件:  # 1.1.0解决一种材质类型多个部件ramp贴图（如丝柯克）
            #     Ramp贴图节点组.node_tree = Ramp贴图节点组.node_tree.copy()  # 应用节点组副本
            #     节点组编号(self, Ramp贴图节点组.node_tree)  # 重命名材质节点组副本
            #     self.report({"INFO"},f'材质Material["{材质.name}"]创建Ramp贴图节点组副本:ShaderNodeNodeTree["{Ramp贴图节点组.node_tree.name}"]')
            for Ramp节点 in sorted(Ramp贴图节点组.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 从上到下
                if 是图像(Ramp节点):
                    Ramp贴图节点.append(Ramp节点)
        for 节点 in Ramp贴图节点:
            if 节点.image:
                return # 已有ramp贴图
        # TODO:检查材质分类是否为头发或皮肤、衣服
        if (冷Ramp and 冷Ramp.users == 0 + 记录次数) or (暖Ramp and 暖Ramp.users == 0 + 记录次数):  # 1.1.0记录贴图
            if 多部件:  # 1.1.0解决一种材质类型多个部件ramp贴图（如丝柯克）
                Ramp节点组.node_tree = Ramp节点组.node_tree.copy()  # 应用节点组副本
                节点组编号(self, Ramp节点组.node_tree)  # 重命名材质节点组副本
                报告信息(self, '正常', f'材质Material["{材质.name}"]创建Ramp节点组副本:ShaderNodeNodeTree["{Ramp节点组.node_tree.name}"]')
                贴图节点 = next((节点 for 节点 in Ramp节点组.node_tree.nodes if 是图像(节点)), None)
                Ramp贴图节点 = []
                if 贴图节点:  # 找到ramp贴图节点
                    for Ramp节点 in sorted(Ramp节点组.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 从上到下
                        if 是图像(Ramp节点):
                            Ramp贴图节点.append(Ramp节点)
                else:  # 头发和衣服ramp贴图节点位置不同
                    Ramp贴图节点组 = next((节点 for 节点 in Ramp节点组.node_tree.nodes if 是群组(节点) and 节点.node_tree.name.startswith("ramp")), None)
                    Ramp贴图节点组.node_tree = Ramp贴图节点组.node_tree.copy()  # 应用节点组副本
                    节点组编号(self, Ramp贴图节点组.node_tree)  # 重命名材质节点组副本
                    报告信息(self, '正常', f'材质Material["{材质.name}"]创建Ramp贴图节点组副本:ShaderNodeNodeTree["{Ramp贴图节点组.node_tree.name}"]')
                    for Ramp节点 in sorted(Ramp贴图节点组.node_tree.nodes, key=lambda x: x.location.y, reverse=True):  # 从上到下
                        if 是图像(Ramp节点):
                            Ramp贴图节点.append(Ramp节点)
                for 节点 in Ramp贴图节点:
                    if 节点.image:
                        return  # 已有ramp贴图
            if 暖Ramp:
                for 节点, 贴图 in zip(Ramp贴图节点, Ramp贴图):
                    if 贴图:
                        节点.image = 贴图
                        报告信息(self, '正常', f'材质Material["{材质.name}"]输入Ramp贴图:Texture["{贴图.name}"]')
            else:
                贴图节点.image = 冷Ramp
        else:
            报告信息(self, '异常', f'材质Material["{材质.name}"]的基础贴图["{基础贴图.name}"]未找到ramp贴图')
            # 1.1.0没有找到Ramp贴图贴图，新建空白图像
            Ramp贴图 = 获取空白贴图("小二插件：未找到Ramp贴图")
            for 节点 in Ramp贴图节点:
                节点.image = Ramp贴图  # 应用Ramp贴图贴图
###################################################################################################