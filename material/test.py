eye_mouth_name = ["眉", "mei", "睫", "jie", "二重", "bai", "眼", "目", "瞳", "eye", "Eye", "hi", "yinying",
                  "口", "嘴", "唇", "mouth", "kou", "lip", "牙", "齿", "齒", "teeth", "舌", "tongue", "she",
                  "痣"]
eye_mouth_materials = []

emotion_name = ["表情", "biaoq", "bq", "emo", "heart", "星", "Star", "❤", "Cheek", "nose", "脸红", "照れ", "> <"]
emotion_materials = []

hair_name = ["发", "髪", "髮", "辫", "hair", "Hair", "Bang", "刘海", "后脑勺", "马尾", "馬尾"]
hair_materials = []

face_name = ["脸", "颜", "顏", "面", "face", "Face"]
face_materials = []  # 考虑到有些模型将脸分成多个材质
skin_name = ["首", "脖", "kubi", "皮肤", "肌", "skin", "Skin", "體", "ear", "hou"]
skin_materials = []  # 在几何节点时可将脸材质并入皮肤材质同时输入；在着色节点时，处理脸材质后将其从皮肤材质中移除，然后处理皮肤材质

# 反向过滤
clothes_name = ["面具", "面罩", "面襯", "神之眼", "眼罩", "眼镜", "饰", "飾", "绳", "繩", "纱", "紗", "带", "帶"]
clothes_materials = []

material_name = r'toushi'

is_eye_mouth = any(keyword in material_name or keyword in material_name.lower() for keyword in eye_mouth_name)
is_emotion = any(keyword in material_name or keyword in material_name.lower() for keyword in emotion_name)
is_hair = any(keyword in material_name or keyword in material_name.lower() for keyword in hair_name)
is_face = any(keyword in material_name or keyword in material_name.lower() for keyword in face_name)
is_skin = any(keyword in material_name or keyword in material_name.lower() for keyword in skin_name)
is_clothes = any(keyword in material_name or keyword in material_name.lower() for keyword in clothes_name)

if __name__ == "__main__":
    print(is_eye_mouth)