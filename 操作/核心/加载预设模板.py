import os, bpy, traceback
from typing import cast
from ...核心.加载预设模板 import 干翻小二
from ...查找.查找贴图 import 查找贴图
from ...通用.改名 import 模型名称处理
from ...通用.路径 import 获取模型路径
from ...偏好.获取偏好 import 获取偏好
from ...偏好.获取游戏 import 获取游戏
from ...指针 import XiaoerObject
from ...通用.回调 import 回调

class XiaoerAddonExecuteTemplate(bpy.types.Operator):
    """ 只选中一个模型，选择游戏加载预设模板，设置描边材质，连接节点组 """
    bl_idname = "import_xiaoer.execute_template"
    bl_label = "加载预设模板"

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH' and context.mode == 'OBJECT' and len(context.selected_objects) == 1  # 1.1.0只支持一个模型

    def execute(self, context):
        模型 = cast(XiaoerObject, context.active_object)
        偏好 = 获取偏好()
        游戏 = 获取游戏()
        文件 = True
        文件路径 = getattr(偏好, 游戏.replace("：", "")+"模板路径", None)# 属性名称不支持冒号
        if 模型.小二预设模板.完成导入模板 == False:
            if 模型.小二预设模板.使用插件 == True:
                self.report({"WARNING"}, f"{模型.name}未完成导入模板")
            if   not 文件路径:
                self.report({"ERROR"}, f"未设置{游戏}预设模板路径")
                文件 = False
            elif not os.path.exists(文件路径):
                self.report({"ERROR"}, f"{游戏}预设模板路径无效 {文件路径}")
                文件 = False
            elif not os.path.splitext(文件路径)[1].lower().startswith('.blend'):
                self.report({"ERROR"}, f"{游戏}预设模板非blend文件")
                文件 = False
        # 角色 = 模型.name.replace("_mesh", "")
        角色 = 模型名称处理(模型)
        贴图 = True
        贴图路径 = None  # 初始化
        if 偏好.导入贴图:
            if 模型.小二预设模板.完成导入贴图 == False:
                if 模型.小二预设模板.使用插件 == True:
                    self.report({"WARNING"}, f"{模型.name}未完成导入贴图")
                if 偏好.贴图来源 == '搜索':  # 如果开启了自动搜索贴图文件夹
                    if   not 偏好.贴图目录:
                        self.report({"ERROR"}, f"偏好未设置贴图目录")
                        贴图 = False
                    elif not os.path.exists(偏好.贴图目录):
                        self.report({"ERROR"}, f"偏好贴图目录无效 {偏好.贴图目录}")
                        贴图 = False
                    else:
                        贴图路径, 角色 = 查找贴图(self, 偏好, 模型, 游戏)
                        if 贴图路径 and 角色:
                            self.report({"INFO"}, f"{模型.name}搜索到贴图文件夹名称：{角色}")
                        else:
                            角色 = 模型.name.replace("_mesh", "")
                            self.report({"ERROR"}, f"{偏好.贴图目录} 未搜索到 {角色} 贴图文件夹")
                            贴图 = False
                if 偏好.贴图来源 == '指定':  # 1.1.0如果没有开启搜索贴图路径，那就是导入偏好路径下的贴图
                    if   not 偏好.贴图文件夹:
                        self.report({"ERROR"}, f"未指定贴图路径")
                        贴图 = False
                    elif not os.path.exists(偏好.贴图文件夹):
                        self.report({"ERROR"}, f"指定贴图路径无效 {偏好.贴图文件夹}")
                        贴图 = False
                    else:
                        贴图路径 = 偏好.贴图文件夹
                        self.report({"INFO"}, f"指定贴图路径 {贴图路径}")
                if 偏好.贴图来源 == '模型':  # 1.1.0模型路径直接作为贴图路径
                    贴图路径 = 获取模型路径(self, 模型)
                    if 贴图路径:
                        if os.path.exists(贴图路径):
                            self.report({"INFO"}, f"使用模型路径：{贴图路径}")
                        else:
                            self.report({"ERROR"}, f"模型路径无效 {贴图路径}")
                            贴图 = False
                    else:
                        self.report({"ERROR"}, f"未找到{角色}模型路径")
                        贴图 = False
        if not 文件 or not 贴图:
            return {'CANCELLED'}  # 确保返回有效结果
        if not 模型.小二预设模板.完成导入模板 or (偏好.导入贴图 and not 模型.小二预设模板.完成匹配贴图) or not 模型.小二预设模板.加载完成:
            if 模型.小二预设模型.使用插件 == True:
                self.report({"INFO"}, f"{模型.name}已导入预设")
                return {'FINISHED'}
            if 模型.小二预设模板.加载完成 == True:
                self.report({"INFO"}, f"{模型.name}已加载模板，在物体属性面板取消加载完成状态可再次导入")
                return {'FINISHED'}
            try:
                回调(干翻小二, self, 偏好, 模型, 游戏, 角色, 文件路径, 贴图路径)
            except Exception as e:
                错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                self.report({"ERROR"}, f"{角色}加载预设模板过程出现异常，可向插件作者反馈错误信息\n"
                                       f"模板 {str(文件路径)}\n"
                                       f"贴图 {str(贴图路径)}\n"
                                       f"{错误信息}")
        return {'FINISHED'}