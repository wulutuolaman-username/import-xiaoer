# coding: utf-8
import bpy
from ...通用.回调 import 回调
from ...通用.信息 import 报告信息
from ...着色.贴图.基础贴图 import 匹配基础贴图
from ...着色.贴图.光照贴图 import 获取光照贴图
from ...着色.贴图.法线贴图 import 获取法线贴图
from ...着色.混合.混合透明 import 混合透明, MMDalpha
from ...通用.编号 import 节点组编号
from ...材质.检测透明.检测透明 import 材质UV包含透明像素
from ...着色.节点.材质输出 import 获取材质输出节点
from ...着色.节点.透明.透明节点 import 获取透明节点
from ...着色.节点.透明.混合节点 import 获取混合节点
from ...着色.节点.透明.区域节点 import 获取区域节点
from ...着色.节点.贴图.基础贴图 import 获取基础贴图节点
from ...着色.节点.材质节点组.材质节点组 import 获取材质节点组
from ...着色.节点.材质节点组.调色节点组 import 获取材质节点组 as 获取调色节点组
from ...着色.节点.贴图节点组.光照贴图节点组 import 获取光照贴图节点组
from ...着色.节点.贴图节点组.Ramp贴图节点组 import ramp节点组
from ...着色.节点.贴图节点组.我的贴图节点组 import 我的贴图节点组
from ...着色.贴图.空白贴图 import 获取空白贴图
from ...偏好.偏好设置 import XiaoerAddonPreferences
from ...指针 import XiaoerObject, XiaoerMaterial

