import os
import bpy
from bpy.props import StringProperty
from ...核心.加载预设模板 import 干翻小二
from ...通用.查找 import 查找贴图

class ExecuteTemplate(bpy.types.Operator):
    """ 选择游戏加载预设模板，设置描边材质，连接节点组 """
    bl_idname = "import_xiaoer.execute_template"
    bl_label = "加载预设模板"

    # 定义两个路径属性
    模板路径: StringProperty(subtype='FILE_PATH')
    贴图路径: StringProperty(subtype='FILE_PATH')  # 重命名为image_path

    @classmethod
    def poll(self, context):

        return context.object is not None and context.object.type == 'MESH'

    def invoke(self, context, event):
        偏好 = bpy.context.preferences.addons["导入小二"].preferences
        选中项 = 偏好.游戏列表[偏好.当前列表选项索引]
        偏好名称 = 选中项.名称.replace("：", "")
        文件路径 = getattr(偏好, f"{偏好名称}模板路径", None)
        if 文件路径 and os.path.exists(文件路径):
            self.模板路径 = 文件路径  # 传递模板路径
            if 偏好.导入贴图:
                贴图路径 = 偏好.贴图目录
                if 贴图路径 and os.path.exists(贴图路径):
                    pass
                elif not 贴图路径:
                    self.report({"WARNING"}, f"未设置贴图路径")
                    return {'CANCELLED'}  # 确保返回有效结果
                elif not os.path.exists(贴图路径):
                    self.report({"WARNING"}, f"贴图路径不存在")
                    return {'CANCELLED'}  # 确保返回有效结果
            return self.execute(context)
        elif not 文件路径:
            self.report({"WARNING"}, f"未设置{选中项.名称}预设模板路径")
            return {'CANCELLED'}  # 确保返回有效结果
        elif not os.path.exists(文件路径):
            self.report({"WARNING"}, f"{选中项.名称}预设模板路径不存在")
            return {'CANCELLED'}  # 确保返回有效结果

    def execute(self, context):
        偏好 = bpy.context.preferences.addons["导入小二"].preferences
        选中项 = 偏好.游戏列表[偏好.当前列表选项索引]
        游戏 = 选中项.名称
        模型 = bpy.context.object
        文件路径 = self.模板路径
        # self.report({"INFO"}, f"再次检查偏好路径：" + str(file_path))
        贴图路径 = None  # 初始化
        if 偏好.导入贴图:
            if 偏好.搜索贴图文件夹: # 如果开启了自动搜索贴图文件夹
                if not 偏好.贴图目录 and not os.path.exists(偏好.贴图目录):
                    self.report({"WARNING"}, f"未设置贴图路径或贴图路径不存在")
                    return None
                贴图路径, 角色 = 查找贴图(偏好, 模型)
                if 贴图路径 and 角色:
                    self.report({"INFO"}, "搜索到贴图文件夹名称："+str(角色))
                else:
                    self.report({"WARNING"}, f"未搜索到{模型.name}贴图")
                    return {'CANCELLED'}  # 确保返回有效结果
            else:  # 如果没有开启搜索贴图路径，那就是导入偏好路径下的贴图
                贴图路径 = 偏好.贴图目录
        if 文件路径:
            干翻小二(self, 偏好, 模型, 游戏, 文件路径, 贴图路径)
        return {'FINISHED'}