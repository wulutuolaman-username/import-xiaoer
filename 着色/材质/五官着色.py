# coding: utf-8

import bpy
from ...通用.信息 import 报告信息
from ...着色.贴图.基础贴图 import 匹配基础贴图
from ...着色.混合.混合透明 import 混合透明, MMDalpha
from ...着色.混合.混合贴图 import 混合贴图
from ...着色.节点.材质输出 import 获取材质输出节点
from ...着色.节点.透明.透明节点 import 获取透明节点
from ...着色.节点.透明.混合节点 import 获取混合节点
from ...着色.节点.贴图.基础贴图 import 获取基础贴图节点
from ...材质.检测透明.检测透明 import 材质UV包含透明像素
from ...着色.节点.材质节点组.调色节点组 import 获取材质节点组
from ...偏好.偏好设置 import XiaoerAddonPreferences
from ...指针 import XiaoerObject, XiaoerMaterial

def 五官着色(self:bpy.types.Operator|None, 偏好:XiaoerAddonPreferences, 节点组列表, 材质:XiaoerMaterial, 透明贴图, 游戏, 模型:XiaoerObject, 材质面):
    if 材质.name in 模型.data.materials:
        """
        有基础贴图
            alpha = 1
                开启检测透明材质
                    原始贴图透明 and not 基础贴图透明
                        混合贴图(原始贴图, 基础贴图)
                    基础贴图透明
                        混合透明(基础贴图):
                                          基础贴图.outputs[1] → 混合节点.inputs[0]
                                                    透明节点 → 混合节点.inputs[1]
                            基础贴图 → 材质节点组（调色节点组） → 混合节点.inputs[2] → 材质输出节点
                关闭检测透明材质
                    基础贴图 → 材质节点组（调色节点组） → 材质输出节点
            alpha < 1
                                                 混合节点.inputs[0].default_value = alpha
                                       透明节点 → 混合节点.inputs[1]
                基础贴图 → 材质节点组（调色节点组） → 混合节点.inputs[2]
                如果基础贴图透明，设置贴图为通道打包模式
                MMD着色节点组 → 材质输出节点
        无基础贴图
            原始贴图 → 材质节点组（调色节点组）
            MMD着色节点组 → 材质输出节点
        如果未启用导入贴图，仅使用材质节点组（不连接贴图）
        """
        调色节点组 = 获取材质节点组(self, 节点组列表, 材质)
        材质输出节点 = 获取材质输出节点(材质)
        材质.node_tree.links.new(调色节点组.outputs[0], 材质输出节点.inputs['Surface'])
        MMD着色节点组 = 材质.node_tree.nodes.get("mmd_shader")
        alpha = MMDalpha(材质)
        if alpha < 1:  # 1.0.9设为透明需要在设置描边时删除该材质
            材质.blend_method = 'BLEND'  # 材质模式
            材质.show_transparent_back = False
            透明节点 = 获取透明节点(材质, '小二插件：透明节点')
            混合节点 = 获取混合节点(材质, '小二插件：混合节点')
            混合节点.inputs[0].default_value = alpha  # type:ignore
            材质.node_tree.links.new(透明节点.outputs[0], 混合节点.inputs[1])
            材质.node_tree.links.new(调色节点组.outputs[0], 混合节点.inputs[2])
            if not 材质.小二预设模板.使用插件: # 更新材质不改变输出
                材质.node_tree.links.new(MMD着色节点组.outputs[0], 材质输出节点.inputs['Surface'])
            材质.小二预设模板.透明材质 = True
            材质.小二预设模板.透明更新 = True
            报告信息(self, '正常', f'材质Material["{材质.name}"]根据MMDShaderDev的alpha设置透明')

        if 偏好.导入贴图:  # 如果开启了导入贴图
            图像节点, 基础贴图 = 匹配基础贴图(self, 材质, 游戏)  # 基础贴图
            if 基础贴图:
                基础贴图节点 = 获取基础贴图节点(材质)
                基础贴图节点.image = 基础贴图  # 应用贴图
                报告信息(self, '正常', f'材质Material["{材质.name}"]输入基础贴图:Texture["{基础贴图.name}"]')
                材质.node_tree.links.new(基础贴图节点.outputs[0], 调色节点组.inputs[0])
                材质.node_tree.links.new(调色节点组.outputs[0], 材质输出节点.inputs['Surface'])
                原始贴图 = 图像节点.image  # type:ignore
                if (透明贴图 and 原始贴图 in 透明贴图) or alpha < 1:
                    材质.blend_method = 'BLEND'  # 材质模式
                    材质.show_transparent_back = False
                    if 偏好.检测透明材质 and alpha == 1:  # 1.1.0改进分多种情况处理
                        # 起 = time.perf_counter()
                        原始贴图透明 = 材质UV包含透明像素(self, 偏好, 模型, 材质, 原始贴图, 透明贴图, 材质面)
                        基础贴图透明 = 材质UV包含透明像素(self, 偏好, 模型, 材质, 基础贴图, 透明贴图, 材质面)
                        # 终 = time.perf_counter()
                        # self.report({"INFO"}, f'材质Material["{材质.name}"]检测透明用时: {终 - 起:.6f} 秒')
                        if 原始贴图透明 and not 基础贴图透明:
                            报告信息(self, '正常', f'🔍︎ 检测到材质Material["{材质.name}"]在{原始贴图.name}包含透明像素，但{基础贴图.name}没有，将使用混合贴图')
                            混合贴图(self, 材质, 图像节点, 基础贴图节点, 调色节点组, 材质输出节点)  # 绝区零目影
                        if 基础贴图透明:
                            报告信息(self, '正常', f'🔍︎ 检测到材质Material["{材质.name}"]在{基础贴图.name}包含透明像素，将使用混合透明着色')
                            混合透明(self, 材质, 图像节点, 基础贴图节点, 调色节点组, 材质输出节点)
                    elif alpha < 1:
                        if not 材质.小二预设模板.使用插件:  # 更新材质不改变输出
                            材质.node_tree.links.new(MMD着色节点组.outputs[0], 材质输出节点.inputs['Surface'])
            else:
                # 报告信息(self, '异常', f'材质Material["{材质.name}"]未找到匹配的基础贴图')
                if 图像节点:  # 薇塔的眼睛2材质没有基础贴图
                    材质.node_tree.links.new(图像节点.outputs[0], 调色节点组.inputs[0])
                else:
                    if MMD着色节点组:
                        材质.node_tree.links.new(MMD着色节点组.outputs[0], 材质输出节点.inputs['Surface'])
                    else:
                        材质.blend_method = 'BLEND'  # 材质模式
                        材质.小二预设模板.透明材质 = True  # 记录透明材质，之后在几何节点设置无描边
                        透明节点 = 获取透明节点(材质, '小二插件：透明节点')
                        材质.node_tree.links.new(透明节点.outputs[0], 材质输出节点.inputs['Surface'])
        材质.小二预设模板.加载完成 = True