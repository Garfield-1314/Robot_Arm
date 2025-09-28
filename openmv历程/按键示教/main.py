# Untitled - By: Admin - Wed Jun 25 2025

import sensor,image
import time
import display
import Robot_arm as rb

sensor.reset()  # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565)  # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA)  # Special 128x160 framesize for LCD Shield.
sensor.skip_frames(time=2000)


robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)
time.sleep_ms(1000)
lcd = display.SPIDisplay()
time.sleep_ms(1000)
robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
# robot.home_seting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行

a = robot.get_xyz_point() #获取当前XYZE坐标
print(f"X:{int(a[0])} Y:{int(a[1])} Z:{int(a[2])}")

# robot.get_key_val()

# robot.set_xyz_point(0,174,277,0,0)    #给XYZE坐标，坐标系为平面直角坐标系，（X，Y，Z，E,F），#
# #                                     # E为滑轨坐标，不带滑轨给0即可，F为机械臂运行速度，值小于5为自动插值。#
# #                                     # x=0,y=174，z=277为复位后初始坐标#

# robot.relay(True)    #控制继电器（机械臂主板）

# robot.Servo(False)    #控制舵机（接机械臂主板）

# robot.mv_servo(0)   #给定抓夹舵机角度（接OPENMV拓展板）

while True:
    img = sensor.snapshot()
    robot.ad_key_control()
    a = robot.get_xyz_point() #获取当前XYZE坐标
    img.draw_string(0,0, "Hello Robot!",color=(255,0,0))
    img.draw_string(0, 10, f"X:{int(a[0])} Y:{int(a[1])} Z:{int(a[2])}", color=(255,0,0))
    lcd.write(img.copy(hint=image.ROTATE_90))
