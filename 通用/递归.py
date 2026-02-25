import bpy  # noqa: F401
from .清理 import 清理贴图
from .改名 import 重命名贴图
from ..属性.属性 import *
from ..偏好.偏好设置 import *
from ..指针 import *

def 递归节点组(self:bpy.types.Operator, 偏好:小二偏好, 数据源, 文件路径, 角色, 节点组):
    # if 节点组.node_tree and 节点组.node_tree.type == 'SHADER':
        类型 = 节点组.node_tree.type
        for 节点 in 节点组.node_tree.nodes:  # type:小二节点
            if 节点.判断类型.节点.着色.是图像:
                图像 = 节点.image  # type:ignore
                if 图像:
                    清理贴图(self, 图像, 节点, 数据源, 类型)
                    重命名贴图(偏好, 图像, 节点, 角色, 类型)
                    小二预设贴图属性(图像, 文件路径, 角色)
            if 节点.判断类型.节点.是群组:
                if 节点.node_tree:  # 1.1.0增加检查
                    # self.report({"INFO"},f"递归节点组{节点.node_tree.name}")
                    递归节点组(self, 偏好, 数据源, 文件路径, 角色, 节点)
#             小二预设节点属性(节点, 文件路径, 角色)
#
# def 递归几何节点组(self:bpy.types.Operator, 偏好:小二偏好, 数据源, 文件路径, 角色, 节点组):
#     if 节点组.node_tree and 节点组.node_tree.type == 'GEOMETRY':
#         for 节点 in 节点组.node_tree.nodes:
            if 节点.判断类型.节点.几何.是图像:
                输入接口 = next((s for s in 节点.inputs if s.name == 'Image'), None)
                图像 = 输入接口.default_value  # type:ignore
                if 图像:
                    # 清理贴图(图像, 节点, 'GEOMETRY')
                    重命名贴图(偏好, 图像, 节点, 角色, 类型)
                    小二预设贴图属性(图像, 文件路径, 角色)
            if 节点.判断类型.节点.几何.是材质选择:  # 1.1.0清理材质选择节点里的贴图，缇宝预设材质比模型材质多一个飘带+
                材质:小二材质
                材质 = 节点.inputs[0].default_value  # type:ignore
                if 材质 and not 材质.小二预设材质.使用插件:
                    递归节点组(self, 偏好, 数据源, 文件路径, 角色, 材质)
            if 节点.判断类型.节点.几何.是设置材质:  # 1.1.0清理描边材质里的贴图
                材质:小二材质
                材质 = 节点.inputs[2].default_value  # type:ignore
                if 材质 and not 材质.小二预设材质.使用插件:
                    递归节点组(self, 偏好, 数据源, 文件路径, 角色, 材质)
            # if 节点.type == 'GROUP':
            #     if 节点.node_tree:  # 1.1.0增加检查
            #         # self.report({"INFO"},f"递归节点组{节点.node_tree.name}")
            #         递归几何节点组(self, 偏好, 数据源, 文件路径, 角色, 节点)
            小二预设节点属性(节点, 文件路径, 角色)