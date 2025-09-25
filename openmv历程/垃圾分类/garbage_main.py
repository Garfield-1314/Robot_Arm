# main.py - 基于OpenMV的智能垃圾分类机械臂程序
"""
程序功能：
- 使用摄像头识别垃圾类型
- 控制机械臂自动分拣垃圾到不同垃圾桶
- 支持厨余垃圾、其他垃圾、有害垃圾、可回收垃圾四种分类
"""

# 导入必要的库
import sensor, time                    # 摄像头传感器和时间相关库
import sensor, image, time, ml, math, uos, gc  # 图像处理、机器学习等核心库
import Robot_arm as rb                 # 机械臂控制库
import move                            # 机械臂动作控制模块

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
# sensor.set_windowing((224, 224))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)
robot.home_setting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行

# ===== 加载机器学习模型和标签 =====
# 读取垃圾分类标签文件，每行一个标签名称
with open('labels_garbage.txt','r') as file:
    labels = [line.strip()for line in file if line.strip()]  # 去除空行和首尾空格
    print(labels)  # 打印标签列表，用于调试

# 加载训练好的TensorFlow Lite模型
model = ml.Model("model_garbage.tflite", load_to_fb=True)  # load_to_fb=True表示加载到帧缓冲区以提高性能
print(model)  # 打印模型信息

# 创建数据归一化对象，将像素值从0-255范围缩放到0.0-1.0范围
norm = ml.Normalization(scale = (0.0,1.0))

# ===== 机械臂和摄像头参数配置 =====
Actuator = 55      # 执行器高度偏移量，用于调整机械臂Z轴位置

# 摄像头识别区域的偏移参数，用于微调识别窗口位置
ShiftX = 20        # X轴方向偏移量（像素）
ShiftY = 5         # Y轴方向偏移量（像素）

# 定义识别窗口的尺寸
w = 128            # 识别窗口宽度（像素）
h = 128            # 识别窗口高度（像素）

# 计算ROI（感兴趣区域）的坐标
# ROI格式：(x起始坐标, y起始坐标, 宽度, 高度)
# 将识别窗口居中放置在320x240的图像中，并应用偏移量
roi = (int((320-w)/2)+ShiftX,int((240-h)/2)+ShiftY,w,h)

# ===== 垃圾识别函数 =====
def garbage():
    """
    垃圾分类识别函数
    
    功能描述：
    - 连续拍摄10张照片进行识别
    - 使用机器学习模型对每张图片进行分类
    - 通过众数算法提高识别准确性
    - 只保留置信度高于0.8的识别结果
    
    返回值：
    - str: 识别出的垃圾类型（如"kitchen_garbage", "other"等）
    - None: 如果没有高置信度的识别结果
    """
    results = []  # 存储多次识别的结果列表

    # 进行10次识别采样，提高识别的稳定性和准确性
    for _ in range(10):
        # 拍摄一帧图像
        img = sensor.snapshot()
        
        # 在图像上绘制红色矩形框，显示识别区域
        # 参数：(x, y, 宽度, 高度, 颜色)
        img.draw_rectangle(int((320-w)/2)+ShiftX,int((240-h)/2)+ShiftY,w,h,color = (0,0,255))
        
        # 从原始图像中裁剪出识别区域
        img2 = img.copy(roi=roi)
        
        # 对图像进行归一化处理，将像素值从0-255缩放到0.0-1.0
        input = [norm(img2)]  # scale 0~255 to 0.0~1.0
        
        # 使用机器学习模型进行预测，获取各个类别的置信度分数
        scores = model.predict(input)[0].flatten().tolist()

        # 找到置信度最高的标签
        max_score = 0      # 记录最高置信度分数
        max_label = None   # 记录对应的标签
        
        # 遍历所有标签和对应的置信度分数
        for label, score in zip(labels, scores):
            if score > max_score:
                max_score = score
                max_label = label

        # 仅保存置信度高于0.8的识别结果，过滤掉不确定的识别
        if max_score > 0.8:
            results.append(max_label)

    # 如果没有任何高置信度的识别结果，返回None
    if not results:
        return None

    # 使用众数算法：统计出现频率最高的标签作为最终结果
    # 这样可以减少单次识别错误对最终结果的影响
    count_dict = {}  # 创建字典用于计数
    for label in results:
        # 统计每个标签出现的次数
        count_dict[label] = count_dict.get(label, 0) + 1

    # 找出出现次数最多的标签
    max_count = 0      # 记录最高出现次数
    best_label = None  # 记录对应的标签
    for label, count in count_dict.items():
        if count > max_count:
            max_count = count
            best_label = label

    return best_label  # 返回最终识别结果


# ===== 主循环：持续进行垃圾识别和分拣 =====
while(True):
    labelb = garbage()                 # 调用垃圾识别函数
    print(labelb)                      # 打印识别结果
    
    # 如果成功识别到垃圾类型，执行相应的分拣动作
    if labelb is not None:
        move.execute_garbage_sorting(robot, Actuator, labelb)
    else:
        print("未识别到垃圾或识别置信度过低")
