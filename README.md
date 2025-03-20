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
3.预设文件名称和模型名称是否对的上（例如茜特菈莉的模型错了一个字）![image](https://github.com/user-attachments/assets/2132c250-492a-418c-bace-9ecb1a14020b)，需要修改名称以匹配
```python
if f.endswith(".blend"):
    base_name = f[:-6]  # 去掉.blend后缀
    file_name = base_name.replace("渲染", "")  # 去除文件名"渲染"字样
    file_name = file_name.replace("预设", "")  # 去除文件名"预设"字样
    if file_name in obj_name :  # 如果模型名称包含了处理以后的文件名
        return os.path.join(root, f), file_name

