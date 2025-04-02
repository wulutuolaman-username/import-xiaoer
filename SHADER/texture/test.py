import re


def find_related_textures(color_files, all_files):
    file_set = set(all_files)
    result = []

    for color_file in color_files:
        # 新正则表达式结构说明：
        # ^(.*_\d{2})_       -> 前缀包含两位数字 (如 Avatar_Fugue_00)
        # ([^_]+)            -> 部件类型 (Body/Hair/Tail等)
        # _Color(.*)\.png$   -> Color及其后缀
        match = re.match(r'^(.*_\d{2})_([^_]+)_Color(.*)\.png$', color_file)
        if not match:
            continue

        prefix, part_type, color_suffix = match.groups()

        # 处理LightMap后缀 ------------------------------------------------
        # 分解颜色后缀（如 "_A_L" -> ["A", "L"]）
        suffix_parts = [p for p in color_suffix.split('_') if p]

        # 只保留最后一个有效_L后缀
        lightmap_suffix = ""
        if suffix_parts and suffix_parts[-1] == 'L':
            lightmap_suffix = f"_{suffix_parts[-1]}"

        # 构建LightMap文件名（保留数字前缀）
        lightmap_name = f"{prefix}_{part_type}_LightMap{lightmap_suffix}.png"
        lightmap = lightmap_name if lightmap_name in file_set else None

        # 处理Ramp文件 ---------------------------------------------------
        # 判断是否为编号身体部件（Body后接数字）
        is_numbered_body = re.match(r'Body\d+', part_type)

        if is_numbered_body:
            # 编号身体部件：Ramp不带部件类型
            ramp_prefix = prefix
        else:
            # 常规部件：Ramp带部件类型
            ramp_prefix = f"{prefix}_{part_type}"

        # 生成Ramp文件名
        cool_ramp = f"{ramp_prefix}_Cool_Ramp.png"
        warm_ramp = f"{ramp_prefix}_Warm_Ramp.png"

        # 检查文件是否存在
        cool_ramp = cool_ramp if cool_ramp in file_set else None
        warm_ramp = warm_ramp if warm_ramp in file_set else None

        result.append({
            "Color": color_file,
            "LightMap": lightmap,
            "Cool_Ramp": cool_ramp,
            "Warm_Ramp": warm_ramp
        })

    return result


# 测试用例
test_files = [
    # 常规用例
    "Avatar_Fugue_00_Tail_Color.png",
    "Avatar_Fugue_00_Tail_LightMap.png",
    "Avatar_Fugue_00_Tail_Cool_Ramp.png",
    "Avatar_Fugue_00_Tail_Warm_Ramp.png",

    # 带_L后缀用例
    "Avatar_BlackSwan_01_Body_Color_L.png",
    "Avatar_BlackSwan_01_Body_LightMap_L.png",
    "Avatar_BlackSwan_01_Body_Cool_Ramp.png",
    "Avatar_BlackSwan_01_Body_Warm_Ramp.png",

    # 复杂后缀用例
    "Avatar_TheHerta_99_Body_Color_A_L.png",
    "Avatar_TheHerta_99_Body_LightMap_L.png",
    "Avatar_TheHerta_99_Body_Cool_Ramp.png",
    "Avatar_TheHerta_99_Body_Warm_Ramp.png",

    # 编号身体部件用例
    "Avatar_Kafka_03_Body2_Color.png",
    "Avatar_Kafka_03_Body2_LightMap.png",
    "Avatar_Kafka_03_Cool_Ramp.png",
    "Avatar_Kafka_03_Warm_Ramp.png"
]

color_files = [f for f in test_files if "_Color" in f]
results = find_related_textures(color_files, test_files)

# 打印验证结果
for i, item in enumerate(results, 1):
    print(f"Case {i}:")
    print(f"Color: {item['Color']}")
    print(f"LightMap: {item['LightMap']}")
    print(f"Cool_Ramp: {item['Cool_Ramp']}")
    print(f"Warm_Ramp: {item['Warm_Ramp']}")
    print("-" * 50)