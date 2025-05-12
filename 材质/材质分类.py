# coding: utf-8

# 材质按名称分组，不一定分对
def 材质分类(模型):
    # 1.02增加"袖"，英文全部小写
    # 1.03增加"声痕"、"body"、"发卡"
    眼口关键词 = ["眉","mei","睫","jie","二重","bai","眼","目","瞳","eye","Eye","hi","yinying",
                      "口","嘴","唇","mouth","kou","lip","牙","齿","齒","teeth","舌","tongue","she",
                      "痣"]
    眼口材质 = []

    表情关键词 = ["表情","biaoq","bq","emo","heart","星","star","❤","cheek","nose","脸红","照れ","> <","声痕"]
    表情材质 = []

    头发关键词 = ["发","髪","髮","辫","hair","bang","刘海","后脑勺","马尾","馬尾"]
    头发材质 = []

    脸关键词 = ["脸","颜","顏","面","face"]
    脸 = next((材质 for 材质 in 模型.data.materials if any(关键词 in 材质.name or 关键词 in 材质.name.lower() for 关键词 in 脸关键词)), None)  #1.0.3更新大小写匹配
    脸材质 = []  # 考虑到有些模型将脸分成多个材质

    皮肤关键词 = ["首","脖","kubi","皮肤","肌","skin","體","ear","hou","body"]
    皮肤材质 = []  # 在几何节点时可将脸材质并入皮肤材质同时输入；在着色节点时，处理脸材质后将其从皮肤材质中移除，然后处理皮肤材质

    # 反向过滤
    衣服关键词 =["面具","面罩","面襯","神之眼","眼罩","眼镜","饰","飾","绳","繩","纱","紗","带","帶","袖","发卡"]
    衣服材质 = []

    for 材质 in 模型.data.materials:

        是眼口 = any(关键词 in 材质.name or 关键词 in 材质.name.lower() for 关键词 in 眼口关键词)
        是表情 = any(关键词 in 材质.name or 关键词 in 材质.name.lower() for 关键词 in 表情关键词)
        是头发 = any(关键词 in 材质.name or 关键词 in 材质.name.lower() for 关键词 in 头发关键词)
        是脸 = any(关键词 in 材质.name or 关键词 in 材质.name.lower() for 关键词 in 脸关键词)
        是皮肤 = any(关键词 in 材质.name or 关键词 in 材质.name.lower() for 关键词 in 皮肤关键词)
        是衣服 = any(关键词 in 材质.name or 关键词 in 材质.name.lower() for 关键词 in 衣服关键词)

        if 是衣服:
            衣服材质.append(材质)
            continue  # 跳过后续判断
        if 是眼口:
            眼口材质.append(材质)
        elif 是表情:
            表情材质.append(材质)
        elif 是头发:
            头发材质.append(材质)
        elif 是脸:
            脸材质.append(材质)
        elif 是皮肤:
            皮肤材质.append(材质)
        else:
            衣服材质.append(材质)

    return 眼口材质, 表情材质, 头发材质, 脸, 脸材质, 皮肤材质, 衣服材质
