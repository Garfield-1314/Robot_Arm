
# 物块抓取及码垛——AI识别与机械臂协作主控程序
# 通过神经网络模型识别物块颜色，实现自动分拣与堆叠
import sensor, image, time, ml, math, uos, gc
import Robot_arm as rb
import machine

# 摄像头初始化
sensor.reset()                         # 重置并初始化摄像头
sensor.set_pixformat(sensor.RGB565)    # 设置像素格式为RGB565（或GRAYSCALE）
sensor.set_framesize(sensor.QVGA)      # 设置分辨率为QVGA (320x240)
sensor.skip_frames(time=2000)          # 等待摄像头稳定

robot = rb.Robot(3) # 初始化，设置串口3为机械臂通讯串口。


# 识别置信度阈值
min_confidence = 0.5



# 加载神经网络模型
net = ml.Model("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
print(net)



# 加载标签（如['background', 'blue', 'yellow']）
labels = [line.rstrip('\n') for line in open("labels.txt")]
print(labels)


# 检测框颜色（按类别区分）
colors = [
    (255,   0,   0),    # 红
    (  0, 255,   0),    # 绿
    (255, 255,   0),    # 黄
    (  0,   0, 255),    # 蓝
    (255,   0, 255),    # 紫
    (  0, 255, 255),    # 青
    (255, 255, 255),    # 白
]


# 二值化阈值（用于blob检测）
threshold_list = [(math.ceil(min_confidence * 255), 255)]


# FOMO模型输出后处理，返回每类物块的检测框和置信度
def fomo_post_process(model, inputs, outputs):
    ob, oh, ow, oc = model.output_shape[0]

    x_scale = inputs[0].roi[2] / ow
    y_scale = inputs[0].roi[3] / oh
    scale = min(x_scale, y_scale)
    x_offset = ((inputs[0].roi[2] - (ow * scale)) / 2) + inputs[0].roi[0]
    y_offset = ((inputs[0].roi[3] - (ow * scale)) / 2) + inputs[0].roi[1]

    l = [[] for i in range(oc)]  # 每个类别一个列表

    for i in range(oc):
        img = image.Image(outputs[0][0, :, :, i] * 255)
        blobs = img.find_blobs(
            threshold_list, x_stride=1, y_stride=1, area_threshold=1, pixels_threshold=1
        )
        for b in blobs:
            rect = b.rect()
            x, y, w, h = rect
            score = (
                img.get_statistics(thresholds=threshold_list, roi=rect).l_mean() / 255.0
            )
            x = int((x * scale) + x_offset)
            y = int((y * scale) + y_offset)
            w = int(w * scale)
            h = int(h * scale)
            l[i].append((x, y, w, h, score))
    return l



# 机械臂复位到初始位置
robot.home_setting()   # 机械臂复位
robot.Servo(0)         # 舵机归零
robot.set_xyz_point(0,174,290,0,0)  # 机械臂移动到初始点
time.sleep_ms(1000)


# 机械臂抓取与堆叠参数
Actuator = 50  # 吸盘/夹爪动作参数

# 蓝色物块堆叠区参数
atxb = -90
atyb = 229
b_num = 0  # 蓝色物块计数

# 黄色物块堆叠区参数
atxy = -95
atyy = 168
y_num = 0  # 黄色物块计数

atz = 18   # 堆叠Z轴基准高度

flag = 0   # 当前检测到的物块类别

ROI=(160,120,120,120)  # 感兴趣区域

a = 0     # 连续检测到目标的帧数

YELLOW = [(45, 100, -128, 2, 16, 127)]  # 黄色物块LAB阈值
BLUE = [(0, 41, -128, 127, -128, 127)]  # 蓝色物块LAB阈值


# 机械臂动作函数：根据检测到的物块类别和数量进行抓取与堆叠
def Robot_move_ai(flag,a):
    global b_num,y_num
    # 蓝色物块抓取与堆叠流程
    if flag == "blue\r" and a >= 20:
        time.sleep_ms(1000)
        a = 0
        flag = 0
        time.sleep_ms(1000)
        robot.Servo(0)
        robot.set_xyz_point(35,194,atz+Actuator,0,0)  # 移动到抓取点
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.Servo(60)  # 吸取/夹取
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,120+Actuator,0,0)  # 移动到蓝色堆叠区上方
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,25+Actuator+b_num*25,0,0)  # 堆叠高度随数量递增
        time.sleep_ms(1000)
        robot.Servo(0)  # 放下
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,240+Actuator,0,0)  # 回到初始点
        time.sleep_ms(1000)
        b_num = b_num + 1

    # 黄色物块抓取与堆叠流程
    if flag == "yellow" and a >= 20:
        time.sleep_ms(1000)
        a = 0
        flag = 0
        time.sleep_ms(1000)
        robot.Servo(0)
        robot.set_xyz_point(35,194,atz+Actuator,0,0)
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.Servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,25+Actuator+y_num*25,0,0)
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,240+Actuator,0,0)
        time.sleep_ms(1000)
        y_num = y_num + 1


