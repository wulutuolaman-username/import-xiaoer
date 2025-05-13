# coding: utf-8

import bpy
from ..通用.设置 import 渲染设置
from ..几何.几何节点 import 几何节点
from ..通用.清理 import 清理贴图
from ..图像.筛选贴图 import 筛选图像
from ..通用.绑定 import 绑定

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
                模型.parent.parent.animation_data.action.name += "_" + 角色
        for 子级 in 模型.parent.parent.children:
            if 偏好.独立集合:  ############### 如果开启了连续导入 ###############
                for 集合 in 子级.users_collection:
                    集合.objects.unlink(子级)  # 祖父级空物体的子级全部移出旧集合
                新集合.objects.link(子级)  # 祖父级空物体的子级全部移入新集合
            if 子级.name.startswith(模型.name.split("_mesh")[0]):  # 骨架
                if 偏好.重命名动作:  ############### 如果开启了连续导入 ###############
                    if 子级.animation_data and 子级.animation_data.action:
                        子级.animation_data.action.name += "_" + 角色
            else:  # 如果是刚体和关节的父级空物体
                if 偏好.重命名刚体和关节:  ############### 如果开启了连续导入 ###############
                    子级名 = 子级.name
                    if 子级名[-3:].isdigit():  # 如果有副本后缀
                        子级名 = 子级名[:-4]  # 剪去后缀
                    子级.name = f"{子级名}_{角色}"  # 祖父级空物体的子级物体重命名
                for 孙级 in 子级.children:
                    if 偏好.独立集合:  ############### 如果开启了连续导入 ###############
                        for 集合 in 孙级.users_collection:
                            集合.objects.unlink(孙级)  # 祖父级空物体的孙级全部移出旧集合
                        新集合.objects.link(孙级)  # 祖父级空物体的孙级全部移入新集合
                    if 偏好.重命名刚体和关节:  ############### 如果开启了连续导入 ###############
                        if 孙级 is 模型:
                            continue
                        孙级名 = 孙级.name
                        if 孙级名[-3:].isdigit():  # 如果有副本后缀
                            孙级名 = 孙级.name[:-4]  # 剪去后缀
                        孙级.name = f"{孙级名}_{角色}"  # 祖父级空物体的孙级物体重命名

    # 替换网格材质
    for i, 旧材质 in enumerate(模型.data.materials):  # 在网格中遍历旧材质
        if 旧材质:
            for 材质 in 数据源.materials:  # 在追加材质中遍历新材质
                新名 = 材质.name
                if 材质 and 材质.name[-3:].isdigit():  # 追加材质可能有后缀.001
                    新名 = 材质.name[:-4]
                新材质 = 材质  # 获取新材质
                if 旧材质.name == 新名 or 旧材质.name[:-4] == 新名: # 匹配材质名称
                    模型.data.materials[i] = 新材质  # 替换材质
                    新材质.name = 新名  # 应用材质原名称
                    if 偏好.重命名资产 and 偏好.重命名材质:  ############### 如果开启了连续导入 ###############
                        新材质.name += "_" + 角色  # 网格材质重命名
    # 替换MMD变形材质
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
                        if 节点.node_tree.name[-3:].isdigit():
                            新名 = 节点.node_tree.name[:-4]
                            新节点组 = bpy.data.node_groups.get(新名)
                            if 新节点组:
                                节点.node_tree = 新节点组
                            else:
                                节点.node_tree.name = 新名
    bpy.ops.outliner.orphans_purge()  # 清除孤立数据

    # 绑定头骨
    绑定(偏好, 模型)  # 必须在关联集合后

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
                if 模型.data.shape_keys.name[-3:].isdigit():
                    模型.data.shape_keys.name = 模型.data.shape_keys.name[:-4]
                模型.data.shape_keys.name += "_" + 角色  # 形态键重命名
        if 偏好.重命名动作:  ############### 如果开启了连续导入 ###############
            if 模型.data.shape_keys.animation_data and 模型.data.shape_keys.animation_data.action:
                模型.data.shape_keys.animation_data.action.name += "_" + 角色