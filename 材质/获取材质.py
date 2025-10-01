def 获取材质(模型):
    材质集合 = set()
    def 添加材质(模型):
        for 材质 in 模型.data.materials:
            材质集合.add(材质)
    # 添加材质(模型)
    完成递归 = set()
    骨架 = 模型.parent
    # if 骨架 and 骨架.type == 'ARMATURE' and len([网格 for 网格 in 骨架.children if 网格.type == 'MESH']) > 1:
    if 骨架:
        def 递归(骨架):
            if 骨架 not in 完成递归:
                完成递归.add(骨架)
                for 网格 in 骨架.children:
                    if 网格.type == 'MESH' and 网格.mmd_type != 'RIGID_BODY':  # 排除面部定位和刚体
                        添加材质(网格)
                    elif 网格.children:
                        for 物体 in 网格.children:
                            递归(物体)
                if 骨架.parent:
                    递归(骨架.parent)
        递归(骨架)
    return 材质集合