# coding: utf-8

import bpy
from ..通用.设置 import 渲染设置
from ..通用.剪尾 import 剪去后缀
from ..通用.清理 import 清理贴图
from ..通用.灯光 import 灯光驱动
from ..通用.绑定 import 矩阵绑定
from ..几何.几何节点 import 几何节点
from ..通用.改名 import 重命名贴图
from ..通用.递归 import 递归着色节点组, 递归几何节点组
from ..属性.预设 import 小二预设模型属性, 小二预设材质属性, 小二预设贴图属性, 小二预设节点属性, 小二预设节点组属性

def 炒飞小二(self, 偏好, 模型, 文件路径, 角色, 数据源=None, 重命名=True):

    UV图层 = 模型.data.uv_layers.active
    if not UV图层:
        self.report({"ERROR"}, f"{模型.name}未找到活动UV图层")
        return None

    UV图层.name = "UVMap"  # 统一活动UV图层名称，以便几何节点正确访问
    小二预设模型属性(模型, 文件路径, 角色)
    if 模型.parent:
        小二预设模型属性(模型.parent, 文件路径, 角色)
        if 模型.parent.parent:
            小二预设模型属性(模型.parent.parent, 文件路径, 角色)
    self.report({"INFO"}, f"{模型.name}导入预设文件：{文件路径}")
    if not 数据源:
    # 追加预设文件的所有资产
        with bpy.data.libraries.load(文件路径) as (数据源, 数据流):
            排除 = {"workspaces", "screens"}
            for 属性 in dir(数据流):
                if 属性 not in 排除:  # 1.1.0排除屏幕和工作区
                    setattr(数据流, 属性, getattr(数据源, 属性))
    # for 节点组 in 数据源.node_groups:  # 1.1.0fbx模型分离
    #     # if 节点组.name in bpy.data.node_groups:
    #     #     self.report({"INFO"}, 节点组.name)
    #     # else:
    #     if 节点组.name not in bpy.data.node_groups:
    #         # 报告缺失的节点组名称
    #         self.report({'ERROR'}, f"几何节点组 '{节点组.name}' 已被移除或未加载！")
    for 节点组 in list(数据源.node_groups):
        try:
            _ = 节点组.name
        except:  # 移除无效节点组
            数据源.node_groups.remove(节点组)
    for 贴图 in list(数据源.images):
        try:
            _ = 贴图.name
        except:  # 移除无效节点组
            数据源.images.remove(贴图)

    # 设置辉光属性和色彩管理
    渲染设置()

    # self.report({"INFO"}, f"{数据源.node_groups}")

    # 应用几何节点
    for 节点组 in 数据源.node_groups:
        # self.report({"INFO"}, f"{节点组}")
        if 节点组.type == 'GEOMETRY' and (节点组.小二预设模板.应用修改器 == True or 节点组.users == 0):  # 未被使用的几何节点组
            几何节点(模型, 节点组)  # 应用几何节点
            for 节点 in 节点组.nodes:
                if 节点.type == 'GROUP':
                    递归几何节点组(self, 偏好, 数据源, 文件路径, 角色, 节点)
                小二预设节点属性(节点, 文件路径, 角色)
        if 节点组.name.startswith("MMDTexUV") or 节点组.name.startswith("MMDShaderDev"):
            continue  # 如果是MMD固有节点组，无需后续重命名
        if 偏好.重命名资产 and 偏好.重命名节点组 and 重命名:  ############### 如果开启了连续导入 ###############
            节点组.name += "_" + 角色  # 节点组重命名
        小二预设节点组属性(节点组, 文件路径, 角色)  # bpy.types.NodeTree
    for 节点组 in 数据源.node_groups:  # 1.1.0fbx模型分离
        if 节点组.users == 0:
            节点组.use_fake_user = True  # 必须在修改器之后
    for 材质 in 数据源.materials:
        if 材质.users == 0:
            材质.use_fake_user = True

    if 偏好.重命名资产 and 偏好.独立集合 and 重命名:  ############### 如果开启了连续导入 ###############
        # 将模型相关物体移入独立集合
        新集合 = bpy.data.collections.get(角色)
        if not 新集合:
            新集合 = bpy.data.collections.new(角色)  # 新建独立集合
        if 新集合.name not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(新集合)  # 关联到场景集合
        for 集合 in 模型.users_collection:
            集合.objects.unlink(模型)
        新集合.objects.link(模型)
        for 物体 in 数据源.objects:
            新集合.objects.link(物体)  # 将驱动物体移入新集合
        if 模型.parent and 模型.parent.parent:
            for 集合 in 模型.parent.parent.users_collection:
                集合.objects.unlink(模型.parent.parent)  # 祖父级空物体移出旧集合
            新集合.objects.link(模型.parent.parent)  # 祖父级空物体移入新集合
    if 偏好.重命名资产 and 重命名:  ############### 如果开启了连续导入 ###############
        if 偏好.重命名动作:  ############### 如果开启了连续导入 ###############
            if 模型.parent:
                if 模型.parent.parent:
                    动作 = 模型.parent.parent.animation_data
                else:
                    动作 = 模型.parent.animation_data
                if 动作 and 动作.action:
                    名称, 后缀 = 剪去后缀(动作.action.name)
                    if 后缀:
                        动作.action.name = 名称
                    动作.action.name += "_" + 角色
        if 模型.parent and 模型.parent.parent:
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
                                if 集合.name not in ['RigidBodyConstraints', 'RigidBodyWorld']:
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
            # 同名材质 = [m for m in 模型.data.materials if 剪去后缀(m.name)[0] == 名称]
            同名材质 = [
                m for m in 模型.data.materials
                if (
                    剪去后缀(m.name.replace(f'_{m.小二预设材质.角色}', '')
                    if m.小二预设材质.角色 and m.name.endswith(f'_{m.小二预设材质.角色}')  # 材质可能重命名
                    else m.name)[0] == 名称
                )
            ]
            if len(同名材质) > 1:
                同名集合.add(名称)
                模型同名材质列表.extend(同名材质)
    if len(同名集合) > 0:
        for 名称 in 同名集合:
            for 材质 in reversed(数据源.materials):
                if 剪去后缀(材质.name)[0] == 名称:
                    预设同名材质列表.append(材质)
        if len(模型同名材质列表) == len(预设同名材质列表):  # 1.1.0fbx模型存在多个材质槽共用相同材质
            for 模型材质, 预设材质 in zip(模型同名材质列表, 预设同名材质列表):
                for i, 材质 in enumerate(模型.data.materials):
                    if 材质 is 模型材质:
                        模型.data.materials[i] = 预设材质
                        模型材质角色 = 模型材质.小二预设材质.角色
                        if 模型材质角色 and 模型材质.name.endswith(f'_{模型材质角色}'):
                            模型材质.name = 模型材质.name.rsplit('_', 1)[0]  # 材质可能重命名
                        预设材质.name = 模型材质.name
                        # if 偏好.重命名资产 and 偏好.重命名材质 and 重命名:  ############### 如果开启了连续导入 ###############
                        #     预设材质.name += "_" + 角色  # 网格材质重命名
                        break

    # 替换网格材质
    for i, 模型材质 in enumerate(模型.data.materials):  # 在网格中遍历旧材质
        if 模型材质 not in 预设同名材质列表:
            名称1, 后缀1 = 剪去后缀(模型材质.name)  # 连续导入模型，材质会产生后缀
            模型材质角色 = 模型材质.小二预设材质.角色
            if 模型材质角色 and 名称1.endswith(f'_{模型材质角色}'):
                名称1 = 名称1.rsplit('_', 1)[0]  # 去掉材质重命名
            模型材质.name = 名称1
            for 预设材质 in 数据源.materials:  # 在追加材质中遍历新材质
                名称2, 后缀2 = 剪去后缀(预设材质.name)
                if 名称1 == 名称2: # 匹配材质名称
                    小二预设材质属性(预设材质, 文件路径, 角色)
                    模型.data.materials[i] = 预设材质  # 替换材质
                    预设材质.name = 名称1  # 应用材质原名称
                    预设材质.小二预设材质.导入完成 = True
                    # if 偏好.重命名资产 and 偏好.重命名材质 and 重命名:  ############### 如果开启了连续导入 ###############
                    #     预设材质.name += "_" + 角色  # 网格材质重命名
                    break
    # 替换MMD变形材质
    if 模型.parent and 模型.parent.parent and hasattr(模型.parent.parent, "mmd_root"):  # 1.1.1blender4.0似乎没有对应的mmd_tools插件
        if 模型.parent.parent.mmd_root.material_morphs:
            for 变形 in 模型.parent.parent.mmd_root.material_morphs:
                for 数据 in 变形.data:
                    # if 偏好.重命名资产 and 偏好.重命名材质 and 重命名:  ############### 如果开启了连续导入 ###############
                    #     数据.material = f"{数据.material[:-4]}_{角色}"  # 应用材质原名称后，旧材质名称出现后缀，通过减去后缀名称替换MMD变形材质
                    # else:
                    数据.material = 数据.material[:-4]  # 应用材质原名称后，旧材质名称出现后缀，通过减去后缀名称替换MMD变形材质
    bpy.ops.outliner.orphans_purge()  # 清除孤立数据

    # # 材质图像重命名
    # 重命名图像 = set()
    # def 重命名贴图(偏好, 节点, 角色):
    #     if 偏好.重命名资产 and 偏好.重命名贴图:  ############### 如果开启了连续导入 ###############
    #         图像 = 节点.image
    #         # self.report({'INFO'}, f"{图像}")
    #         if 图像 and 图像.name not in 重命名图像:
    #             if not 筛选图像(图像):
    #                 # 1.1.0mmd_tools导入的模型贴图的内存地址不同
    #                 新图 = bpy.data.images.get(图像.name + "_" + 角色)
    #                 # self.report({'INFO'}, f"新图: {新图}")
    #                 # self.report({'INFO'}, f"重命名前: {图像.name}")
    #                 if 新图 :  # 防止同名不同内存地址的贴图被重复命名
    #                     if 图像.name != 新图.name:
    #                         # self.report({'INFO'}, f"新图名称: {新图.name}")
    #                         节点.image = 新图
    #                         # self.report({'INFO'}, f"输入新图: {节点.image.name}")
    #                 else:
    #                     # self.report({'INFO'}, f"图像数据: {图像}")
    #                     # self.report({'INFO'}, f"重命名前: {图像.name}")
    #                     图像.name += "_" + 角色  # 材质图像重命名
    #                     # self.report({'INFO'}, f"重命名后: {图像.name}")
    #                     # self.report({'INFO'}, f"重命名为: {图像.name}")
    #                     重命名图像.add(图像.name)
    #
    # def 递归节点组(self, 节点组):
    #     for 节点 in 节点组.node_tree.nodes:
    #         if 节点.type == 'TEX_IMAGE':
    #             清理贴图(节点)
    #             重命名贴图(偏好, 节点, 角色)
    #             小二预设贴图属性(节点.image, 文件路径, 角色)
    #         if 节点.type == 'GROUP':
    #             if 节点.node_tree:  # 1.1.0增加检查
    #                 # self.report({"INFO"},f"递归节点组{节点.node_tree.name}")
    #                 递归节点组(self, 节点)
    #         小二预设节点属性(节点, 文件路径, 角色)

    # 清理材质图像
    for 材质 in 模型.data.materials:
        if 材质.node_tree:
            for 节点 in 材质.node_tree.nodes:
                if 节点.type == 'TEX_IMAGE':
                    图像 = 节点.image
                    if 图像:
                        名称, 后缀 = 剪去后缀(图像.name)
                        if 后缀 and "mmd" not in 节点.name:
                            图像.name = 名称  # 雷泽模型和预设都存在Avatar_Boy_Claymore_Razor_Tex_Body_Diffuse.png，但是内容不同
                        清理贴图(self, 图像, 节点, 数据源, 'SHADER')
                        重命名贴图(偏好, 图像, 节点, 角色, 'SHADER')
                        小二预设贴图属性(图像, 文件路径, 角色)
                if 节点.type == 'GROUP':
                    递归着色节点组(self, 偏好, 数据源, 文件路径, 角色, 节点)
                    # 清理MMD固有节点组
                    if 节点.node_tree.name.startswith("MMDTexUV") or 节点.node_tree.name.startswith("MMDShaderDev"):
                        名称, 后缀 = 剪去后缀(节点.node_tree.name)
                        if 后缀:
                            节点组 = bpy.data.node_groups.get(名称)
                            if 节点组:
                                # 1.1.1blender4.1出现替换MMD节点组后断连、输入参数重置
                                # 首先记录替换前的连接、输入参数
                                输入参数 = {}
                                输入连接 = {}
                                输出连接 = {}
                                输入数量 = len(节点.inputs)
                                输出数量 = len(节点.outputs)
                                if 输入数量 > 0:
                                    for i, 输入 in enumerate(节点.inputs):
                                        if 输入.is_linked:
                                            输入连接[i] = 输入.links[0].from_socket
                                        if 输入.bl_idname != "NodeSocketVirtual":
                                            输入参数[i] = 输入.default_value
                                if 输出数量 > 0:
                                    for i, 输出 in enumerate(节点.outputs):
                                        if 输出.is_linked:
                                            输出连接[i] = set()
                                            for 连接 in 输出.links:
                                                输出连接[i].add(连接.to_socket)
                                # 替换节点组
                                节点.node_tree = 节点组
                                # 如果连接断开，再恢复连接和输入参数
                                if 输入数量 > 0:
                                    for i in 输入参数:
                                        节点.inputs[i].default_value = 输入参数[i]
                                    for i in 输入连接:
                                        材质.node_tree.links.new(输入连接[i], 节点.inputs[i])
                                if 输出数量 > 0:
                                    for i in 输出连接:
                                        for 接口 in 输出连接[i]:
                                            材质.node_tree.links.new(节点.outputs[i], 接口)
                            else:
                                节点.node_tree.name = 名称
                小二预设节点属性(节点, 文件路径, 角色)
            小二预设节点组属性(材质.node_tree, 文件路径, 角色)  # bpy.types.NodeTree
    bpy.ops.outliner.orphans_purge()  # 清除孤立数据

    # 1.0.7确保驱动物体在模型集合中
    for 物体 in 数据源.objects:
        if 物体.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(物体)  # 手动加入场景
        if 模型.users_collection:  # 检查选中模型是否在集合中
            for 集合 in 物体.users_collection:
                集合.objects.unlink(物体)
            模型.users_collection[0].objects.link(物体)  # 将驱动物体移入模型集合
        if 物体.type == 'LIGHT':
            try:
                灯光驱动(self, 物体)
            except:  # 1.1.0如果驱动失败
                模型.select_set(True)
                bpy.context.view_layer.objects.active = 模型
        if 物体.type == 'EMPTY':  # 1.1.0 传入定位
            try:
                矩阵绑定(self, 模型, 物体)  # 必须在关联集合后
            except:  # 1.1.0如果绑定失败
                模型.select_set(True)
                bpy.context.view_layer.objects.active = 模型

    模型.小二预设模型.导入完成 = True
    # if 模型.parent:
    #     模型.parent.小二预设模型.导入完成 = True
    #     if 模型.parent.parent:
    #         模型.parent.parent.小二预设模型.导入完成 = True

    if 偏好.重命名资产 and 偏好.重命名材质 and 重命名:  ############### 如果开启了连续导入 ###############
        for 材质 in 数据源.materials:
            # if 材质.name not in 模型.data.materials:
                # 材质.name += "_" + 角色  # 描边材质重命名
            名称, 后缀 = 剪去后缀(材质.name)
            材质.name = 名称 + "_" + 角色  # 材质重命名
        # for image in 数据源.images:
        #     if check_material_image_name(image):
        #         continue
        #     image.name = f"{image.name}_{角色}"  # 图像重命名  # 在清理材质图像时改变了属性，所以不可用
    if 偏好.重命名资产 and 偏好.重命名驱动物体 and 重命名:  ############### 如果开启了连续导入 ###############
        for 物体 in 数据源.objects:
            名称, 后缀 = 剪去后缀(物体.name)
            物体.name = 名称 + "_" + 角色  # 驱动物体重命名
            if 物体.type == "LIGHT":
                名称, 后缀 = 剪去后缀(物体.data.name)
                物体.data.name = 名称 + "_" + 角色  # 虚拟灯光数据块重命名
    if 偏好.重命名资产 and 偏好.重命名形态键:  ############### 如果开启了连续导入 ###############
        if 偏好.重命名形态键:  ############### 如果开启了连续导入 ###############
            if 模型.data.shape_keys:
                名称, 后缀 = 剪去后缀(模型.data.shape_keys.name)
                if 后缀:
                    模型.data.shape_keys.name = 名称
                模型.data.shape_keys.name += "_" + 角色  # 形态键重命名
        if 偏好.重命名动作:  ############### 如果开启了连续导入 ###############
            if 模型.data.shape_keys and 模型.data.shape_keys.animation_data and 模型.data.shape_keys.animation_data.action:
                名称, 后缀 = 剪去后缀(模型.data.shape_keys.animation_data.action.name)
                if 后缀:
                    模型.data.shape_keys.animation_data.action.name = 名称
                模型.data.shape_keys.animation_data.action.name += "_" + 角色

    bpy.ops.outliner.orphans_purge()  # 清除孤立数据
    self.report({"OPERATOR"}, f"{模型.name}完成预设导入")

    骨架 = 模型.parent
    # if 骨架 and 骨架.type == 'ARMATURE' and len([模型 for 模型 in 骨架.children if 模型.type == 'MESH']) > 1:
    if 骨架:
        def 递归(骨架):
            if not 骨架.小二预设模型.导入完成:
                骨架.小二预设模型.导入完成 = True
                for 模型 in 骨架.children:  # 1.1.0fbx模型分离
                    if 模型.type == 'MESH' and not 模型.rigid_body:  # 排除面部定位和刚体
                        炒飞小二(self, 偏好, 模型, 文件路径, 角色, 数据源, 重命名=False)
                    elif 模型.children:
                        for 物体 in 模型.children:
                            递归(物体)
                if 骨架.parent:
                    递归(骨架.parent)
        递归(骨架)

    # # 1.1.0清除导入的屏幕和工作区
    # for 工作区 in 数据源.workspaces:
    #     临时 = {'workspace': 工作区}  # 创建临时上下文删除工作区
    #     bpy.ops.workspace.delete(临时)  # 删除当前工作区
        # self.report({'INFO'}, f"删除工作区: {工作区.name}")
        # 临时 = {'workspace': 工作区}  # 创建临时上下文删除工作区
        # bpy.ops.workspace.delete(临时)  # 删除当前工作区
        # 目前只有这种方式能删除工作区，但是被删除的工作区仍然使用屏幕
        #
        # 工作区.screens = [bpy.context.workspace.screens]
        # AttributeError: bpy_struct: attribute "screens" from "WorkSpace" is read - only
        #
        # 工作区.screens.clear()
        # AttributeError: 'bpy_prop_collection' object has no attribute 'clear'
        # bpy.ops.screen.delete()无法删除屏幕，因为屏幕仍被已删除的工作区使用
        # bpy.ops.screen.delete(override)将会闪退
        #
        # bpy.data.screens.remove(屏幕)
        # AttributeError: 'bpy_prop_collection' object has no attribute 'remove'
        #
        # 工作区.screens.remove(屏幕)
        # AttributeError: 'bpy_prop_collection' object has no attribute 'remove'
        #
        # bpy.ops.outliner.orphans_purge(do_recursive=True)  # 脚本触发无法删除未使用的屏幕，只有手动点击才能清除未使用的屏幕
        #
        # 如何通过bpy脚本删除屏幕？