import bpy

# 设置辉光属性和色彩管理
def Setting_blend():
    # 颜色编码转换函数
    def srgb_to_linearrgb(c):
        if c < 0:
            return 0
        elif c < 0.04045:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4
    def hex_to_rgb(h):
        r = (h & 0xff0000) >> 16
        g = (h & 0x00ff00) >> 8
        b = (h & 0x0000ff)
        return tuple([srgb_to_linearrgb(c / 0xff) for c in (r, g, b)])
    # 检查Blender版本是否小于4.2（只比较主版本和次版本）
    if bpy.app.version[:2] < (4, 2):
        bpy.context.scene.eevee.use_bloom = True  # 开启辉光
        bpy.context.scene.eevee.bloom_intensity = 0.08  # 辉光强度
        bpy.context.scene.eevee.bloom_color = hex_to_rgb(0xFFE4D9)  # 辉光颜色
    # 以下设置不受版本影响
    # bpy.context.scene.render.engine = 'Eevee'
    bpy.context.scene.view_settings.view_transform = 'Filmic'
    bpy.context.scene.view_settings.look = 'High Contrast'