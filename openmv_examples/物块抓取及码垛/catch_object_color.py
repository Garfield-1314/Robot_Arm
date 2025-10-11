
# 物块抓取及码垛——基于颜色识别的机械臂分拣主控程序
# 通过颜色识别实现物块自动分拣与堆叠


import sensor
import time
import Robot_arm as rb


# 摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)


clock = time.clock()  # 用于帧率统计


# 机械臂初始化与复位
robot = rb.Robot(3) # 初始化，设置串口3为机械臂通讯串口。
print(robot)
robot.home_setting()   # 机械臂复位，复位运行时若有异常请重启机械臂后再次运行
robot.Servo(0)
robot.set_xyz_point(0,174,290,0,0)
time.sleep_ms(1000)


# 机械臂抓取与堆叠参数
Actuator = 50  # 吸盘/夹爪动作参数

# 蓝色物块堆叠区参数
atxb = -85
atyb = 226
b_num = 0  # 蓝色物块计数

# 黄色物块堆叠区参数
atxy = -92
atyy = 168
y_num = 0  # 黄色物块计数

atz = 18   # 堆叠Z轴基准高度

flag = 0   # 当前检测到的物块类别

ROI=(160,120,120,120)  # 感兴趣区域
YELLOW = [(45, 100, -128, 2, 16, 127)]  # 黄色物块LAB阈值
BLUE = [(0, 41, -128, 127, -128, 127)]  # 蓝色物块LAB阈值
a = 0     # 连续检测到目标的帧数



# 机械臂动作函数：根据检测到的物块颜色和数量进行抓取与堆叠
def Robot_move():
    global flag, a, b_num, y_num
    # 蓝色物块抓取与堆叠流程
    if flag == 'BLUE' and a == 60:
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
        robot.set_xyz_point(atxb,atyb,25+Actuator+b_num*23,0,0)  # 堆叠高度随数量递增
        time.sleep_ms(1000)
        robot.Servo(0)  # 放下
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,240+Actuator,0,0)  # 回到初始点
        time.sleep_ms(1000)
        a=0
        flag = 0
        b_num = b_num + 1

    # 黄色物块抓取与堆叠流程
    if flag == 'YELLOW' and a == 60:
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
        robot.set_xyz_point(atxy,atyy,25+Actuator+y_num*23,0,0)
        time.sleep_ms(1000)
        robot.Servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,240+Actuator,0,0)
        time.sleep_ms(1000)
        a=0
        flag = 0
        y_num = y_num + 1


# 主循环：持续检测物块颜色并控制机械臂分拣堆叠
while True:
    while True:
        img = sensor.snapshot()  # 拍摄一帧图像
        # 检测黄色物块
        for blob in img.find_blobs([YELLOW[0]],pixels_threshold=200,area_threshold=200,merge=True,roi=ROI):
            # 只有非圆形物块检测更稳定
            if not blob:
                a = 0
                flag = 0
                continue
            if blob:
                img.draw_rectangle(blob.rect())
                img.draw_cross(blob.cx(), blob.cy())
                print("YELLOW",blob.x(), blob.y())
                flag = 'YELLOW'
                a = a + 2
                break
            else:
                print("UNKNOWN")
        # 检测蓝色物块
        for blob in img.find_blobs([BLUE[0]],pixels_threshold=200,area_threshold=200,merge=True,roi=ROI):
            if not blob:
                a = 0
                flag = 0
                continue
            if blob:
                img.draw_rectangle(blob.rect())
                img.draw_cross(blob.cx(), blob.cy())
                print("BLUE",blob.x(), blob.y())
                flag = 'BLUE'
                a = a + 2
                break
            else:
                print("UNKNOWN")

        # 连续检测到目标后，减少a防止误触发
        if flag != 0:
            if a > 0:
                a = a - 1
            else:
                a = 0
                flag = 0
            print(flag,a)
            break

    Robot_move()  # 执行分拣与堆叠动作

    if a > 100:
        a = 0
