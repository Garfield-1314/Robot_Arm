
# 导入所需模块
import sensor, ml  # OpenMV 图像传感器与机器学习模块
import Robot_arm as rb  # 机械臂控制模块
import move  # 机械臂动作模块

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # 设置像素格式为RGB565
sensor.set_framesize(sensor.QVGA)    # 设置分辨率为320x240
sensor.skip_frames(time=2000)        # 跳过前2000ms帧，等待摄像头稳定

# 初始化机械臂对象，并回到初始位置
robot = rb.Robot(3)
robot.home_setting()

# 读取垃圾类别标签
with open('labels_garbage.txt','r') as file:
    labels = [line.strip() for line in file if line.strip()]

# 加载垃圾分类模型，并设置归一化参数
model = ml.Model("model_garbage.tflite", load_to_fb=True)
norm = ml.Normalization(scale = (0.0,1.0))

# 机械臂参数与ROI区域设置
Actuator = 55  # 机械臂末端执行器高度
ShiftX = 20    # ROI区域X方向偏移
ShiftY = 5     # ROI区域Y方向偏移
w = 128        # ROI宽度
h = 128        # ROI高度

# 计算ROI区域（感兴趣区域）
roi = (int((320-w)/2)+ShiftX, int((240-h)/2)+ShiftY, w, h)


# 垃圾识别函数，返回识别到的垃圾类别标签
def garbage():
    results = []  # 存储多次识别结果
    for _ in range(10):  # 连续识别10次，提升鲁棒性
        img = sensor.snapshot()  # 拍摄一张图片
        img2 = img.copy(roi=roi)  # 裁剪出ROI区域
        input = [norm(img2)]  # 归一化处理
        scores = model.predict(input)[0].flatten().tolist()  # 模型预测，获取各类别分数
        max_score = 0
        max_label = None
        # 找到分数最高的类别
        for label, score in zip(labels, scores):
            if score > max_score:
                max_score = score
                max_label = label
        # 若置信度大于0.8，记录该类别
        if max_score > 0.8:
            results.append(max_label)
    if not results:
        return None  # 若无高置信度结果，返回None
    # 统计出现次数最多的类别，作为最终结果
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


# 主循环，不断识别垃圾并控制机械臂分类
while(True):
    labelb = garbage()  # 获取识别结果
    print(labelb)  # 打印识别结果
    if labelb is not None:
        move.execute_garbage_sorting(robot, Actuator, labelb)  # 执行垃圾分类动作
    else:
        print("未识别到垃圾或识别置信度过低")  # 提示未识别到垃圾
