import bpy, re
from .剪尾 import 剪去后缀
from ..图像.筛选贴图 import 筛选图像
from ..偏好.偏好设置 import XiaoerAddonPreferences
from ..指针 import XiaoerObject

重命名图像 = set()

def 重命名贴图(偏好:XiaoerAddonPreferences, 图像, 节点, 角色, 类型):
    if 偏好.重命名资产 and 偏好.重命名贴图:  ############### 如果开启了连续导入 ###############
        # self.report({'INFO'}, f"{图像}")
        if 图像 and 图像 not in 重命名图像:
            名称, 后缀 = 剪去后缀(图像.name)
            if not 筛选图像(图像):
                # 1.1.0mmd_tools导入的模型贴图的内存地址不同
                新图 = bpy.data.images.get(名称 + "_" + 角色)
                # self.report({'INFO'}, f"新图: {新图}")
                # self.report({'INFO'}, f"重命名前: {图像.name}")
                # if not 新图:
                #     新图 = bpy.data.images.new(名称 + "_" + 角色, width=1, height=1)
                    # 新图 = bpy.data.images.get(临时.name)  # 防止名称长度限制
                    # bpy.data.images.remove(临时)  # 删除临时图像
                if 新图 and 名称 != 新图.name:  # 防止同名不同内存地址的贴图被重复命名
                    # self.report({'INFO'}, f"新图名称: {新图.name}")
                    # 1.1.0分类处理
                    if 类型 == 'SHADER':
                        节点.image = 新图
                        # self.report({'INFO'}, f"输入新图: {节点.image.name}")
                    if 类型 == 'GEOMETRY':
                        输入接口 = next((s for s in 节点.inputs if s.name == 'Image'), None)
                        if 输入接口 and 输入接口.default_value:
                            输入接口.default_value = 新图  # 描边遮罩
                else:
                    # self.report({'INFO'}, f"图像数据: {图像}")
                    # self.report({'INFO'}, f"重命名前: {图像.name}")
                    图像.name = 名称 + "_" + 角色  # 材质图像重命名
                    # self.report({'INFO'}, f"重命名后: {图像.name}")
                    # self.report({'INFO'}, f"重命名为: {图像.name}")
                    重命名图像.add(图像)

# 1.1.0
def 模型名称处理(模型:XiaoerObject, 星穹铁道=False):
    if 模型.parent and 模型.parent.type == 'ARMATURE':
        if 模型.parent.parent:
            return 模型名称(模型.parent.parent, 星穹铁道)
        return 模型名称(模型.parent, 星穹铁道)
    return 模型名称(模型, 星穹铁道)
def 模型名称(模型:XiaoerObject, 星穹铁道):
    # 名称 = 模型.name
    名称, 后缀 = 剪去后缀(模型.name)
    # 替换 = str.maketrans('', '', '0123456789.')  # 创建翻译表，删除数字和点
    # 名称 = 名称.translate(替换)  # 移除数字和点
    名称 = 名称.replace("_arm", "")
    名称 = 名称.replace("_mesh", "")
    名称 = 名称.replace("【", "").replace("】", "")
    名称 = 名称.replace("-", "")
    名称 = 名称.replace(".", "")
    名称 = 名称.replace(" ", "")
    替换 = str.maketrans('', '', '0123456789')  # 创建翻译表，删除数字
    名称 = 名称.translate(替换)  # 移除数字
    # noinspection RegExpRedundantEscape
    去掉括号 = re.sub(r'[\(\（].*?[\)\）]', '', 名称).strip()  # 去掉括号及括号内内容
    if 去掉括号:
        名称 = 去掉括号
    if not 星穹铁道:
        名称 = 名称.replace("星穹铁道—", "")
        名称 = 名称.replace("星穹铁道", "")
    return 名称