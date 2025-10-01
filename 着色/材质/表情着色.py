# coding: utf-8

from ...通用.信息 import 报告信息
from ...着色.贴图.基础贴图 import 筛选贴图, 匹配基础贴图
from ...着色.混合.混合透明 import MMDalpha
from ...着色.节点.材质输出 import 获取材质输出节点
from ...着色.节点.透明.透明节点 import 获取透明节点
from ...着色.节点.透明.混合节点 import 获取混合节点
from ...着色.节点.透明.区域节点 import 获取区域节点
from ...着色.节点.贴图.基础贴图 import 获取基础贴图节点
from ...着色.节点.材质节点组.调色节点组 import 获取材质节点组

def 表情着色(self, 偏好, 节点组列表, 材质, 游戏, 模型):
    if 材质.name in 模型.data.materials:
        """
        alpha = 0
            透明节点 → 材质输出节点
        alpha > 0
            有基础贴图
                              基础贴图.outputs[1] → 混合节点.inputs[0]
                                        透明节点 → 混合节点.inputs[1]
                基础贴图 → 材质节点组（调色节点组） → 混合节点.inputs[2] → 材质输出节点
                如果基础贴图透明，设置贴图为通道打包模式
            无基础贴图
                              原始贴图.outputs[1] → 混合节点.inputs[0]
                                        透明节点 → 混合节点.inputs[1]
                原始贴图 → 材质节点组（调色节点组） → 混合节点.inputs[2] → 材质输出节点
        如果未启用导入贴图，仅使用材质节点组（不连接贴图）
        """
        材质.小二预设模板.透明材质 = True
        材质.小二预设模板.透明更新 = True
        材质.blend_method = 'BLEND'  # 材质模式
        # material.show_transparent_back = False  # 不显示背面
        透明节点 = 获取透明节点(材质, '小二插件：透明节点')
        混合节点 = 获取混合节点(材质, '小二插件：混合节点')
        调色节点组 = 获取材质节点组(节点组列表, 材质)
        材质输出节点 = 获取材质输出节点(材质)
        材质.node_tree.links.new(透明节点.outputs[0], 混合节点.inputs[1])
        材质.node_tree.links.new(调色节点组.outputs[0], 混合节点.inputs[2])
        材质.node_tree.links.new(混合节点.outputs[0], 材质输出节点.inputs['Surface'])
        alpha = MMDalpha(材质)
        if alpha == 0:
            原始贴图, 图像节点 = 筛选贴图(self, 材质)  # 获取原始贴图
            区域节点 = 获取区域节点(材质, '小二插件：alpha为0直接透明')
            透明节点.parent = 区域节点
            材质.node_tree.links.new(图像节点.outputs[0], 调色节点组.inputs[0])
            材质.node_tree.links.new(图像节点.outputs[1], 混合节点.inputs[0])
            if not 材质.小二预设模板.使用插件:  # 更新材质不改变输出
                材质.node_tree.links.new(透明节点.outputs[0], 材质输出节点.inputs['Surface'])
            报告信息(self, '正常', f'材质Material["{材质.name}"]根据MMDShaderDev的alpha值为0设为透明')
            return  # 如果MMD节点组设置为透明，材质直接输出透明，然后进入下一个循环
        if 偏好.导入贴图:  # 如果开启了导入贴图
            原始贴图节点, 基础贴图 = 匹配基础贴图(self, 材质, 游戏)  # 基础贴图
            if 基础贴图:
                基础贴图节点 = 获取基础贴图节点(材质)
                基础贴图节点.image = 基础贴图  # 应用贴图
                报告信息(self, '正常', f'材质Material["{材质.name}"]输入基础贴图:Texture["{基础贴图.name}"]')
                材质.node_tree.links.new(基础贴图节点.outputs[0], 调色节点组.inputs[0])
                材质.node_tree.links.new(基础贴图节点.outputs[1], 混合节点.inputs[0])
            else:
                # 报告信息(self, '异常', f'材质Material["{材质.name}"]未找到匹配的基础贴图')
                if 原始贴图节点:  # 薇塔的眼睛2材质没有基础贴图
                    材质.node_tree.links.new(原始贴图节点.outputs[0], 调色节点组.inputs[0])
                    材质.node_tree.links.new(原始贴图节点.outputs[1], 混合节点.inputs[0])
                elif not 材质.小二预设模板.使用插件: # 更新材质不改变输出:
                    if MMD着色节点组:
                        材质.node_tree.links.new(MMD着色节点组.outputs[0], 材质输出节点.inputs['Surface'])
                    else:
                        材质.node_tree.links.new(透明节点.outputs[0], 材质输出节点.inputs['Surface'])
        材质.小二预设模板.加载完成 = True