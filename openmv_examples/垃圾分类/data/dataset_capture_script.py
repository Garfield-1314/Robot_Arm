# Untitled - By: Admin - Mon Jul 21 2025

import sensor
import time

ShiftX = 20
ShiftY = 5

w = 128
h = 128

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_windowing(int((320-w)/2)+ShiftX,int((240-w)/2)+ShiftY,w,h)

clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())
