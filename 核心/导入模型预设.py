# coding: utf-8

import bpy
from ..通用.设置 import 渲染设置
from ..几何.几何节点 import 几何节点
from ..通用.清理 import 清理贴图
from ..图像.筛选贴图 import 筛选图像
from ..通用.绑定 import 绑定
from ..通用.剪尾 import 剪去后缀

def 炒飞小二(偏好, 模型, 文件路径, 角色, self):
    self.report({"INFO"}, f"导入预设" + str(文件路径))
    # 追加预设文件的所有资产
    with bpy.data.libraries.load(文件路径) as (数据源, 数据流):
        for 属性 in dir(数据流):
            setattr(数据流, 属性, getattr(数据源, 属性))

    # 设置辉光属性和色彩管理
    渲染设置()

    # 应用几何节点
    for 节点组 in 数据源.node_groups:
        if 节点组.type == 'GEOMETRY' and 节点组.users == 0:  # 未被使用的几何节点组
            几何节点(模型, 节点组)  # 应用几何节点
            if 偏好.重命名资产 and 偏好.重命名贴图:  ############### 如果开启了连续导入 ###############
                for 节点 in 节点组.nodes:
                    if 节点.type == 'GROUP':
                        for 二级节点组 in 节点.node_tree.nodes:
                            if 二级节点组.type == 'GROUP':
                                if 二级节点组.node_tree:
                                    for 图像节点 in 二级节点组.node_tree.nodes:
                                        if 图像节点.name.startswith("Image Texture"):  # 查找图像纹理节点:
                                            输入接口 = next((s for s in 图像节点.inputs if s.name == 'Image'), None)
                                            if 输入接口 and 输入接口.default_value:
                                                描边遮罩 = 输入接口.default_value
                                                描边遮罩.name += "_" + 角色  # 描边遮罩重命名
        if 节点组.name.startswith("MMDTexUV") or 节点组.name.startswith("MMDShaderDev"):
            continue  # 如果是MMD固有节点组，无需后续重命名
        if 偏好.重命名资产 and 偏好.重命名节点组:  ############### 如果开启了连续导入 ###############
            节点组.name += "_" + 角色  # 节点组重命名

    # 1.0.7确保驱动物体在模型集合中
    for 物 in 数据源.objects:
        if 物.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(物)  # 手动加入场景
        if 模型.users_collection:  # 检查选中模型是否在集合中
            for 集合 in 物.users_collection:
                集合.objects.unlink(物)
            模型.users_collection[0].objects.link(物)  # 将驱动物体移入模型集合

    if 偏好.重命名资产 and 偏好.独立集合:  ############### 如果开启了连续导入 ###############
        # 将模型相关物体移入独立集合
        新集合 = bpy.data.collections.new(角色)  # 新建独立集合
        bpy.context.scene.collection.children.link(新集合)  # 关联到场景集合
        for 集合 in 模型.users_collection:
            集合.objects.unlink(模型)
        新集合.objects.link(模型)
        for 物 in 数据源.objects:
            新集合.objects.link(物)  # 将驱动物体移入新集合
        for 集合 in 模型.parent.parent.users_collection:
            集合.objects.unlink(模型.parent.parent)  # 祖父级空物体移出旧集合
        新集合.objects.link(模型.parent.parent)  # 祖父级空物体移入新集合
    if 偏好.重命名资产:  ############### 如果开启了连续导入 ###############
        if 偏好.重命名动作:  ############### 如果开启了连续导入 ###############
            if 模型.parent.parent.animation_data and 模型.parent.parent.animation_data.action:
                名称, 后缀 = 剪去后缀(模型.parent.parent.animation_data.action.name)
                if 后缀:
                    模型.parent.parent.animation_data.action.name = 名称
                模型.parent.parent.animation_data.action.name += "_" + 角色
        for 子级 in 模型.parent.parent.children:
            if 偏好.独立集合:  ############### 如果开启了连续导入 ###############
                for 集合 in 子级.users_collection:
                    集合.objects.unlink(子级)  # 祖父级空物体的子级全部移出旧集合
                新集合.objects.link(子级)  # 祖父级空物体的子级全部移入新集合
            if 子级.name.startswith(模型.name.split("_mesh")[0]):  # 骨架
                if 偏好.重命名动作:  ############### 如果开启了连续导入 ###############
                    if 子级.animation_data and 子级.animation_data.action:
                        名称, 后缀 = 剪去后缀(子级.animation_data.action.name)
                        if 后缀:
                            子级.animation_data.action.name = 名称
                        子级.animation_data.action.name += "_" + 角色
            else:  # 如果是刚体和关节的父级空物体
                if 偏好.重命名刚体和关节:  ############### 如果开启了连续导入 ###############
                    名称, 后缀 = 剪去后缀(子级.name)
                    子级.name = f"{名称}_{角色}"  # 祖父级空物体的子级物体重命名
                for 孙级 in 子级.children:
                    if 偏好.独立集合:  ############### 如果开启了连续导入 ###############
                        for 集合 in 孙级.users_collection:
                            集合.objects.unlink(孙级)  # 祖父级空物体的孙级全部移出旧集合
                        新集合.objects.link(孙级)  # 祖父级空物体的孙级全部移入新集合
                    if 偏好.重命名刚体和关节:  ############### 如果开启了连续导入 ###############
                        名称, 后缀 = 剪去后缀(孙级.name)
                        孙级.name = f"{名称}_{角色}"  # 祖父级空物体的孙级物体重命名

    # 1.0.5解决同名材质问题
    同名集合 = set()
    模型同名材质列表 = []
    预设同名材质列表 = []
    # 检测模型中的同名材质
    for 材质 in 模型.data.materials:
        名称, 后缀 = 剪去后缀(材质.name)
        if 名称 not in 同名集合:
            同名材质 = [m for m in 模型.data.materials if 剪去后缀(m.name)[0] == 名称]
            if len(同名材质) > 1:
                同名集合.add(名称)
                模型同名材质列表.extend(同名材质)
    if len(同名集合) > 0:
        for 名称 in 同名集合:
            for 材质 in reversed(数据源.materials):
                if 剪去后缀(材质.name)[0] == 名称:
                    预设同名材质列表.append(材质)
        for 模型材质, 预设材质 in zip(模型同名材质列表, 预设同名材质列表):
            for i, 材质 in enumerate(模型.data.materials):
                if 材质 is 模型材质:
                    模型.data.materials[i] = 预设材质
                    预设材质.name = 模型材质.name
                    if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
                        预设材质.name += "_" + 角色  # 网格材质重命名
                    break

    # 替换网格材质
    for i, 模型材质 in enumerate(模型.data.materials):  # 在网格中遍历旧材质
        if 模型材质 not in 预设同名材质列表:
            名称1, 后缀1 = 剪去后缀(模型材质.name)  # 连续导入模型，材质会产生后缀
            if 后缀1:
                模型材质.name = 名称1
            for 预设材质 in 数据源.materials:  # 在追加材质中遍历新材质
                名称2, 后缀2 = 剪去后缀(预设材质.name)
                if 名称1 == 名称2: # 匹配材质名称
                    模型.data.materials[i] = 预设材质  # 替换材质
                    预设材质.name = 名称1  # 应用材质原名称
                    if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
                        预设材质.name += "_" + 角色  # 网格材质重命名
                    break
    # 替换MMD变形材质
    if 模型.parent.parent.mmd_root:
        if 模型.parent.parent.mmd_root.material_morphs:
            for 变形 in 模型.parent.parent.mmd_root.material_morphs:
                for 数据 in 变形.data:
                    if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
                        数据.material = f"{数据.material[:-4]}_{角色}"  # 应用材质原名称后，旧材质名称出现后缀，通过减去后缀名称替换MMD变形材质
                    else:
                        数据.material = 数据.material[:-4]  # 应用材质原名称后，旧材质名称出现后缀，通过减去后缀名称替换MMD变形材质
    bpy.ops.outliner.orphans_purge()  # 清除孤立数据

    # 材质图像重命名
    重命名图像 = set()
    def 重命名贴图(偏好, 节点, 角色):
        if 偏好.重命名资产 and 偏好.重命名贴图:  ############### 如果开启了连续导入 ###############
            图像 = 节点.image
            if 图像 and 图像 not in 重命名图像:
                重命名图像.add(图像)
                if 筛选图像(图像):
                    pass
                else:
                    图像.name += "_" + 角色  # 材质图像重命名

    def 递归节点组(节点组):
        for 节点 in 节点组.node_tree.nodes:
            if 节点.type == 'TEX_IMAGE':
                清理贴图(节点)
                重命名贴图(偏好, 节点, 角色)
            if 节点.type == 'GROUP':
                递归节点组(节点)

    # 清理材质图像
    for 材质 in 模型.data.materials:
        if 材质.node_tree:
            for 节点 in 材质.node_tree.nodes:
                if 节点.type == 'TEX_IMAGE':
                    清理贴图(节点)
                    重命名贴图(偏好, 节点, 角色)
                if 节点.type == 'GROUP':
                    递归节点组(节点)
                    # 清理MMD固有节点组
                    if 节点.node_tree.name.startswith("MMDTexUV") or 节点.node_tree.name.startswith("MMDShaderDev"):
                        名称, 后缀 = 剪去后缀(节点.node_tree.name)
                        if 后缀:
                            节点组 = bpy.data.node_groups.get(名称)
                            if 节点组:
                                节点.node_tree = 节点组
                            else:
                                节点.node_tree.name = 名称
    bpy.ops.outliner.orphans_purge()  # 清除孤立数据

    # 绑定头骨
    绑定(偏好, 模型, self)  # 必须在关联集合后

    if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
        for 材质 in 数据源.materials:
            if 材质.name not in 模型.data.materials:
                材质.name += "_" + 角色  # 描边材质重命名
        # for image in 数据源.images:
        #     if check_material_image_name(image):
        #         continue
        #     image.name = f"{image.name}_{角色}"  # 图像重命名  # 在清理材质图像时改变了属性，所以不可用
    if 偏好.重命名资产 and 偏好.重命名驱动物体:  ############### 如果开启了连续导入 ###############
        for 物 in 数据源.objects:
            物.name += "_" + 角色  # 驱动物体重命名
            if 物.type == "LIGHT":
                物.data.name += "_" + 角色  # 虚拟灯光数据块重命名
    if 偏好.重命名资产 and 偏好.重命名形态键:  ############### 如果开启了连续导入 ###############
        if 偏好.重命名形态键:  ############### 如果开启了连续导入 ###############
            if 模型.data.shape_keys:
                名称, 后缀 = 剪去后缀(模型.data.shape_keys.name)
                if 后缀:
                    模型.data.shape_keys.name = 名称
                模型.data.shape_keys.name += "_" + 角色  # 形态键重命名
        if 偏好.重命名动作:  ############### 如果开启了连续导入 ###############
            if 模型.data.shape_keys.animation_data and 模型.data.shape_keys.animation_data.action:
                名称, 后缀 = 剪去后缀(模型.data.shape_keys.animation_data.action.name)
                if 后缀:
                    模型.data.shape_keys.animation_data.action.name = 名称
                模型.data.shape_keys.animation_data.action.name += "_" + 角色