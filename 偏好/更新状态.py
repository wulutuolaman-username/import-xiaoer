from ..着色.节点.材质节点组.材质节点组 import 搜索材质节点组
from ..着色.节点.贴图.基础贴图 import 搜索基础贴图节点
from ..着色.混合.混合法向 import 混合法向

def 更新状态(self, context, 当前选项, 选项列表):
    if hasattr(self, 当前选项) and getattr(self, 当前选项, True):
        for 选项 in 选项列表:
            setattr(self, 选项, False)  # 动态设置属性
        # 强制标记属性为已修改
        context.scene.update_tag()
    return None  # 显式返回 None
# update=lambda self, context: self.更新状态(context, '搜索贴图文件夹', ["指定贴图文件夹", "使用模型路径"])

def 更新搜索贴图文件夹(self, context):
    if self.搜索贴图文件夹:
        self.指定贴图文件夹 = False
        self.使用模型路径 = False
    return None  # 显式返回 None

def 更新指定贴图文件夹(self, context):
    if self.指定贴图文件夹:
        self.搜索贴图文件夹 = False
        self.使用模型路径 = False
    return None  # 显式返回 None

def 更新使用模型路径(self, context):
    if self.使用模型路径:
        self.搜索贴图文件夹 = False
        self.指定贴图文件夹 = False
    return None  # 显式返回 None

def 更新基础贴图快速匹配(self, context):
    if self.基础贴图快速匹配:
        self.基础贴图精确匹配 = False
    return None  # 显式返回 None

def 更新基础贴图精确匹配(self, context):
    if self.基础贴图精确匹配:
        self.基础贴图快速匹配 = False
    return None  # 显式返回 None

# def 更新贴图名称严格匹配(self, context):
#     if self.贴图名称严格匹配:
#         self.贴图名称宽松匹配 = False
#     return None  # 显式返回 None
#
# def 更新贴图名称宽松匹配(self, context):
#     if self.贴图名称宽松匹配:
#         self.贴图名称严格匹配 = False
#     return None  # 显式返回 None

def 更新基础贴图alpha连接(self, context):
    if context.active_object and context.active_object.type == 'MESH':
        # print(context.active_object.name)
        for 材质 in context.active_object.data.materials:
            材质节点组 = 搜索材质节点组(材质)
            基础贴图节点 = 搜索基础贴图节点(材质)
            if 基础贴图节点 and 材质节点组 and len(材质节点组.inputs) > 1 and "alpha" in 材质节点组.inputs[1].name.lower():
                # print(材质.name, 材质节点组.name, 基础贴图节点.name)
                if self.连接基础贴图alpha and not 基础贴图节点.小二预设模板.已连接基础贴图alpha:
                    材质.node_tree.links.new(基础贴图节点.outputs[1], 材质节点组.inputs[1])
                    基础贴图节点.小二预设模板.已连接基础贴图alpha = True
                    # print(f"{材质.name}已连接基础贴图alpha")
                if not self.连接基础贴图alpha and 基础贴图节点.小二预设模板.已连接基础贴图alpha:
                    材质.node_tree.links.remove(next((连接 for 连接 in 材质.node_tree.links
                      if 连接.from_socket== 基础贴图节点.outputs[1] and 连接.to_socket == 材质节点组.inputs[1]),None))
                    基础贴图节点.小二预设模板.已连接基础贴图alpha = False
                    # print(f"{材质.name}已断连基础贴图alpha")
    return None

def 更新通过点乘混合法向(self, context):
    混合法向(self)
    return None