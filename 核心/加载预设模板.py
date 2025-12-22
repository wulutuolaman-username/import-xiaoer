# coding: utf-8

import bpy
from typing import cast
from ..通用.设置 import 渲染设置
from ..通用.灯光 import 灯光驱动
from ..图像.导入贴图 import 导入贴图
from ..材质.材质分类 import 材质分类
from ..材质.检测透明.材质面 import 获取材质面
from ..着色.材质.脸部着色 import 脸部着色
from ..着色.材质.五官着色 import 五官着色
from ..着色.材质.表情着色 import 表情着色
from ..着色.材质.小二好色 import 小二好色
from ..着色.节点.法线贴图转换 import 法线校正
from ..着色.节点.崩铁头发光照合并颜色 import 移除崩铁头发光照合并颜色
from ..着色.混合.混合透明 import MMDalpha
from ..几何.设置描边 import 设置描边
from ..通用.绑定 import 矩阵绑定
from ..属性.属性 import 小二预设模板属性
from ..偏好.偏好设置 import XiaoerAddonPreferences
from ..指针 import XiaoerObject, XiaoerMaterial, XiaoerNode, XiaoerShaderNodeTree, XiaoerGeometryNodeTree, XiaoerCompositorNodeTree

定位 = set()  # 1.1.0blender导入fbx可能有部分模型没有骨架修改器，如卡莲-原罪猎人

