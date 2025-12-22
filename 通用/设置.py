# coding: utf-8

import bpy

# 设置辉光属性和色彩管理
def 渲染设置():
    # 代码来源：峰峰居士
    # 颜色编码转换函数
    def srgb_to_linearrgb(c):
        if c < 0:
            return 0
        elif c < 0.04045:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4
    def hex_to_rgb(h):
        r = (h & 0xff0000) >> 16
        g = (h & 0x00ff00) >> 8
        b = (h & 0x0000ff)
        return tuple([srgb_to_linearrgb(c / 0xff) for c in (r, g, b)])
    if bpy.app.version[:2] < (4, 2):
        bpy.context.scene.eevee.use_bloom = True  # 开启辉光
        bpy.context.scene.eevee.bloom_intensity = 0.08  # 辉光强度
        bpy.context.scene.eevee.bloom_color = hex_to_rgb(0xFFE4D9)  # 辉光颜色
    elif bpy.app.version[:2] >= (4, 4):
        # 1.1.2 增加辉光节点
        辉光, 渲染, 合成, 预览 = (None,) * 4
        bpy.context.space_data.shading.use_compositor = 'ALWAYS'  # type:ignore
        if bpy.app.version[:2] < (5, 0):
            # <blender_console>:1: DeprecationWarning: 'Scene.use_nodes' is expected to be removed in Blender 6.0
            bpy.context.scene.use_nodes = True
            节点树 = bpy.context.scene.node_tree
        else:
            节点树 = bpy.context.scene.compositing_node_group  # type:ignore
            if not 节点树:
                名称 = "小二插件：合成器节点"
                bpy.ops.node.new_compositing_node_group(name=名称)  # type:ignore
                节点树 = bpy.context.scene.compositing_node_group = bpy.data.node_groups.get(名称)  # type:ignore
        def 找到辉光(群组:bpy.types.Scene|bpy.types.NodeGroup):
            nonlocal 辉光
            for 节点 in 群组.node_tree.nodes:  # type:bpy.types.NodeGroup
                if 节点.type == 'GROUP':
                    找到辉光(节点)
                if 节点.type == 'GLARE':
                    辉光 = 节点
                if 辉光:
                    break
        for 节点 in 节点树.nodes:  # type:bpy.types.NodeGroup
            if 节点.type == 'R_LAYERS':
                渲染 = 节点
            if 节点.type in ['COMPOSITE','GROUP_OUTPUT']:
                合成 = 节点
            if 节点.type == 'VIEWER':
                预览 = 节点
            if 节点.type == 'GROUP':
                找到辉光(节点)
            if 节点.type == 'GLARE':
                辉光 = 节点
            if 渲染 and 辉光 and 合成 and 预览:
                break
        if not 辉光:
            if not 渲染:
                渲染 = 节点树.nodes.new("CompositorNodeRLayers")
            if not 合成:
                if bpy.app.version[:2] < (5, 0):
                    合成 = 节点树.nodes.new("CompositorNodeComposite")
                else:  # blender 5.0 合成器只有组输出
                    合成 = 节点树.nodes.new("NodeGroupOutput")
                    # 节点树.outputs.new('NodeSocketColor', "颜色")
            if not 预览:
                预览 = 节点树.nodes.new("CompositorNodeViewer")
                预览.location.x = 合成.location.x
                预览.location.y = 合成.location.y - 150

            辉光 = 节点树.nodes.new("CompositorNodeGlare")
            辉光.name = "小二插件：辉光节点"
            if bpy.app.version[:2] < (5, 0):
                辉光.glare_type = 'BLOOM'
                辉光.quality = 'MEDIUM'
            else:
                辉光.inputs['Type'].default_value = 'Bloom'  # type:ignore
                辉光.inputs['Quality'].default_value = 'Medium'  # type:ignore
            辉光.inputs['Threshold'].default_value = 1.0  # type:ignore
            辉光.inputs['Smoothness'].default_value = 0.1  # type:ignore
            # 辉光.inputs['Clamp'].default_value = False  # type:ignore
            # 辉光.inputs['Maximum'].default_value = 10.0  # type:ignore
            辉光.inputs['Strength'].default_value = 0.80  # type:ignore
            辉光.inputs['Saturation'].default_value = 1.0  # type:ignore
            辉光.inputs['Tint'].default_value = (*hex_to_rgb(0xFFE4D9), 1.0)  # type:ignore
            辉光.inputs['Size'].default_value = 0.5  # type:ignore

            左位 = 渲染.location.x
            合成接口 = 合成.inputs[0]
            预览接口 = 预览.inputs[0]
            右位 = min(合成.location.x, 预览.location.x)

            # 辉光节点输出优先连接转接点
            if 合成接口.is_linked:
                节点 = 合成接口.links[0].from_node  # 与合成相连的节点
                输出接口 = 合成接口.links[0].from_socket
                if 节点.type == 'REROUTE':  # 转接点
                    输入接口 = 节点.inputs[0]
                    输出接口 = 输入接口.links[0].from_socket
                    右位 = min(右位, 节点.location.x)
                    if 输入接口.is_linked:
                        节点 = 节点.inputs[0].links[0].from_node  # 与转接点相连的节点
                    节点树.links.new(辉光.outputs[0], 输入接口)
                else:
                    节点树.links.new(辉光.outputs[0], 合成接口)
                    节点树.links.new(辉光.outputs[0], 预览接口)
                左位 = max(左位, 节点.location.x)
            else:
                输出接口 = 渲染.outputs[0]
                节点树.links.new(辉光.outputs[0], 合成接口)
                节点树.links.new(辉光.outputs[0], 预览接口)
            if 预览接口.is_linked:
                节点 = 预览接口.links[0].from_node  # 与预览相连的节点
                if 节点.type == 'REROUTE':  # 转接点
                    右位 = min(右位, 节点.location.x)
                    节点树.links.new(辉光.outputs[0], 节点.inputs[0])
            节点树.links.new(输出接口, 辉光.inputs[0])
            # 辉光节点前后间距不小于500
            间隔 = 右位 - 左位
            if 间隔 < 500:
                右位 += 500 - 间隔
                for 连接 in 辉光.outputs[0].links:
                    连接.to_node.location.x  += 500 - 间隔
            辉光.location.x = (右位 + 左位) / 2 + 50
            辉光.location.y = 合成.location.y
            区域 = 节点树.nodes.new(type='NodeFrame')
            区域.location = 辉光.location
            区域.label = 辉光.name
            辉光.parent = 区域

    # 以下设置不受版本影响
    # bpy.context.scene.render.engine = 'Eevee'
    bpy.context.scene.view_settings.view_transform = 'Filmic'  # type:ignore
    bpy.context.scene.view_settings.look = 'High Contrast'  # type:ignore
    bpy.context.space_data.shading.type = 'RENDERED'  # type:ignore
    if "goo" in bpy.app.version_string.lower():  # 1.1.0如果是goo blender
        bpy.context.scene.eevee.use_ssr = True  # 开启屏幕空间反射
        bpy.context.scene.eevee.use_ssr_refraction = True  # 开启折射
