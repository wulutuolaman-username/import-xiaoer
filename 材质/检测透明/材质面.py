import bpy, bmesh
from collections import defaultdict
from ...偏好.偏好设置 import XiaoerAddonPreferences

# 1.1.0检测透明材质
def 获取材质面(self:bpy.types.Operator, 偏好:XiaoerAddonPreferences, 模型:bpy.types.Object, 手动检测=False):
    UV图层 = 模型.data.uv_layers.active
    if not UV图层:
        self.report({"ERROR"}, f"{模型.name}未找到活动UV图层")
        return None
    UV图层.name = "UVMap"  # 统一活动UV图层名称，以便几何节点正确访问
    if not 模型.data.materials:
        self.report({"ERROR"}, f"{模型.name}没有材质")
        return None
    if 偏好.检测透明材质 or 手动检测:
        bm = bmesh.new()
        bm.from_mesh(模型.data)
        UV图层 = bm.loops.layers.uv.active
        材质面 = defaultdict(list)
        材质面去重 = defaultdict(list)
        # 材质面索引 = defaultdict(list)
        材质面索引 = defaultdict(set)  # 集合自动去重
        for 面 in bm.faces:
            材质索引 = 面.material_index
            材质 = 模型.data.materials[材质索引]
            面顶点 = [(loop[UV图层].uv.x, loop[UV图层].uv.y) for loop in 面.loops]
            # for 循环 in 面.loops:
            #     UV坐标 = 循环[UV图层].uv
            #     # x = UV坐标.x % 1  # 规范化到[0,1]
            #     # y = UV坐标.y % 1  # 规范化到[0,1]
            #     # 面数据['UV坐标'].append((x, y))
            #     面顶点.append((UV坐标.x, UV坐标.y))
            if all(x // 1 != 0 or y // 1 != 0 for x, y in 面顶点):  # 黄泉的裤材质最顶上的点超过1
                x_偏移, y_偏移 = zip(*((x // 1, y // 1) for x, y in 面顶点))
                计数 = {}
                for x_ in x_偏移:
                    for y_ in y_偏移:
                        面内 = sum(1 for x, y in 面顶点 if 0 <= x - x_ < 1 and 0 <= y - y_ < 1)
                        计数[面内] = (x_, y_)
                x_偏移, y_偏移 = 计数[max(计数)]
                面顶点 = [(loop[UV图层].uv.x - x_偏移, loop[UV图层].uv.y - y_偏移) for loop in 面.loops]
            # 可能有同样的顶点坐标但相反顶点排序的重合面，分别在不同材质里
            if sorted(面顶点) not in 材质面去重[材质]:
                材质面去重[材质].append(sorted(面顶点))
                材质面[材质].append(面顶点)
        return 材质面
    return None