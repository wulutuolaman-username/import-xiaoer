def 移除崩铁头发光照合并颜色(游戏, 节点组列表):
    if 游戏 == "崩坏：星穹铁道":
        for 节点组 in 节点组列表:
            if "hair" in 节点组.name and "小二" in 节点组.name:
                for 节点 in 节点组.nodes:
                    if 节点.type == 'GROUP' and 节点.node_tree and 节点.node_tree.name == "虚拟日光":
                        for 输入 in 节点.inputs:
                            if 输入.is_linked:
                                for 连接 in 输入.links:
                                    if 连接.from_node.type == 'COMBINE_COLOR':  # 找到合并颜色节点
                                        合并颜色 = 连接.from_node
                                        输入接口 = 输入
                                        for 输入 in 合并颜色.inputs:
                                            if 输入.is_linked:
                                                for 连接 in 输入.links:
                                                    输出接口 = 连接.from_socket
                                                    节点组.links.new(输出接口, 输入接口)
                                                    节点组.nodes.remove(合并颜色)
                        break