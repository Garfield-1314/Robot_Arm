
import Robot_arm as rb
import time

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)
Actuator = 50
def get_qizi(num):
    if num == 0:
        robot.mv_servo(40)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 108
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 108
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(65)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 108
        robot.set_xyz_point(robotx,roboty,70+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 1:
        robot.mv_servo(40)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134+5
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134+5
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(65)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134+5
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 2:
        robot.mv_servo(40)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 167+5
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 167+5
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(65)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 167+5
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 3:
        robot.mv_servo(40)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 94
        roboty = 197+5
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 94
        roboty = 197+5
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(65)
        time.sleep_ms(1000)
        robotx = 94
        roboty = 197+5
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 4:
        robot.mv_servo(40)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 226+5
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 226+5
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(65)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 226+5
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)


def move2pan(x,y):
    if x == 0 and y == 0:
        robotx = -33
        roboty = 245
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(57)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = 1
        roboty = 245
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 35
        roboty = 245
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -36
        roboty = 213
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 215
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 35
        roboty = 213
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = -35
        roboty = 189
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 1
        roboty = 189
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 35
        roboty = 189
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,20+Actuator,0,0)
        time.sleep_ms(1200)
        robot.mv_servo(60)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,220+Actuator,0,0)
        time.sleep_ms(1000)
    # return robotx,roboty



