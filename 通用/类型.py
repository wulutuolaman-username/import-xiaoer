# 1.2.0闭包判断类型
def 是(对象, 类型) -> bool:
    # isinstance(对象, bpy.types.ID)
    # bpy.types.ID 是所有可独立存在于 bpy.data 里的数据块基类，Node、NodeSocket、Modifier不属于bpy.types.ID
    # hasattr(对象, "type")
    # 排除没有type属性的Preferences、Operator
    return 对象 and hasattr(对象, "type") and 对象.type == 类型

class 对象:
    # __slots__ = ('_对象',)
    def __init__(self, 对象): self._对象 = 对象

# ── 运行时真正执行的判断器 ──
class 编辑判断器(对象):
    @property
    def 是3D视图(self) -> bool:   return 是(self._对象, 'VIEW_3D')
    @property
    def 是UV或图像编辑器(self) -> bool:   return 是(self._对象, 'IMAGE_EDITOR')  # ui_type = 'UV' or 'IMAGE_EDITOR'

class 分区判断器(对象):
    @property
    def 是UI面板(self) -> bool:   return 是(self._对象, 'UI')

class 物体判断器(对象):
    @property
    def 是网格(self) -> bool:   return 是(self._对象, 'MESH')
    @property
    def 是灯光(self) -> bool:   return 是(self._对象, 'LIGHT')
    @property
    def 是相机(self) -> bool:   return 是(self._对象, 'CAMERA')
    @property
    def 是骨架(self) -> bool:   return 是(self._对象, 'ARMATURE')
    @property
    def 是空物体(self) -> bool:  return 是(self._对象, 'EMPTY')

class 修改器判断器(对象):
    @property
    def 是骨架修改器(self) -> bool:  return 是(self._对象, 'ARMATURE')
    @property
    def 是几何节点修改器(self) -> bool:  return 是(self._对象, 'NODES')

class 节点树判断器(对象):
    @property
    def 是着色节点树(self) -> bool:  return 是(self._对象, 'SHADER')
    @property
    def 是几何节点树(self) -> bool:  return 是(self._对象, 'GEOMETRY')

class 着色节点判断器(对象):
    @property
    def 是图像(self) -> bool:     return 是(self._对象, 'TEX_IMAGE')
    @property
    def 是材质输出(self) -> bool:  return 是(self._对象, 'OUTPUT_MATERIAL')
    @property
    def 是合并XYZ(self) -> bool:  return 是(self._对象, 'COMBXYZ')
    @property
    def 是法线贴图(self) -> bool:  return 是(self._对象, 'NORMAL_MAP')

class 几何节点判断器(对象):
    @property
    def 是图像(self) -> bool:      return 是(self._对象, 'IMAGE_TEXTURE')
    @property
    def 是设置材质(self) -> bool:   return 是(self._对象, 'SET_MATERIAL')
    @property
    def 是材质选择(self) -> bool:   return 是(self._对象, 'MATERIAL_SELECTION')
    @property
    def 是物体信息(self) -> bool:   return 是(self._对象, 'OBJECT_INFO')
    @property
    def 是删除几何体(self) -> bool: return 是(self._对象, 'DELETE_GEOMETRY')
    @property
    def 是合并XYZ(self) -> bool:  return 是(self._对象, 'COMBXYZ')
    @property
    def 是预览器(self) -> bool:  return 是(self._对象, 'VIEWER')

class 合成节点判断器(对象):
    @property
    def 是合成(self) -> bool:    return 是(self._对象, 'COMPOSITE')
    @property
    def 是渲染层(self) -> bool:   return 是(self._对象, 'R_LAYERS')
    @property
    def 是辉光(self) -> bool:     return 是(self._对象, 'GLARE')
    @property
    def 是合并XYZ(self) -> bool:  return 是(self._对象, 'COMBINE_XYZ')
    @property
    def 是预览器(self) -> bool:   return 是(self._对象, 'VIEWER')

class 节点判断器(对象):
    def __init__(self, 对象):
        super().__init__(对象)
        self.着色 = 着色节点判断器(对象)
        self.几何 = 几何节点判断器(对象)
        self.合成 = 合成节点判断器(对象)
    @property
    def 是帧(self) -> bool:   return 是(self._对象, 'FRAME')
    @property
    def 是群组(self) -> bool:   return 是(self._对象, 'GROUP')
    @property
    def 是转接点(self) -> bool:   return 是(self._对象, 'REROUTE')
    @property
    def 是组输出(self) -> bool:   return 是(self._对象, 'GROUP_OUTPUT')
    @property
    def 是合并颜色(self) -> bool:   return 是(self._对象, 'COMBINE_COLOR')

class 接口判断器(对象):
    @property
    def 是颜色(self) -> bool:  return 是(self._对象, 'RGBA')
    @property
    def 是布尔(self) -> bool:  return 是(self._对象, 'BOOLEAN')
    @property
    def 是几何数据(self) -> bool:  return 是(self._对象, 'GEOMETRY')
    # "CUSTOM",
    # "VALUE",
    # "INT",
    # "BOOLEAN",
    # "VECTOR",
    # "STRING",
    # "RGBA",
    # "SHADER",
    # "OBJECT",
    # "IMAGE",
    # "GEOMETRY",
    # "COLLECTION",
    # "TEXTURE",
    # "MATERIAL",


class 类型判断器:
    # __slots__ = ('_对象',)
    def __init__(self, 对象): self._对象 = 对象
    @property
    def 编辑器(self) -> 编辑判断器:  return 编辑判断器(self._对象)
    @property
    def 分区(self) -> 分区判断器:    return 分区判断器(self._对象)
    @property
    def 物体(self) -> 物体判断器:    return 物体判断器(self._对象)
    @property
    def 修改器(self) -> 修改器判断器: return 修改器判断器(self._对象)
    @property
    def 节点树(self) -> 节点树判断器: return 节点树判断器(self._对象)
    @property
    def 节点(self) -> 节点判断器:    return 节点判断器(self._对象)
    @property
    def 接口(self) -> 接口判断器:    return 接口判断器(self._对象)

# @property
# 把方法伪装成属性，访问时不需要加括号：
# 没有 @property
# 对象.判断类型()   # 要加括号
#
# 有 @property
# 对象.判断类型     # 不加括号，像访问普通属性一样
# 对象.判断类型.物体.是网格()  # 所以链式调用才自然
#
# # ── 运行时入口函数 ──
# def 判断类型(对象) -> 类型判断器:
#     return 类型判断器(对象)

