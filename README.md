### 基于[峰峰居士](https://space.bilibili.com/373134990?spm_id_from=333.337.0.0)的[原版代码](https://www.bilibili.com/video/BV18u4y1K7EM)
### 加入[芙生一梦](https://space.bilibili.com/449654059?spm_id_from=333.337.0.0)的版本检查逻辑
### 参考[异次元学者](https://space.bilibili.com/181717176)的[Blender插件开发教程](https://space.bilibili.com/181717176/lists/3130635?type=season)
### 和[DeepSeek](https://www.deepseek.com/)大战三百回合完成开发
---
### 新代码功能
1. 基础功能完善，导入预设后不会再出现大量图像、节点组的副本
   
2. 如果在偏好设置了包含所有预设文件的预设目录，并且开启了自动查找预设开关，那么代码将会根据预设文件名和模型名称进行匹配  
如果按下按钮没有反应，你需要检查：  
1.是否在偏好设置了预设目录  
2.预设文件是否在预设目录内  
3.预设文件名称和模型名称是否对的上（例如茜特菈莉的模型错了一个字），需要修改名称以匹配
![image](https://github.com/user-attachments/assets/9d73da1b-0d19-48b8-89be-6f282386d39a)![image](https://github.com/user-attachments/assets/257520f0-2710-40aa-bf40-760cd8b4f951)
不排除因为名称相近导入错误的预设（如黑塔和大黑塔），这种情况需要关闭自动查找预设开关，点击手动导入预设文件
```python
if f.endswith(".blend"):
    base_name = f[:-6]  # 去掉.blend后缀
    file_name = base_name.replace("渲染", "")  # 去除文件名"渲染"字样
    file_name = file_name.replace("预设", "")  # 去除文件名"预设"字样
    if file_name in obj_name :  # 如果模型名称包含了处理以后的文件名
        return os.path.join(root, f), file_name
```
3. 增加了默认姿态开关
   如果模型处于默认姿态（模型刚导入时的姿态）可以打开此开关，面部定位将会绑定到头骨的中点  
   如果模型不处于默认姿态（改变了位置、旋转等属性），需要关闭此开关，面部定位可以精准定位到头骨，但是需要改变旋转属性  
   ![image](https://github.com/user-attachments/assets/b0d563a1-1e84-4589-9ca5-60b3d6180f49)  

5. 增加了重命名资产的功能
   如果在一个工程内连续导入多个预设，可能需要管理工程的资产文件  
   开启此开关后，导入预设将将把模型相关的所有物体移入新集合（集合名称为处理以后的文件名），与模型相关的图像、材质、节点组、驱动物体等都会添加下划线和集合名称作为后缀，以防止混乱

   https://github.com/user-attachments/assets/7d2f4e57-ee01-401e-9ea8-68a44d65200f


