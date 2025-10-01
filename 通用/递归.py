from .清理 import 清理贴图
from .改名 import 重命名贴图
from ..属性.预设 import 小二预设贴图属性, 小二预设节点属性

def 递归着色节点组(self, 偏好, 数据源, 文件路径, 角色, 节点组):
    if 节点组.node_tree and 节点组.node_tree.type == 'SHADER':
        for 节点 in 节点组.node_tree.nodes:
            if 节点.type == 'TEX_IMAGE':
                图像 = 节点.image
                if 图像:
                    清理贴图(self, 图像, 节点, 数据源, 'SHADER')
                    重命名贴图(偏好, 图像, 节点, 角色, 'SHADER')
                    小二预设贴图属性(图像, 文件路径, 角色)
            if 节点.type == 'GROUP':
                if 节点.node_tree:  # 1.1.0增加检查
                    # self.report({"INFO"},f"递归节点组{节点.node_tree.name}")
                    递归着色节点组(self, 偏好, 数据源, 文件路径, 角色, 节点)
            小二预设节点属性(节点, 文件路径, 角色)

def 递归几何节点组(self, 偏好, 数据源, 文件路径, 角色, 节点组):
    if 节点组.node_tree and 节点组.node_tree.type == 'GEOMETRY':
        for 节点 in 节点组.node_tree.nodes:
            if 节点.type == 'IMAGE_TEXTURE':
                输入接口 = next((s for s in 节点.inputs if s.name == 'Image'), None)
                图像 = 输入接口.default_value
                if 图像:
                    # 清理贴图(图像, 节点, 'GEOMETRY')
                    重命名贴图(偏好, 图像, 节点, 角色, 'GEOMETRY')
                    小二预设贴图属性(图像, 文件路径, 角色)
            if 节点.type == 'MATERIAL_SELECTION':  # 1.1.0清理材质选择节点里的贴图，缇宝预设材质比模型材质多一个飘带+
                材质 = 节点.inputs[0].default_value
                if 材质 and not 材质.小二预设材质.使用插件:
                    递归着色节点组(self, 偏好, 数据源, 文件路径, 角色, 材质)
            if 节点.type == 'SET_MATERIAL':  # 1.1.0清理描边材质里的贴图
                材质 = 节点.inputs[2].default_value
                if 材质:
                    递归着色节点组(self, 偏好, 数据源, 文件路径, 角色, 材质)
            if 节点.type == 'GROUP':
                if 节点.node_tree:  # 1.1.0增加检查
                    # self.report({"INFO"},f"递归节点组{节点.node_tree.name}")
                    递归几何节点组(self, 偏好, 数据源, 文件路径, 角色, 节点)
            小二预设节点属性(节点, 文件路径, 角色)