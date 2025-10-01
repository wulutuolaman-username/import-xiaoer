from ....属性.模板 import 小二预设模板属性

def 搜索材质节点组(材质):
    材质节点组 = 材质.node_tree.nodes.get("小二插件：材质节点组", None)
    return 材质节点组

def 设置材质节点组(材质, 节点组, 材质节点组):
    材质节点组.node_tree = 节点组  # 应用材质节点组
    材质节点组.location = (-200, 1500)  # 定位材质节点组
    材质节点组.name = "小二插件：材质节点组"
    print(f'材质Material["{材质.name}"]输入节点组{节点组.name}')

def 获取材质节点组(游戏, 节点组列表, 材质, 小二材质类型):
    材质节点组 = 搜索材质节点组(材质)
    if not 材质节点组:
        材质节点组 = 材质.node_tree.nodes.new(type='ShaderNodeGroup')  # 新建节点组
    if not 材质节点组.node_tree or 材质.小二预设模板.材质分类 != 材质.小二预设模板.更新分类:
        for 节点组 in 节点组列表:  # 设置材质节点组
            if 节点组.type == 'SHADER' and (  # 搜索材质节点组
                    节点组.name == f"{游戏}{材质.小二预设模板.材质分类}" or
                    (小二材质类型 in 节点组.name and "小二" in 节点组.name)
            ):
                # self.report({"INFO"}, f'材质Material["{材质.name}"]材质节点组ShaderNodeGroup["{节点组.name}"]')
                设置材质节点组(材质, 节点组, 材质节点组)
                break  # 找到后立即退出循环，提高效率
    小二预设模板属性(材质节点组.小二预设模板, None, None, None, None)
    return 材质节点组