sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

# 导入核心库：图像处理、机器学习、机械臂控制
import sensor, ml
import Robot_arm as rb
import move

# 传感器初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)



# 读取标签文件，获取垃圾类别标签
with open('labels.txt','r') as file:
    labels = [line.strip()for line in file if line.strip()]
    print(labels)  # 打印标签列表，便于调试

# 加载垃圾分类模型
model = ml.Model("model.tflite", load_to_fb=True)
print(model)  # 打印模型信息

# 归一化处理对象
norm = ml.Normalization(scale = (0.0,1.0))

# 机械臂参数设置
Actuator = 55  # 执行器高度偏移量
ShiftX = 20    # X轴方向偏移量
ShiftY = 5     # Y轴方向偏移量
w = 128        # 识别窗口宽度
h = 128        # 识别窗口高度
roi = (int((320-w)/2)+ShiftX,int((240-h)/2)+ShiftY,w,h)  # 识别区域

# 初始化机械臂
robot = rb.Robot(3)  # 创建机械臂对象，串口3
robot.home_setting() # 机械臂复位


with open('labels.txt','r') as file:
    labels = [line.strip()for line in file if line.strip()]
    print(labels)
model = ml.Model("model.tflite", load_to_fb=True)
print(model)
norm = ml.Normalization(scale = (0.0,1.0))

Actuator = 55

ShiftX = 20
ShiftY = 5

w = 128
h = 128

roi = (int((320-w)/2)+ShiftX,int((240-h)/2)+ShiftY,w,h)

def garbage():
    """
    垃圾分类识别函数：
    连续采集10帧图像，使用模型进行分类，采用众数算法提升准确率。
    只保留置信度大于0.8的结果。
    返回：识别出的垃圾类型字符串或None。
    """
    results = []  # 存储多次识别结果
    for _ in range(10):
        img = sensor.snapshot()  # 拍摄一帧图像
        # 绘制红色识别区域
        img.draw_rectangle(int((320-w)/2)+ShiftX,int((240-h)/2)+ShiftY,w,h,color = (0,0,255))
        img2 = img.copy(roi=roi)  # 裁剪识别区域
        input = [norm(img2)]     # 归一化处理
        scores = model.predict(input)[0].flatten().tolist()  # 模型预测
        max_score = 0
        max_label = None
        # 找到置信度最高的标签
        for label, score in zip(labels, scores):
            if score > max_score:
                max_score = score
                max_label = label
        # 只保留置信度高的结果
        if max_score > 0.8:
            results.append(max_label)
    if not results:
        return None  # 没有高置信度结果
    # 众数算法，统计出现最多的标签
    count_dict = {}
    for label in results:
        count_dict[label] = count_dict.get(label, 0) + 1
    max_count = 0
    best_label = None
    for label, count in count_dict.items():
        if count > max_count:
            max_count = count
            best_label = label
    return best_label




while(True):
    labelb = garbage()  # 调用识别函数
    print(labelb)       # 打印识别结果
    if labelb is not None:
        # 根据识别结果执行分拣动作
        move.execute_garbage_sorting(robot, Actuator, labelb)
    else:
        print("未识别到垃圾或识别置信度过低")
