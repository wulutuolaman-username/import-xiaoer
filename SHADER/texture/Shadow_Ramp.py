import bpy
import re

def shadow_ramp_texture(self,game,diffuse_image):
###################################################################################################
    if game == "原神":
        try:
            Shadow_Ramp_image = bpy.data.images[diffuse_image.name.replace("Diffuse", "Shadow_Ramp")]
            return Shadow_Ramp_image
        except KeyError as e:
            if "not found" in str(e):
                return None  # 如果不存在就跳过
            else:
                raise  # 其他错误继续抛出
###################################################################################################
    if game == "崩坏：星穹铁道":
        # 新正则表达式结构说明：
        # ^(.*_\d{2})_       -> 前缀包含两位数字 (如 Avatar_Fugue_00)
        # ([^_]+)            -> 部件类型 (Body/Hair/Tail等)
        # _Color(.*)\.png$   -> Color及其后缀
        match = re.match(r'^(.*_\d{2})_([^_]+)_Color(.*)\.png$', diffuse_image.name)
        if match:
            prefix, part_type, color_suffix = match.groups()
            # self.report({"INFO"}, f'基础贴图["{diffuse_image}"]\nprefix:{prefix}\npart_type:{part_type}')
            # 处理Ramp名称：部件后跟数字时不带部件类型
            if part_type[-1].isdigit():
                cool_ramp_name = f"{prefix}_Cool_Ramp.png"
                warm_ramp_name = f"{prefix}_Warm_Ramp.png"
                if warm_ramp_name not in bpy.data.images:
                    part_type = part_type[: -1]
                    cool_ramp_name = f"{prefix}_{part_type}_Cool_Ramp.png"
                    warm_ramp_name = f"{prefix}_{part_type}_Warm_Ramp.png"
                    if warm_ramp_name not in bpy.data.images:
                        cool_ramp_name = None
                        warm_ramp_name = f"{prefix}_{part_type}_Ramp.png"
            else:
                cool_ramp_name = f"{prefix}_{part_type}_Cool_Ramp.png"
                warm_ramp_name = f"{prefix}_{part_type}_Warm_Ramp.png"
                if warm_ramp_name not in bpy.data.images:
                    cool_ramp_name = f"{prefix}_{part_type}_Ramp.png"
                    warm_ramp_name = f"{prefix}_{part_type}_Ramp.png"
            # 检查文件是否存在
            try:
                # self.report({"INFO"}, f'cool_ramp_name:{cool_ramp_name }\nwarm_ramp_name:{warm_ramp_name}')
                cool_ramp = bpy.data.images[cool_ramp_name]
                warm_ramp = bpy.data.images[warm_ramp_name]
                return cool_ramp,warm_ramp
            except KeyError as e:
                if "not found" in str(e):
                    return None,None # 如果不存在就跳过
                else:
                    raise  # 其他错误继续抛出
        else:  # 可能不是角色贴图
            match = re.match(r"^(.*?_[A-Z]\d)_([^_]+)_Color(.*)\.png$", diffuse_image.name)
            if match:
                prefix, part_type, color_suffix = match.groups()
                # 处理Ramp名称：部件后跟数字时不带部件类型
                if part_type[-1].isdigit():
                    part_type = part_type[:-1]
                cool_ramp_name = f"{prefix}_{part_type}_Cool_Ramp.png"
                warm_ramp_name = f"{prefix}_{part_type}_Warm_Ramp.png"
                # 检查文件是否存在
                try:
                    cool_ramp = bpy.data.images[cool_ramp_name]
                    warm_ramp = bpy.data.images[warm_ramp_name]
                    return cool_ramp, warm_ramp
                except KeyError as e:
                    if "not found" in str(e):
                        return None, None  # 如果不存在就跳过
                    else:
                        raise  # 其他错误继续抛出
            else:
                return None, None  # 如果不存在就跳过
###################################################################################################