def 干翻小二(self:bpy.types.Operator, 偏好:XiaoerAddonPreferences, 模型:XiaoerObject, 游戏, 角色, 文件路径, 贴图路径):

    # 材质集合 = set()
    # def 添加材质(模型):
    #     for 材质 in 模型.data.materials:
    #         材质集合.add(材质)
    # 添加材质(模型)
    小二预设模板属性(模型.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
    if 模型.parent:
        # 骨架 = 模型.parent
        # if 骨架.type == 'ARMATURE' and len([网格 for 网格 in 骨架.children if 网格.type == 'MESH']) > 1:
        #     for 网格 in 骨架.children:
        #         if 网格.type == 'MESH':  # 面部定位
        #             添加材质(网格)
        小二预设模板属性(模型.parent.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        if 模型.parent.parent:
            小二预设模板属性(模型.parent.parent.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)

    # 设置辉光属性和色彩管理
    渲染设置()
    # if not 模型.小二预设模板.完成导入模板:
    # if not any(物体.小二预设模板.完成导入模板 for 物体 in 模型.parent.children if 模型.parent) and not 模型.小二预设模板.完成导入模板:  # 1.1.0fbx模型分离
    global 定位
    # 防止重复加载文件
    if not any(物体.小二预设模板.完成导入模板 for 物体 in bpy.data.objects) and not 模型.小二预设模板.完成导入模板:  # 1.1.0fbx模型分离
        # 追加预设文件的所有资产
        self.report({"INFO"}, f"{模型.name}加载预设模板" + str(文件路径) + "=================================================")
        with bpy.data.libraries.load(文件路径) as (数据源, 数据流):
            # 仅加载物体、材质和节点组
            数据流.objects = 数据源.objects
            数据流.materials = 数据源.materials
            数据流.node_groups = 数据源.node_groups
        # 追加物体移入选中网格的集合
        for 物体 in 数据源.objects:
            if 模型.users_collection:  # 检查选中模型是否在集合中
                模型.users_collection[0].objects.link(物体)  # 将驱动物体移入新集合
            if 物体.type == 'LIGHT':
                try:
                    灯光驱动(self, 物体)
                except:  # 1.1.0如果驱动失败
                    模型.select_set(True)
                    bpy.context.view_layer.objects.active = 模型
            if 物体.type == 'EMPTY':  # 1.1.0优化矩阵计算方式，不再出现X旋转-90°
                定位.add(物体)

        模型.select_set(True)
        bpy.context.view_layer.objects.active = 模型

        for 材质 in 数据源.materials:
            for 节点 in 材质.node_tree.nodes:
                节点: XiaoerNode
                小二预设模板属性(节点.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        # 收集节点组
        for 节点组 in 数据源.node_groups:
            选项 = 模型.小二预设模板.导入节点组.add()
            选项.节点组 = 节点组
            节点组:XiaoerShaderNodeTree | XiaoerGeometryNodeTree | XiaoerCompositorNodeTree
            for 节点 in 节点组.nodes:
                节点: XiaoerNode
                小二预设模板属性(节点.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
            小二预设模板属性(节点组.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        模型.小二预设模板.完成导入模板 = True

        for 物体 in 定位:  # 1.1.0fbx模型分离
            矩阵绑定(self, 模型, 物体)

    节点组列表 = []
    if 模型.小二预设模板.导入节点组:
        for 群组 in 模型.小二预设模板.导入节点组:
            节点组列表.append(群组.节点组)
    # elif 模型.parent:  # 1.1.0fbx模型分离
    #     for 物体 in 模型.parent.children:
    else:
        for 物体 in bpy.data.objects:
            物体:XiaoerObject
            if 物体.小二预设模板.导入节点组:
                for 群组 in 物体.小二预设模板.导入节点组:
                    节点组列表.append(群组.节点组)
                    选项 = 模型.小二预设模板.导入节点组.add()
                    选项.节点组 = 群组.节点组
                break

    # 1.1.0检测透明材质
    材质面 = 获取材质面(self, 偏好, 模型)

    透明贴图 = 导入贴图(self, 偏好, 模型, 贴图路径, 文件路径, 游戏, 角色)

    # 材质按名称分组，不一定分对
    五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质 = 材质分类(模型)
    self.report({"INFO"}, f"材质按名称分组结果----------------------------------------------------------------------------------")
    self.report({"INFO"}, f"五官材质分组: " + " ".join(材质.name for 材质 in 五官材质))
    self.report({"INFO"}, f"表情材质分组: " + " ".join(材质.name for 材质 in 表情材质))
    self.report({"INFO"}, f"头发材质分组: " + " ".join(材质.name for 材质 in 头发材质))
    # self.report({"INFO"}, f"脸材质: " + str(face_材质.name))
    self.report({"INFO"}, f"脸部材质分组: " + " ".join(材质.name for 材质 in 脸部材质))
    self.report({"INFO"}, f"皮肤材质分组: " + " ".join(材质.name for 材质 in 皮肤材质))
    self.report({"INFO"}, f"衣服材质分组: " + " ".join(材质.name for 材质 in 衣服材质))

    # 1.0.9先处理材质着色器，再处理几何节点组
    # 处理材质着色器
    self.report({"INFO"}, f"处理材质着色器-------------------------------------------------------------------------------------------")
    self.report({"INFO"}, f'脸部材质')
    for 材质 in 脸部材质:  # 脸材质
        脸部着色(self, 偏好, 节点组列表, 材质, 透明贴图, 游戏, 模型)
        # 小二预设模板属性(材质.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        # 小二预设模板属性(材质.node_tree.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
    self.report({"INFO"}, f'五官材质')
    for 材质 in 五官材质:  # 五官材质
        五官着色(self, 偏好, 节点组列表, 材质, 透明贴图, 游戏, 模型, 材质面)
        # 小二预设模板属性(材质.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        # 小二预设模板属性(材质.node_tree.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
    self.report({"INFO"}, f'表情材质')
    for 材质 in 表情材质:
        表情着色(self, 偏好, 节点组列表, 材质, 游戏, 模型)
        # 小二预设模板属性(材质.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        # 小二预设模板属性(材质.node_tree.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
    self.report({"INFO"}, f'头发材质')
    for 材质 in 头发材质:
        小二好色(self, 偏好, 节点组列表, 材质, 透明贴图, "头发",    "hair", 游戏, 模型, 材质面)
        # 小二预设模板属性(材质.node_tree.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        # 小二预设模板属性(材质.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
    self.report({"INFO"}, f'皮肤材质')
    for 材质 in 皮肤材质:
        小二好色(self, 偏好, 节点组列表, 材质, 透明贴图, "皮肤", "clothes", 游戏, 模型, 材质面)
        # 小二预设模板属性(材质.node_tree.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        # 小二预设模板属性(材质.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
    self.report({"INFO"}, f'衣服材质')
    for 材质 in 衣服材质:
        小二好色(self, 偏好, 节点组列表, 材质, 透明贴图, "衣服", "clothes", 游戏, 模型, 材质面)
        # 小二预设模板属性(材质.node_tree.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
        # 小二预设模板属性(材质.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
    for 材质 in 模型.data.materials:
        材质:XiaoerMaterial
        if 材质.小二预设模板.加载完成:
            节点树 = cast(XiaoerShaderNodeTree, 材质.node_tree)
            小二预设模板属性(材质.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
            小二预设模板属性(节点树.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)
            for 节点 in 材质.node_tree.nodes:
                节点:XiaoerNode
                小二预设模板属性(节点.小二预设模板, 贴图路径, 文件路径, 游戏, 角色)

    # 1.1.0法线校正
    法线校正()
    # 1.1.0颜色渐变为黑白后不需要再单独合并到红或绿通道
    移除崩铁头发光照合并颜色(游戏, 节点组列表)

    # 处理几何节点组
    self.report({"INFO"}, f"处理几何节点组------------------------------------------------------------------------------------------")
    设置描边(self, 模型, 节点组列表, 五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质)

    模型.小二预设模板.加载完成 = True
    if 模型.parent:
        模型.parent.小二预设模板.加载完成 = True
        if 模型.parent.parent:
            模型.parent.parent.小二预设模板.加载完成 = True

    if 透明材质:
        self.report({"INFO"}, "透明材质：\n" +
                    "\n".join(材质.name + (" 检测为透明材质" if 材质.小二预设模板.检测结果 else
                                          " MMD alpha < 1" if MMDalpha(材质) < 1 else
                                          " 表情材质" if 材质.小二预设模板.材质分类 == '表情' else
                                          " "
                                           ) for 材质 in 透明材质
                              )
                    )

    bpy.context.space_data.shading.type = 'RENDERED'  # type:ignore
    self.report({"OPERATOR"}, f"{模型.name}加载模板完成，信息面板查看加载模板过程")