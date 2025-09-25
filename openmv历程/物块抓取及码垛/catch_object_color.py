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
robot.home_seting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行
robot.mv_servo(0)
robot.set_xyz_point(0,174,222,0,0)
time.sleep_ms(1000)

Actuator = 55
atxb = -164
atyb = 152

atxy = -168
atyy = 113

atz = 10

flag = 0

ROI=(160,120,160,120)

a = 0

while True:
    
    while True:
        img = sensor.snapshot()
        for c in img.find_circles(threshold = 2000, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 2, r_max = 100, r_step = 2,roi = ROI):
            area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
            #area为识别到的圆的区域，即圆的外接矩形框
            statistics = img.get_statistics(roi=area)#像素颜色统计
            img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
            a = a + 1
            # print(statistics)
            if 0<statistics.l_mode()<100 and 0<statistics.a_mode()<127 and statistics.b_mode()<0:
                print("BLUE",c.x(), c.y())
                flag = 'BLUE'
                break
            elif 0<statistics.l_mode()<100 and statistics.a_mode()<0 and 0<statistics.b_mode()<127:
                print("YELLOW",c.x(), c.y())
                flag = 'YELLOW'
                break
            else:
                print("UNKNOWN")
        # for r in img.find_rects(threshold=8000,roi = ROI):
        #     img.draw_rectangle(r.rect(), color=(255, 0, 0))
        if flag != 0:
            print(flag,a)
            break

    # a = a + 1
    if flag == 'BLUE' and a == 30:
        time.sleep_ms(1000)
        a=0
        flag = 0
        time.sleep_ms(1000)
        robot.mv_servo(0)
        robot.set_xyz_point(45,168,atz+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(0)
        time.sleep_ms(1000)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxb,atyb,25+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)

    if flag == 'YELLOW' and a == 30:
        time.sleep_ms(1000)
        a=0
        flag = 0
        time.sleep_ms(1000)
        robot.mv_servo(0)
        robot.set_xyz_point(45,168,atz+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(0)
        time.sleep_ms(1000)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,120+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(atxy,atyy,25+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