# 材质处理
def 小二好色(self:bpy.types.Operator|None, 偏好:XiaoerAddonPreferences, 节点组列表, 材质:XiaoerMaterial, 透明贴图, 材质类型, 小二材质类型, 游戏, 模型:XiaoerObject, 材质面):
    if 材质.name in 模型.data.materials:
        """
        有基础贴图
            alpha = 1
                开启检测透明材质
                    基础贴图透明
                        混合透明(基础贴图):
                              基础贴图.outputs[1] → 混合节点.inputs[0]
                                        透明节点 → 混合节点.inputs[1]
                            基础贴图 → 材质节点组 → 混合节点.inputs[2] → 材质输出节点
                            如果基础贴图透明，设置贴图为通道打包模式
                关闭检测透明材质
                    基础贴图 → 材质节点组 → 材质输出节点
                    如果基础贴图透明，设置贴图为通道打包模式
            0 < alpha < 1
                                      混合节点.inputs[0].default_value = alpha
                            透明节点 → 混合节点.inputs[1]
                基础贴图 → 材质节点组 → 混合节点.inputs[2] → 材质输出节点
                如果基础贴图透明，设置贴图为通道打包模式
            alpha = 0
                透明节点 → 材质输出节点
        无基础贴图
            原始贴图 → 材质节点组（调色节点组）
            MMD着色节点组 → 材质输出节点
        如果未启用导入贴图，仅使用材质节点组（不连接贴图）
        """
        材质节点组 = 获取材质节点组(self, 游戏, 节点组列表, 材质, 小二材质类型)
        材质输出节点 = 获取材质输出节点(材质)
        材质.node_tree.links.new(材质节点组.outputs[0], 材质输出节点.inputs['Surface'])
        MMD着色节点组 = 材质.node_tree.nodes.get("mmd_shader")  # 设为透明需要在设置描边时删除该材质
        alpha = MMDalpha(材质)
        if alpha < 1:  # 1.0.9检测材质alpha
            材质.blend_method = 'BLEND'  # 材质模式
            材质.show_transparent_back = False
            透明节点 = 获取透明节点(材质, '小二插件：透明节点')
            区域节点 = 获取区域节点(材质, '小二插件：已在几何节点设置无描边')
            透明节点.parent = 区域节点
            if alpha == 0:
                if not 材质.小二预设模板.使用插件:  # 更新材质不改变输出
                    材质.node_tree.links.new(透明节点.outputs[0], 材质输出节点.inputs['Surface'])
                报告信息(self, '正常', f'材质Material["{材质.name}"]根据MMDShaderDev的alpha设置透明')
            if alpha > 0:  # 1.0.9混合透明
                混合节点 = 获取混合节点(材质, '小二插件：混合节点')
                混合节点.inputs[0].default_value = alpha  # type:ignore
                材质.node_tree.links.new(透明节点.outputs[0], 混合节点.inputs[1])
                材质.node_tree.links.new(材质节点组.outputs[0], 混合节点.inputs[2])
                if not 材质.小二预设模板.使用插件:  # 更新材质不改变输出
                    材质.node_tree.links.new(混合节点.outputs[0], 材质输出节点.inputs['Surface'])
            材质.小二预设模板.透明材质 = True
            材质.小二预设模板.透明更新 = True
        if 偏好.导入贴图:  # 如果开启了导入贴图
            图像节点, 基础贴图 = 匹配基础贴图(self, 材质, 游戏)  # 基础贴图
            # self.report({"INFO"}, f'材质Material["{材质.name}"] 图像节点{图像节点} 基础贴图{基础贴图}')
            if not 材质.小二预设模板.完成匹配基础贴图:
                if 图像节点:
                    # 1.1.0如果没有匹配基础贴图，使用调色节点组
                    调色节点组 = 获取调色节点组(self, 节点组列表, 材质)
                    # for 节点组 in 节点组列表:  # 设置材质节点组并输出材质
                    #     if 节点组.type == 'SHADER' and any(
                    #         节点组.name.startswith(后缀) for 后缀 in ["调色", "校色"]):  # 搜索材质节点组
                    #         材质节点组.node_tree = 节点组  # 应用节点组
                    材质.node_tree.links.new(图像节点.outputs[0], 调色节点组.inputs[0])
                    if alpha < 1:
                        混合节点 = 获取混合节点(材质, '小二插件：混合节点')
                        材质.node_tree.links.new(调色节点组.outputs[0], 混合节点.inputs[2])
                if MMD着色节点组:
                    if not 材质.小二预设模板.使用插件:  # 更新材质不改变输出
                        材质.node_tree.links.new(MMD着色节点组.outputs[0], 材质输出节点.inputs['Surface'])
                else:
                    透明节点 = 获取透明节点(材质, '小二插件：透明节点')
                    材质.blend_method = 'BLEND'
                    材质.小二预设模板.透明材质 = True  # 记录透明材质，之后在几何节点设置无描边
                    if not 材质.小二预设模板.使用插件:  # 更新材质不改变输出
                        材质.node_tree.links.new(透明节点.outputs[0], 材质输出节点.inputs['Surface'])
                    return
            if 材质.小二预设模板.完成匹配基础贴图:  # 如果检索到材质的匹配贴图
                基础贴图透明 = False
                if 透明贴图 and 基础贴图 in 透明贴图:
                    if 偏好.检测透明材质 and alpha == 1:  # 1.1.0检测透明材质
                        基础贴图透明 = 材质UV包含透明像素(self, 偏好, 模型, 材质, 基础贴图, 透明贴图, 材质面)
                if 材质节点组.node_tree.name == f"{游戏}{材质类型}":  # 如果是我的中文名节点组模板
                    我的贴图节点组(self, 偏好, 节点组列表, 材质, 材质节点组, 游戏, 基础贴图, 材质类型, 透明贴图, 基础贴图透明, 材质输出节点)
                elif "小二" in 材质节点组.node_tree.name:  # 小二的英文名节点组模板
                    基础贴图节点 = 获取基础贴图节点(材质)
                    基础贴图节点.image = 基础贴图  # 应用贴图
                    报告信息(self, '正常', f'材质Material["{材质.name}"]输入基础贴图:Texture["{基础贴图.name}"]')
                    if 透明贴图 and 基础贴图 in 透明贴图:
                        基础贴图节点.image.alpha_mode = 'CHANNEL_PACKED'  # 通道打包
                        if 基础贴图透明:  # 1.1.0可选混合透明
                            材质.blend_method = 'CLIP'  # 材质模式  # BLEND会将视线穿过的所有面透明，如爱可菲的裙材质（胸口）
                            材质.show_transparent_back = False
                            报告信息(self, '正常', f'🔍︎ 检测到材质Material["{材质.name}"]在{基础贴图.name}包含透明像素，将使用混合透明着色')
                            混合透明(self, 材质, 图像节点, 基础贴图节点, 材质节点组, 材质输出节点)
                    # 光照贴图
                    光照贴图节点组 = None
                    # self.report({"INFO"},f'检查点1：材质Material["{材质.name}"]光照贴图节点组{光照贴图节点组.node_tree.name}')
                    多部件 = False  # 1.1.0解决一种材质类型多个部件ramp贴图（如养乐多的丝柯克）

                    记录次数 = 0
                    def 记录(网格:XiaoerObject):
                        nonlocal 记录次数  # 声明使用外层的记录次数
                        if 网格.小二预设模板.导入贴图:
                            记录次数 += 1
                    回调(记录, 模型)

                    if 基础贴图.小二预设模板.匹配节点组:  # 检查贴图和材质节点组的使用情况
                        # self.report({"INFO"}, f"1当前字典键: {list(基础贴图匹配的节点组.items())}")
                        # self.report({"INFO"},f'检查点1：材质Material["{材质.name}"]材质节点组{材质节点组.node_tree.name}')
                        材质节点组.node_tree = 基础贴图.小二预设模板.匹配节点组
                        光照贴图节点组 = 获取光照贴图节点组(游戏, 材质节点组)
                        # self.report({"INFO"},f'检查点2：材质Material["{材质.name}"]材质节点组{材质节点组.node_tree.name}')
                        # self.report({"INFO"},f'材质Material["{material.name}"]应用材质节点组:ShaderNodeNodeTree["{材质节点组.node_tree.name}"]')
                        # self.report({"INFO"}, f'材质Material["{material.name}"]应用光照贴图节点组{光照贴图节点组.node_tree.name}')
                    elif not 基础贴图.小二预设模板.匹配节点组 and 材质节点组.node_tree.users == 1 + 记录次数:  # 1.1.0记录节点组
                        # self.report({"INFO"},f'材质Material["{material.name}"]应用节点组:ShaderNodeNodeTree["{材质节点组.node_tree.name}"]')
                        基础贴图.小二预设模板.匹配节点组 = 材质节点组.node_tree  # 存储贴图和材质节点组对应信息
                        光照贴图节点组 = 获取光照贴图节点组(游戏, 材质节点组)
                        报告信息(self, '正常', f'材质Material["{材质.name}"]第一个应用光照贴图节点组{光照贴图节点组.node_tree.name}')
                    elif not 基础贴图.小二预设模板.匹配节点组 and 材质节点组.node_tree.users > 1 + 记录次数:  # 1.1.0记录节点组
                        多部件 = True
                        材质节点组.node_tree = 材质节点组.node_tree.copy()  # 应用节点组副本
                        节点组编号(self, 材质节点组.node_tree)  # 重命名材质节点组副本
                        报告信息(self, '正常', f'材质Material["{材质.name}"]创建材质节点组副本:ShaderNodeNodeTree["{材质节点组.node_tree.name}"]')
                        基础贴图.小二预设模板.匹配节点组 = 材质节点组.node_tree  # 存储贴图和材质节点组对应信息
                        # self.report({"INFO"}, f"2当前字典键: {list(基础贴图匹配的节点组.items())}")
                        光照贴图节点组 = 获取光照贴图节点组(游戏, 材质节点组)  # 材质节点组重命名后，需要重新找到ligthmap节点组
                        光照贴图节点组.node_tree = 光照贴图节点组.node_tree.copy()  # 应用节点组副本
                        节点组编号(self, 光照贴图节点组.node_tree)  # 重命名光照贴图节点组副本
                        报告信息(self, '正常', f'材质Material["{材质.name}"]创建光照贴图节点组副本{光照贴图节点组.node_tree.name}')
                    # 改变组节点节点树后会断开连接
                    if 基础贴图透明:
                        混合节点 = 获取混合节点(材质, '小二插件：混合节点')
                        材质.node_tree.links.new(材质节点组.outputs[0], 混合节点.inputs[2])
                    else:
                        材质.node_tree.links.new(材质节点组.outputs[0], 材质输出节点.inputs['Surface'])
                    if not 光照贴图节点组:
                        报告信息(self, '异常', f'节点组["{材质节点组.name}"]未找到光照贴图节点组')
                    # self.report({"INFO"},f'检查点2：材质Material["{材质.name}"]光照贴图节点组{光照贴图节点组.node_tree.name}')
                    光照贴图节点 = next((node for node in 光照贴图节点组.node_tree.nodes if node.type == 'TEX_IMAGE'), None)  # 找到ligthmap贴图节点
                    光照贴图 = 获取光照贴图(self, 游戏, 基础贴图)
                    if 光照贴图:
                        光照贴图节点.image = 光照贴图  # 应用光照贴图
                        报告信息(self, '正常', f'材质Material["{材质.name}"]输入光照贴图:Texture["{光照贴图.name}"]')
                        光照贴图.colorspace_settings.name = 'Non-Color'  # type:ignore
                    else:
                        报告信息(self, '异常', f'材质Material["{材质.name}"]的基础贴图["{基础贴图.name}"]未找到光照贴图')
                        # 1.1.0没有找到光照贴图，新建空白图像
                        光照贴图 = 获取空白贴图("小二插件：未找到光照贴图")
                        光照贴图节点.image = 光照贴图  # 应用光照贴图
                    # 法线贴图
                    法线贴图 = 获取法线贴图(self, 游戏, 基础贴图)
                    # self.report({"INFO"}, f'材质Material["{material.name}"]调试法线贴图["{法线贴图}"]')
                    if 法线贴图:
                        法线贴图节点 = 材质.node_tree.nodes.new(type='ShaderNodeTexImage')  # 新建图像节点
                        法线贴图节点.image = 法线贴图  # 应用法线贴图
                        报告信息(self, '正常', f'材质Material["{材质.name}"]输入法线贴图:Texture["{法线贴图.name}"]')
                        法线贴图节点.location = (-500, 1000)
                        法线贴图.colorspace_settings.name = 'Non-Color'  # type:ignore
                        材质.node_tree.links.new(法线贴图节点.outputs[0], 材质节点组.inputs[2])
                    # Ramp贴图
                    ramp节点组(self, 游戏, 材质, 材质节点组, 基础贴图, 多部件, 记录次数)
                    材质.node_tree.links.new(基础贴图节点.outputs[0], 材质节点组.inputs[0])
                    if 偏好.连接基础贴图alpha and len(材质节点组.inputs) > 1 and "alpha" in 材质节点组.inputs[1].name.lower():  # 1.1.0原神可能不需要连接alpha
                        材质.node_tree.links.new(基础贴图节点.outputs[1], 材质节点组.inputs[1])
                        基础贴图节点.小二预设模板.已连接基础贴图alpha = True
        材质.小二预设模板.加载完成 = True