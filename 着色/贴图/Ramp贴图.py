# coding: utf-8

import bpy
import re

def 获取Ramp贴图(self, 游戏, 基础贴图):
###################################################################################################
    if 游戏 == "原神":
        try:
            Ramp贴图 = bpy.data.images[基础贴图.name.replace("Diffuse", "Shadow_Ramp")]
            return Ramp贴图
        except KeyError as e:
            if "not found" in str(e):
                return None  # 如果不存在就跳过
            else:
                raise  # 其他错误继续抛出
###################################################################################################
    if 游戏 == "崩坏：星穹铁道":
        # 新正则表达式结构说明：
        # ^(.*_\d{2})_       -> 前缀包含两位数字 (如 Avatar_Fugue_00)
        # ([^_]+)            -> 部件类型 (Body/Hair/Tail等)
        # _Color(.*)\.png$   -> Color及其后缀
        分解 = re.match(r'^(.*_\d{2})_([^_]+)_Color(.*)\.png$', 基础贴图.name)
        if 分解:
            前缀, 部件, 后缀 = 分解.groups()
            # self.report({"INFO"}, f'基础贴图["{diffuse_image}"]\nprefix:{prefix}\npart_type:{part_type}')
            # 处理Ramp名称：部件后跟数字时不带部件类型
            if 部件[-1].isdigit():
                冷名 = f"{前缀}_Cool_Ramp.png"
                暖名 = f"{前缀}_Warm_Ramp.png"
                if 暖名 not in bpy.data.images:
                    部件 = 部件[: -1]
                    冷名 = f"{前缀}_{部件}_Cool_Ramp.png"
                    暖名 = f"{前缀}_{部件}_Warm_Ramp.png"
                    if 暖名 not in bpy.data.images:
                        冷名 = None
                        暖名 = f"{前缀}_{部件}_Ramp.png"
            else:
                冷名 = f"{前缀}_{部件}_Cool_Ramp.png"
                暖名 = f"{前缀}_{部件}_Warm_Ramp.png"
                if 暖名 not in bpy.data.images:
                    冷名 = f"{前缀}_{部件}_Ramp.png"
                    暖名 = f"{前缀}_{部件}_Ramp.png"
            # 检查文件是否存在
            try:
                # self.report({"INFO"}, f'cool_ramp_name:{cool_ramp_name }\nwarm_ramp_name:{warm_ramp_name}')
                冷Ramp = bpy.data.images[冷名]
                暖Ramp = bpy.data.images[暖名]
                return 冷Ramp,暖Ramp
            except KeyError as e:
                if "not found" in str(e):
                    return None,None # 如果不存在就跳过
                else:
                    raise  # 其他错误继续抛出
        else:  # 可能不是角色贴图
            分解 = re.match(r"^(.*?_[A-Z]\d)_([^_]+)_Color(.*)\.png$", 基础贴图.name)
            if 分解:
                前缀, 部件, 后缀 = 分解.groups()
                # 处理Ramp名称：部件后跟数字时不带部件类型
                if 部件[-1].isdigit():
                    部件 = 部件[:-1]
                冷名 = f"{前缀}_{部件}_Cool_Ramp.png"
                暖名 = f"{前缀}_{部件}_Warm_Ramp.png"
                # 检查文件是否存在
                try:
                    冷Ramp = bpy.data.images[冷名]
                    暖Ramp = bpy.data.images[暖名]
                    return 冷Ramp, 暖Ramp
                except KeyError as e:
                    if "not found" in str(e):
                        return None, None  # 如果不存在就跳过
                    else:
                        raise  # 其他错误继续抛出
            else:
                return None, None  # 如果不存在就跳过
###################################################################################################