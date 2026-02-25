from typing import TYPE_CHECKING
from ...指针 import *  # noqa: F401

if TYPE_CHECKING:
    from ...属性.材质 import XiaoerAddonMaterialPresetsTemplateInformation
# 前向引用
# Python 不会在运行时解析这个名字
# 只是把它当成字符串保存
# IDE / 类型检查器会解析
# Blender 运行时完全无感知
def 更新材质(self:"XiaoerAddonMaterialPresetsTemplateInformation", context):
    if self.材质分类 and self.更新分类 and self.材质分类 != self.更新分类:
        from ...偏好.获取偏好 import 获取偏好
        from ...偏好.获取游戏 import 获取游戏
        from ...指针 import 小二材质
        偏好 = 获取偏好()
        游戏 = 获取游戏()
        模型 = context.active_object  # type:小二物体
        if 模型.判断类型.物体.是网格:
            材质 = 模型.active_material  # type:小二材质|bpy.types.Material
            if 材质:
                节点组列表 = []
                # print(f'\n更新材质{材质.name} 为{self.材质分类}材质')
                材质.小二预设模板.混合模式 = 材质.blend_method
                材质.小二预设模板.显示背面 = 材质.show_transparent_back
                for 群组 in 模型.小二预设模板.导入节点组:
                    节点组列表.append(群组.节点组)

                from ...材质.材质分类 import 材质分类
                五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质 = 材质分类(模型)

                from ...着色.材质.脸部着色 import 脸部着色
                from ...着色.材质.五官着色 import 五官着色
                from ...着色.材质.表情着色 import 表情着色
                from ...着色.材质.小二好色 import 小二好色
                if   材质.小二预设模板.材质分类 == '脸部':
                    脸部着色(None, 偏好, 节点组列表, 材质, None, 游戏, 模型)
                elif 材质.小二预设模板.材质分类 == '五官':
                    五官着色(None, 偏好, 节点组列表, 材质, None, 游戏, 模型, None)
                elif 材质.小二预设模板.材质分类 == '表情':
                    表情着色(None, 偏好, 节点组列表, 材质, 游戏, 模型)
                elif 材质.小二预设模板.材质分类 == '头发':
                    小二好色(None, 偏好, 节点组列表, 材质, None, "头发", "hair", 游戏, 模型, None)
                elif 材质.小二预设模板.材质分类 == '皮肤':
                    小二好色(None, 偏好, 节点组列表, 材质, None, "皮肤", "clothes", 游戏, 模型, None)
                elif 材质.小二预设模板.材质分类 == '衣服':
                    小二好色(None, 偏好, 节点组列表, 材质, None, "衣服", "clothes", 游戏, 模型, None)

                from .清理节点 import 清理无用节点
                清理无用节点(材质)

                if not 材质.小二预设模板.透明材质:
                    材质.blend_method = 材质.小二预设模板.混合模式
                    材质.show_transparent_back = 材质.小二预设模板.显示背面
                实体化描边 = next((节点组 for 节点组 in 节点组列表 if "实体化描边" in 节点组.name), None)

                if 实体化描边:
                    from ...几何.设置描边 import 分类设置描边
                    分类设置描边(None, 实体化描边, 五官材质, 表情材质, 头发材质, 脸, 脸部材质, 皮肤材质, 衣服材质, 透明材质)

        self.更新分类 = self.材质分类
    return None