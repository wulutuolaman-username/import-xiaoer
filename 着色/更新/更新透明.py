import bpy
from ..节点.贴图.基础贴图 import 搜索基础贴图节点
from ..节点.材质节点组.材质节点组 import 搜索材质节点组
from ..节点.材质输出 import 获取材质输出节点
from ..混合.混合透明 import 混合透明
from ..更新.清理节点 import 清理无用节点
from ...材质.材质分类 import 材质分类
from ...几何.设置描边 import 分类设置描边

运行中 = False

def 更新透明(self, context):
    global 运行中
    模型 = context.active_object
    if 模型 and 模型.active_material and not 运行中:
        材质 = 模型.active_material
        # print(材质.name, 材质.小二预设模板.透明材质, 材质.小二预设模板.透明更新)
        if (材质.小二预设模板.透明材质 == True and 材质.小二预设模板.透明更新 == False) or (材质.小二预设模板.透明材质 == False and 材质.小二预设模板.透明更新 == True):
            运行中 = True
            try:
                基础贴图节点 = 搜索基础贴图节点(材质)
                材质节点组 = 搜索材质节点组(材质)
                材质输出节点 = 获取材质输出节点(材质)
                # print(基础贴图节点.name, 材质节点组.name, 材质输出节点.name)
                if not 基础贴图节点:
                    if 材质节点组 and 材质节点组.inputs and 材质节点组.inputs[0].type == 'RGBA' and 材质节点组.inputs[0].is_linked:
                        节点 = 材质节点组.inputs[0].links[0].from_node
                        if 节点.type == 'TEX_IMAGE':
                            基础贴图节点 = 节点
                    else:
                        for 节点 in 材质.node_tree.nodes:
                            if 节点.type == 'TEX_IMAGE':
                                基础贴图节点 = 节点
                                break
                if not 材质.小二预设模板.混合模式:
                    材质.小二预设模板.混合模式 = 材质.blend_method
                if not 材质.小二预设模板.显示背面:
                    材质.小二预设模板.显示背面 = 材质.show_transparent_back
                if 材质.小二预设模板.透明材质:
                    混合透明(self, 材质, None, 基础贴图节点, 材质节点组, 材质输出节点)
                    if 材质.小二预设模板.材质分类 and 材质.小二预设模板.材质分类 in ['五官', '表情']:
                        材质.blend_method = 'BLEND'
                    elif 材质.blend_method != 'BLEND':
                        材质.blend_method = 'CLIP'
                    材质.show_transparent_back = False
                else:
                    if 材质节点组:
                        材质.node_tree.links.new(材质节点组.outputs[0], 材质输出节点.inputs['Surface'])
                    材质.blend_method = 材质.小二预设模板.混合模式
                    材质.show_transparent_back = 材质.小二预设模板.显示背面
                    清理无用节点(材质)
                    材质.小二预设模板.透明更新 = False
                if 模型.type == 'MESH':
                    节点组列表 = []
                    for 群组 in 模型.小二预设模板.导入节点组:
                        节点组列表.append(群组.节点组)
                    五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质 = 材质分类(模型)
                    实体化描边 = next((节点组 for 节点组 in 节点组列表 if "实体化描边" in 节点组.name), None)
                    if 实体化描边:
                        分类设置描边(self, 实体化描边, 五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质)
                运行中 = False
            finally:
                # 无论成功还是报错，都会把运行中恢复
                运行中 = False
    return None