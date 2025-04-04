### 基于[峰峰居士](https://space.bilibili.com/373134990?spm_id_from=333.337.0.0)的[原版代码](https://www.bilibili.com/video/BV18u4y1K7EM)
### 加入[芙生一梦](https://space.bilibili.com/449654059?spm_id_from=333.337.0.0)的版本检查逻辑
### 感谢[异次元学者](https://space.bilibili.com/181717176)的[Blender插件开发教程](https://space.bilibili.com/181717176/lists/3130635?type=season)
### 使用[BlenderAddonPackageTool](https://github.com/xzhuah/BlenderAddonPackageTool)辅助开发
### 引用[mmd_tools](https://github.com/MMD-Blender/blender_mmd_tools)部分模块
### 和[ChatGPT](https://chatgpt.com/)、[DeepSeek](https://chat.deepseek.com/)大战三百回合完成开发
---
### 新代码主要功能
### 一、使用预设
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
3. 增加了默认姿态开关[(两种绑定方式)](https://github.com/wulutuolaman-username/import-xiaoer/blob/main/general/bind_bone.py)
   如果模型处于默认姿态（模型刚导入时的姿态）可以打开此开关，面部定位将会绑定到头骨的中点  
   如果模型不处于默认姿态（改变了位置、旋转等属性），需要关闭此开关，绑定前面部定位可以精准定位到头骨，但是需要改变旋转属性
   此状态也将影响下面的加载预设模板
   下图为关闭默认姿态后面部定位的属性  
   ![image](https://github.com/user-attachments/assets/b0d563a1-1e84-4589-9ca5-60b3d6180f49)  

5. 增加了重命名资产的功能
   如果在一个工程内连续导入多个预设，可能需要管理工程的资产文件  
   开启此开关后，导入预设将将把模型相关的所有物体移入新集合（集合名称为处理以后的文件名），与模型相关的图像、材质、节点组、驱动物体等都会添加下划线和集合名称作为后缀，以防止混乱
   
   https://github.com/user-attachments/assets/6c9489da-a9ee-4499-803e-422c51e672e8


### 二、获取预设
#### 可以直接点击前往爱发电或模之屋下载预设

### 三、制作预设（需要更多测试反馈）  
[测试视频](https://space.bilibili.com/230130803/lists/4664876?type=series)
1. 在偏好设置预设目录：导入预设的目录和导出预设的位置
2. 是否开启导入贴图：默认开启，需要在偏好设置贴图目录；也可以关闭，只导入节点组、输入材质等
3. 在偏好设置贴图目录：如果模型名称和对应的贴图文件夹名称对应且唯一，可以开启搜索贴图；反之如果没有对应的名称（如崩坏三每个角色都有大量不同模型和贴图），或模型和贴图是在一起的（如鸣潮），可以直接指定模型的贴图文件夹，关闭搜索贴图
4. 匹配贴图：使用图像感知哈希对模型的基础贴图和贴图文件夹的基础贴图进行匹配，匹配的严格程度取决于汉明距离（越小越严格），如果模型使用的基础贴图就是贴图文件夹中的基础贴图（比如鸣潮）,可以关闭匹配贴图状态，代码会直接将模型的基础贴图作为贴图文件夹的基础贴图
5. 在列表选择游戏，加载对应的预设模板，如果开启了导入贴图，代码将会导入贴图文件夹里的所有贴图，先匹配基础贴图，再根据基础贴图鸣潮搜索其他贴图（我对鸣潮的贴图不太熟悉具体的用途，鸣潮的贴图搜索以后还需要改善）
6. 代码将会根据材质的名称进行分组，随后在blender信息窗口中汇报分组结果 [材质分组](https://github.com/wulutuolaman-username/import-xiaoer/blob/main/material/material_sort.py)
7. 随后应用几何节点组，根据分组结果输入材质
8. 根据材质分组结果应用不同的着色节点组，如果开启了导入贴图还会应用贴图
9. 最后绑定定位到头部，注意默认姿态的状态也会影响绑定方式

### 最后，引用了[mmd_tools](https://github.com/MMD-Blender/blender_mmd_tools)部分模块
#### 比如面板和更新插件的功能，更新插件的时间由于插件包的文件大小和网络速度需要较长时间，我测试时需要三五分钟左右


