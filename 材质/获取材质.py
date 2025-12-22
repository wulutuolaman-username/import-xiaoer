from ..通用.回调 import 回调

def 获取材质(模型):
    材质集合 = set()
    def 添加材质(模型):
        for 材质 in 模型.data.materials:
            if 材质.use_nodes:
                材质集合.add(材质)
    回调(添加材质, 模型)
    return 材质集合