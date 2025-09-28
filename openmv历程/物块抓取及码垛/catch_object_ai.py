# Untitled - By: Admin - Thu Jul 3 2025

import sensor, image, time, ml, math, uos, gc
import Robot_arm as rb

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
# sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)

min_confidence = 0.5

# load the model, alloc the model file on the heap if we have at least 64K free after loading
net = ml.Model("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
print(net)


labels = [line.rstrip('\n') for line in open("labels.txt")]
print(labels)

colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
    (255,   0,   0),
    (  0, 255,   0),
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

threshold_list = [(math.ceil(min_confidence * 255), 255)]

def fomo_post_process(model, inputs, outputs):
    ob, oh, ow, oc = model.output_shape[0]

    x_scale = inputs[0].roi[2] / ow
    y_scale = inputs[0].roi[3] / oh

    scale = min(x_scale, y_scale)

    x_offset = ((inputs[0].roi[2] - (ow * scale)) / 2) + inputs[0].roi[0]
    y_offset = ((inputs[0].roi[3] - (ow * scale)) / 2) + inputs[0].roi[1]

    l = [[] for i in range(oc)]

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


# robot.home_setting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行
robot.mv_servo(0)
robot.set_xyz_point(0,174,290,0,0)
time.sleep_ms(1000)

Actuator = 50

atxb = -85
atyb = 226
b_num = 0

atxy = -92
atyy = 162
y_num = 0

atz = 18

flag = 0

ROI=(160,120,120,120)

a = 0



while True:
    a = 0
    while(True):
        img = sensor.snapshot()
        for i, detection_list in enumerate(net.predict([img], callback=fomo_post_process)):
            if i == 0: continue  # background class
            # if len(detection_list) == 0: continue  # no detections for this class?
            for x, y, w, h, score in detection_list:
                center_x = math.floor(x + (w / 2))
                center_y = math.floor(y + (h / 2))
                if score > 0.5 and center_x > 120:
                    # print(labels[i])
                    flag = labels[i]
                    # print(f"x {center_x}\ty {center_y}\tscore {score}")
                    a = a + 1
                    img.draw_circle((center_x, center_y, 12), color=colors[i])
        if flag != 0 and a >= 20:
            print(flag,a)
            break

    # a = a + 1
    if flag == "blue\r" and a >= 20:
        time.sleep_ms(1000)
        a=0
        flag = 0
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
        b_num = b_num + 1

    if flag == "yellow" and a >= 20:
        time.sleep_ms(1000)
        a=0
        flag = 0
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
        y_num = y_num + 1