def Robot_move_blobs(flag, a):
    global b_num, y_num
    # 蓝色物块抓取与堆叠流程
    if flag == 'BLUE' and a >= 0:
        time.sleep_ms(1000)
        robot.Servo(0)
        robot.set_xyz_point(35,194,atz+Actuator,0,0)  # 移动到抓取点
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.Servo(60)  # 吸取/夹取
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,120+Actuator,0,0)  # 移动到蓝色堆叠区上方
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,25+Actuator+b_num*25,0,0)  # 堆叠高度随数量递增
        time.sleep_ms(1000)
        robot.Servo(0)  # 放下
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,240+Actuator,0,0)  # 回到初始点
        time.sleep_ms(1000)
        a=0
        flag = 0
        b_num = b_num + 1

    # 黄色物块抓取与堆叠流程
    if flag == 'YELLOW' and a >= 0:
        time.sleep_ms(1000)
        robot.Servo(0)
        robot.set_xyz_point(35,194,atz+Actuator,0,0)
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.Servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,25+Actuator+y_num*25,0,0)
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,240+Actuator,0,0)
        time.sleep_ms(1000)
        a=0
        flag = 0
        y_num = y_num + 1


# 主循环：持续检测物块并控制机械臂分拣堆叠
def main_ai():
    while True:
        a = 0  # 连续检测到目标的帧数
        flag = 0
        while(True):
            img = sensor.snapshot()  # 拍摄一帧图像
            # 神经网络推理，返回每类物块的检测框
            for i, detection_list in enumerate(net.predict([img], callback=fomo_post_process)):
                if i == 0: continue  # 跳过背景类
                # if len(detection_list) == 0: continue  # 若无检测可跳过
                for x, y, w, h, score in detection_list:
                    center_x = math.floor(x + (w / 2))
                    center_y = math.floor(y + (h / 2))
                    if score > 0.5 and center_x > 120:  # 置信度高且在右侧区域
                        # print(labels[i])
                        flag = labels[i]  # 记录类别
                        # print(f"x {center_x}\ty {center_y}\tscore {score}")
                        a = a + 1  # 连续检测计数
                        img.draw_circle((center_x, center_y, 12), color=colors[i])  # 标记目标
            if flag != 0 and a >= 20:
                print(flag,a)
                break  # 连续检测到目标20帧后，执行机械臂动作
        # print(1)
        Robot_move_ai(flag,a)  # 执行分拣与堆叠动作


def main_blobs():
    while True:
        a = 0
        flag = 0
        last_flag = 0
        while True:
            img = sensor.snapshot()  # 拍摄一帧图像
            detected = 0
            # 检测黄色物块
            for blob in img.find_blobs([YELLOW[0]],pixels_threshold=200,area_threshold=200,merge=True,roi=ROI):
                if blob:
                    img.draw_rectangle(blob.rect())
                    img.draw_cross(blob.cx(), blob.cy())
                    flag = 'YELLOW'
                    detected = 1
                    break
            # 检测蓝色物块
            if not detected:
                for blob in img.find_blobs([BLUE[0]],pixels_threshold=200,area_threshold=200,merge=True,roi=ROI):
                    if blob:
                        img.draw_rectangle(blob.rect())
                        img.draw_cross(blob.cx(), blob.cy())
                        flag = 'BLUE'
                        detected = 1
                        break
            # 连续识别逻辑
            if detected:
                if last_flag == flag:
                    a += 1
                else:
                    a = 1
                last_flag = flag
            else:
                a = 0
                flag = 0
                last_flag = 0
            # 达到阈值才判定有效
            if flag != 0 and a >= 40:
                print(flag, a)
                break
        # print(2)
        Robot_move_blobs(flag,a)  # 执行分拣与堆叠动作
        a = 0

flag = 0
def choice_even():
    global flag
    while 1:
        key = robot.ad_key_control()
        # print(b)
        if key == 10:
            print("10")
            flag = key
            break
        elif key == 11:
            print("11")
            flag = key
            break
        elif key == 12:
            print("12")
            flag = key
            break
        elif key !=0 and key != None :
            print(key)
            flag = key
            break
    return flag
#等待任务选择
choice_even()

if flag == 1:
    main_ai()
elif flag == 2:
    main_blobs()
else:
    machine.reset()
