import bpy
from ...材质.材质分类 import 材质分类
from ...着色.材质.脸部着色 import 脸部着色
from ...着色.材质.五官着色 import 五官着色
from ...着色.材质.表情着色 import 表情着色
from ...着色.材质.小二好色 import 小二好色
from ...几何.设置描边 import 分类设置描边
from .清理节点 import 清理无用节点

def 更新材质(self, context):
    if self.材质分类 and self.更新分类 and self.材质分类 != self.更新分类:
        # bpy.ops.import_xiaoer.update_material_shader()
        偏好 = context.preferences.addons["导入小二"].preferences
        游戏 = 偏好.游戏列表[偏好.当前列表选项索引].名称
        模型 = context.active_object
        if 模型.type == 'MESH':
            节点组列表 = []
            if context.active_object and context.active_object.active_material:
                材质 = context.active_object.active_material
                # print(f'\n更新材质{材质.name} 为{self.材质分类}材质')
                材质.小二预设模板.混合模式 = 材质.blend_method
                材质.小二预设模板.显示背面 = 材质.show_transparent_back
                for 群组 in 模型.小二预设模板.导入节点组:
                    节点组列表.append(群组.节点组)
                # 材质集合 = set()
                # def 添加材质(模型):
                #     for 材质 in 模型.data.materials:
                #         材质集合.add(材质)
                # 添加材质(模型)
                # 骨架 = 模型.parent
                # if 骨架 and 骨架.type == 'ARMATURE' and len([网格 for 网格 in 骨架.children if 网格.type == 'MESH']) > 1:
                #     for 网格 in 骨架.children:
                #         if 网格.type == 'MESH':  # 面部定位
                #             添加材质(网格)
                五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质 = 材质分类(模型)
                if 材质.小二预设模板.材质分类 == '脸部':
                    脸部着色(self, 偏好, 节点组列表, 材质, None, 游戏, 模型)
                elif 材质.小二预设模板.材质分类 == '五官':
                    五官着色(self, 偏好, 节点组列表, 材质, None, 游戏, 模型, None)
                elif 材质.小二预设模板.材质分类 == '表情':
                    表情着色(self, 偏好, 节点组列表, 材质, 游戏, 模型)
                elif 材质.小二预设模板.材质分类 == '头发':
                    小二好色(self, 偏好, 节点组列表, 材质, None, "头发", "hair", 游戏, 模型, None)
                elif 材质.小二预设模板.材质分类 == '皮肤':
                    小二好色(self, 偏好, 节点组列表, 材质, None, "皮肤", "clothes", 游戏, 模型, None)
                elif 材质.小二预设模板.材质分类 == '衣服':
                    小二好色(self, 偏好, 节点组列表, 材质, None, "衣服", "clothes", 游戏, 模型, None)
                清理无用节点(材质)
                if not 材质.小二预设模板.透明材质:
                    材质.blend_method = 材质.小二预设模板.混合模式
                    材质.show_transparent_back = 材质.小二预设模板.显示背面
                实体化描边 = next((节点组 for 节点组 in 节点组列表 if "实体化描边" in 节点组.name), None)
                if 实体化描边:
                    分类设置描边(self, 实体化描边, 五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质)
        self.更新分类 = self.材质分类
    return None