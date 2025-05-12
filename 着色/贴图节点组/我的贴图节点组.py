from .重命名节点组 import 重命名节点组
from ..贴图.光照贴图 import 获取光照贴图
from ..贴图.法线贴图 import 获取法线贴图
from ..贴图.AO贴图 import 获取AO贴图

def 我的贴图节点组(self, 数据源, 材质, 材质节点组, 游戏, 基础贴图, 基础贴图匹配的节点组, 材质类型, alpha贴图):
    贴图节点组 = 材质.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建贴图节点组
    for 节点组 in 数据源.node_groups:
        if 节点组.type == 'SHADER' and f"{材质类型}贴图" in 节点组.name:  # 搜索贴图节点组
            # self.report({"INFO"}, f'调试{texture_node_group_name}')
            贴图节点组.location = (-500, 1500)  # 定位贴图节点组
            if 基础贴图 in 基础贴图匹配的节点组:  # 检查此类材质是否有多个基础色贴图
                贴图节点组.node_tree = 基础贴图匹配的节点组[基础贴图]  # 直接应用贴图节点组
            elif 基础贴图 not in 基础贴图匹配的节点组 and 节点组.users == 0:
                贴图节点组.node_tree = 节点组  # 直接应用节点组
                基础贴图匹配的节点组[基础贴图] = 贴图节点组.node_tree  # 存储贴图和贴图节点组对应信息
            elif 基础贴图 not in 基础贴图匹配的节点组 and 节点组.users > 0:
                # 如果基础色贴图已使用，并且贴图节点组也已使用，但出现了新的材质贴图，说明该材质类型不止一个基础色贴图
                贴图节点组.node_tree = 节点组.copy()  # 应用节点组副本
                # self.report({"INFO"},f'节点组["{texture_node_group.node_tree.name}"]')
                重命名节点组(self, 贴图节点组.node_tree)  # 重命名贴图节点组副本
                # self.report({"INFO"}, f'重命名["{texture_node_group.node_tree.name}"]')
                基础贴图匹配的节点组[基础贴图] = 贴图节点组.node_tree  # 存储贴图和贴图节点组对应信息
            self.report({"INFO"},f'材质Material["{材质.name}"]应用节点组:ShaderNodeNodeTree["{贴图节点组.node_tree.name}"]')

            # 1.0.3连接名称相同的接口
            for 输出 in 贴图节点组.outputs:
                for 输入 in 材质节点组.inputs:
                    if 输出.name == 输入.name:
                        try:
                            材质.node_tree.links.new(输出, 输入)
                        except:
                            pass

            组输出节点 = (贴图节点组.node_tree.nodes.get("组输出") or 贴图节点组.node_tree.nodes.get(
                "Group Output"))  # 找到组输出节点
            if 基础贴图:  # 如果材质查找到匹配贴图
                for 输入 in 组输出节点.inputs:
                    # self.report({"INFO"}, f"输出节点插槽: {input_socket.name}")
                    if "基础" in 输入.name and not "Alpha" in 输入.name:
                        for 连接 in 输入.links:
                            图像节点 = 连接.from_node
                            图像节点.image = 基础贴图  # 输入基础贴图
                            if alpha贴图:
                                if 基础贴图 in alpha贴图:
                                    图像节点.image.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
                            self.report({"INFO"},f'材质Material["{材质.name}"]输入基础贴图:Texture["{基础贴图.name}"]')
                    if "光照" in 输入.name and not "Alpha" in 输入.name:
                        for 连接 in 输入.links:
                            图像节点 = 连接.from_node
                            光照贴图 = 获取光照贴图(游戏, 基础贴图)
                            if 光照贴图:
                                图像节点.image = 光照贴图  # 输入光照贴图
                                光照贴图.colorspace_settings.name = 'Non-Color'  # 非彩色
                                self.report({"INFO"},f'材质Material["{材质.name}"]输入光照贴图:Texture["{光照贴图.name}"]')
                            else:
                                self.report({"WARNING"}, f'材质Material["{材质.name}"]未找到匹配的光照贴图')
                    if "法线" in 输入.name and not "Alpha" in 输入.name:
                        for 连接 in 输入.links:
                            图像节点 = 连接.from_node
                            法线贴图 = 获取法线贴图(游戏, 基础贴图)
                            if 法线贴图:
                                图像节点.image = 法线贴图  # 输入法线贴图
                                法线贴图.colorspace_settings.name = 'Non-Color'  # 非彩色
                                self.report({"INFO"},f'材质Material["{材质.name}"]输入法线贴图:Texture["{法线贴图.name}"]')
                            else:
                                self.report({"WARNING"}, f'材质Material["{材质.name}"]未找到匹配的法线贴图')
                    if "AO" in 输入.name and not "Alpha" in 输入.name:
                        for 连接 in 输入.links:
                            图像节点 = 连接.from_node
                            AO贴图 = 获取AO贴图(游戏, 基础贴图)
                            if AO贴图:
                                图像节点.image = AO贴图  # 输入AO贴图
                                AO贴图.colorspace_settings.name = 'Non-Color'  # 非彩色
                                self.report({"INFO"},f'材质Material["{材质.name}"]输入AO贴图:Texture["{AO贴图.name}"]')
                            else:
                                self.report({"WARNING"}, f'材质Material["{材质.name}"]未找到匹配的AO贴图')
            else:  # 如果材质没有匹配贴图
                self.report({"WARNING"}, f'材质Material["{材质.name}"]未找到匹配的基础贴图')