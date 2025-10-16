
import Robot_arm as rb
import time

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)
Actuator = 35
def get_piece_white(num):
    if num == 0:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 105
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 105
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 98
        roboty = 105
        robot.set_xyz_point(robotx,roboty,70+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 1:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 93
        roboty = 134
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 2:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 167
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 167
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 167
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 3:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 94
        roboty = 197
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 94
        roboty = 197
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 94
        roboty = 197
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 4:
        robot.relay(True)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 226
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 226
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = 90
        roboty = 226
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)


def get_piece_black(num):
    if num == 0:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -98
        roboty = 102
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -98
        roboty = 102
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -98
        roboty = 102
        robot.set_xyz_point(robotx,roboty,70+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 1:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -93
        roboty = 132
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -93
        roboty = 132
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -93
        roboty = 132
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 2:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -88
        roboty = 160
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -88
        roboty = 160
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -88
        roboty = 160
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 3:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -94
        roboty = 190
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -94
        roboty = 190
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -94
        roboty = 190
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)

    if num == 4:
        robot.relay(True)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -80
        roboty = 170
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -90
        roboty = 220
        robot.set_xyz_point(robotx,roboty,40+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -90
        roboty = 220
        robot.set_xyz_point(robotx,roboty,21+Actuator,0,0)
        time.sleep_ms(1000)
        robotx = -90
        roboty = 220
        robot.set_xyz_point(robotx,roboty,100+Actuator,0,0)
        time.sleep_ms(1000)


def move2pan(x,y):
    if x == 0 and y == 0:
        robotx = -35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = 1
        roboty = 238
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -40
        roboty = 208
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 208
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 35
        roboty = 208
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = -35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 1
        roboty = 180
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

def move2pan_45(x,y):
    if x == 0 and y == 0:
        robotx = -51
        roboty = 208
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = -23
        roboty = 230
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 0
        roboty = 253
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,35+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -23
        roboty = 185
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 208
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 25
        roboty = 230
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = 0
        roboty = 165
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 25
        roboty = 185
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 51
        roboty = 203
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(False)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,290,0,0)
        time.sleep_ms(1000)


def get_pan_piece(x,y):
    if x == 0 and y == 0:
        robotx = -35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 1:
        robotx = 1
        roboty = 238
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 0 and y == 2:
        robotx = 35
        roboty = 238
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 0:
        robotx = -40
        roboty = 208
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 1:
        robotx = 0
        roboty = 208
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 1 and y == 2:
        robotx = 35
        roboty = 208
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 0:
        robotx = -35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 1:
        robotx = 1
        roboty = 180
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)

    elif x == 2 and y == 2:
        robotx = 35
        roboty = 180
        robot.set_xyz_point(robotx,roboty,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(robotx,roboty,30+Actuator,0,0)
        time.sleep_ms(1200)
        robot.relay(True)
        time.sleep_ms(1200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(200)
        robot.set_xyz_point(0,174,100,0,0)
        time.sleep_ms(1000)