import os, bpy, traceback
from bpy.props import StringProperty
from ...核心.加载预设模板 import 干翻小二
from ...查找.查找贴图 import 查找贴图
from ...通用.改名 import 模型名称处理
from ...通用.路径 import 获取模型路径
from ...偏好.获取偏好 import 获取偏好

class ExecuteTemplate(bpy.types.Operator):
    """ 只选中一个模型，选择游戏加载预设模板，设置描边材质，连接节点组 """
    bl_idname = "import_xiaoer.execute_template"
    bl_label = "加载预设模板"

    # 定义两个路径属性
    模板路径: StringProperty(subtype='FILE_PATH')
    贴图路径: StringProperty(subtype='FILE_PATH')  # 重命名为image_path

    @classmethod
    def poll(self, context):
        return context.object is not None and context.object.type == 'MESH' and context.mode == 'OBJECT' and len(context.selected_objects) == 1  # 1.1.0只支持一个模型

    # def invoke(self, context, event):
    #     偏好 = bpy.context.preferences.addons["导入小二"].preferences
    #     选项 = 偏好.游戏列表[偏好.当前列表选项索引]
    #     游戏 = 选项.名称.replace("：", "")
    #     文件路径 = getattr(偏好, f"{游戏}模板路径", None)
    #     if 文件路径 and os.path.exists(文件路径):
    #         self.模板路径 = 文件路径  # 传递模板路径
    #         return self.execute(context)  # 1.1.0优化逻辑
    #     elif not 文件路径:
    #         self.report({"WARNING"}, f"未设置{选项.名称}预设模板路径")
    #         return {'CANCELLED'}  # 确保返回有效结果
    #     elif not os.path.exists(文件路径):
    #         self.report({"WARNING"}, f"{选项.名称}预设模板路径不存在")
    #         return {'CANCELLED'}  # 确保返回有效结果

    def execute(self, context):
        模型 = bpy.context.active_object
        偏好 = 获取偏好()
        选项 = 偏好.游戏列表[偏好.当前列表选项索引]
        游戏 = 选项.名称.replace("：", "")  # 属性名称不支持冒号
        文件 = True
        文件路径 = getattr(偏好, f"{游戏}模板路径", None)
        if 模型.小二预设模板.完成导入模板 == False:
            if 模型.小二预设模板.使用插件 == True:
                self.report({"WARNING"}, f"{模型.name}未完成导入模板")
            if   not 文件路径:
                self.report({"ERROR"}, f"未设置{选项.名称}预设模板路径")
                文件 = False
            elif not os.path.exists(文件路径):
                self.report({"ERROR"}, f"{选项.名称}预设模板路径无效 {文件路径}")
                文件 = False
            elif not os.path.splitext(文件路径)[1].lower().startswith('.blend'):
                self.report({"ERROR"}, f"{选项.名称}预设模板非blend文件")
                文件 = False
        游戏 = 选项.名称
        # 角色 = 模型.name.replace("_mesh", "")
        角色 = 模型名称处理(模型)
        贴图 = True
        贴图路径 = None  # 初始化
        if 偏好.导入贴图:
            if 模型.小二预设模板.完成导入贴图 == False:
                if 模型.小二预设模板.使用插件 == True:
                    self.report({"WARNING"}, f"{模型.name}未完成导入贴图")
                if 偏好.搜索贴图文件夹:  # 如果开启了自动搜索贴图文件夹
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
                if 偏好.指定贴图文件夹:  # 1.1.0如果没有开启搜索贴图路径，那就是导入偏好路径下的贴图
                    if   not 偏好.贴图文件夹:
                        self.report({"ERROR"}, f"未指定贴图路径")
                        贴图 = False
                    elif not os.path.exists(偏好.贴图文件夹):
                        self.report({"ERROR"}, f"指定贴图路径无效 {偏好.贴图文件夹}")
                        贴图 = False
                    else:
                        贴图路径 = 偏好.贴图文件夹
                        self.report({"INFO"}, f"指定贴图路径 {贴图路径}")
                if 偏好.使用模型路径:  # 1.1.0模型路径直接作为贴图路径
                    贴图路径 = 获取模型路径(self, 模型)
                    if 贴图路径:
                    # if 模型.parent and 模型.parent.parent and 模型.parent.parent["import_folder"]:  # mmd_tools导入的模型
                    #     贴图路径 = 模型.parent.parent["import_folder"]  # mmd_tools导入模型具有此属性
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
                骨架 = 模型.parent
                # if 骨架 and 骨架.type == 'ARMATURE' and len([模型 for 模型 in 骨架.children if 模型.type == 'MESH']) > 1:
                if 骨架:
                    def 递归(骨架):
                        # self.report({"INFO"}, f"{骨架.name} {骨架.type}")
                        if not 骨架.小二预设模板.加载完成:
                            import datetime
                            # self.report({"INFO"}, f"当前递归 {骨架.name} {datetime.datetime.now()}")
                            骨架.小二预设模板.加载完成 = True
                            for 模型 in 骨架.children:
                                # self.report({"INFO"}, f"{骨架.name} 当前子级 {模型.name} {datetime.datetime.now()}")
                                if 模型.type == 'MESH' and not 模型.rigid_body:  # 排除面部定位和刚体
                                    # self.report({"INFO"}, f"{骨架.name} 子级网格 {模型.name} {datetime.datetime.now()}")
                                    干翻小二(self, 偏好, 模型, 游戏, 角色, 文件路径, 贴图路径)
                                elif 模型.children:
                                    for 物体 in 模型.children:
                                        # self.report({"INFO"}, f"{骨架.name} 当前孙级 {物体.name} {datetime.datetime.now()}")
                                        递归(物体)
                            if 骨架.parent:
                                # self.report({"INFO"}, f"{骨架.name} 当前父级 {骨架.parent.name} {datetime.datetime.now()}")
                                递归(骨架.parent)
                    递归(骨架)
                else:
                    干翻小二(self, 偏好, 模型, 游戏, 角色, 文件路径, 贴图路径)
            except Exception as e:
                错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                self.report({"ERROR"}, f"{角色}加载预设模板过程出现异常，可向插件作者反馈错误信息\n"
                                       f"模板 {str(文件路径)}\n"
                                       f"贴图 {str(贴图路径)}\n"
                                       f"{错误信息}")
        return {'FINISHED'}