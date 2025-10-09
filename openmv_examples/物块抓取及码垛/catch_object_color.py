# Untitled - By: Admin - Thu Jul 3 2025

import sensor
import time
import Robot_arm as rb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

clock = time.clock()

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)
# robot.home_setting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行
robot.mv_servo(0)
robot.set_xyz_point(0,174,290,0,0)
time.sleep_ms(1000)

Actuator = 50
atxb = -85
atyb = 226
b_num = 0

atxy = -92
atyy = 168
y_num = 0

atz = 18

flag = 0

ROI=(160,120,120,120)
YELLOW = [(45, 100, -128, 2, 16, 127)]
BLUE = [(0, 41, -128, 127, -128, 127)]
a = 0

while True:

    while True:
        img = sensor.snapshot()
        for blob in img.find_blobs([YELLOW[0]],pixels_threshold=200,area_threshold=200,merge=True,roi=ROI):
            # These values depend on the blob not being circular - otherwise they will be shaky.
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
        for blob in img.find_blobs([BLUE[0]],pixels_threshold=200,area_threshold=200,merge=True,roi=ROI):
            # These values depend on the blob not being circular - otherwise they will be shaky.
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

        if flag != 0:
            if a > 0:
                a = a - 1
            else:
                a = 0
                flag = 0
            print(flag,a)
            break

    # a = a + 1
    if flag == 'BLUE' and a == 60:
        time.sleep_ms(1000)
        robot.mv_servo(0)
        robot.set_xyz_point(35,194,atz+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(0)
        time.sleep_ms(1000)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,25+Actuator+b_num*23,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,240+Actuator,0,0)
        time.sleep_ms(1000)
        a=0
        flag = 0
        b_num = b_num + 1

    if flag == 'YELLOW' and a == 60:
        time.sleep_ms(1000)
        robot.mv_servo(0)
        robot.set_xyz_point(35,194,atz+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(0)
        time.sleep_ms(1000)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,25+Actuator+y_num*23,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,240+Actuator,0,0)
        time.sleep_ms(1000)
        a=0
        flag = 0
        y_num = y_num + 1

    if a > 100:
        a = 0
