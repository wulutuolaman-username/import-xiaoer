import os

def find_preset(prefs, model):
    if not prefs.user_path or not os.path.exists(prefs.user_path):
        return None

    for root, dirs, files in os.walk(prefs.user_path):
        for f in files:
            if f.endswith(".blend"):
                base_name = f[:-6]  # 去掉.blend后缀
                file_name = base_name.replace("渲染", "")  # 去除文件名"渲染"字样
                file_name = file_name.replace("预设", "")  # 去除文件名"预设"字样
                if file_name in model.name :  # 如果模型名称包含了处理以后的文件名
                    return os.path.join(root, f), file_name

# 自动查找贴图文件
def find_texture(prefs, model):
    if not prefs.texture_path or not os.path.exists(prefs.texture_path):
        return None

    match_name = model.name.replace("_mesh", "")
    match_name = match_name.replace("【", "")
    match_name = match_name.replace("】", "")
    for root, dirs, files in os.walk(prefs.texture_path):
        for dir in dirs:
            if dir in match_name:  # 如果处理后的模型名称包含了文件夹名称
                return os.path.join(root, dir),dir