# main.py
import sensor, time,ml
from pyb import Pin,ADC
import Robot_arm as rb
import chess
import move

Actuator = 55

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)
# robot.home_seting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行
robot.set_xyz_point(0,174,220+Actuator,0,0)
time.sleep_ms(1000)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)


# 轻触开关
adc = ADC("P6")  # ADC初始化，必须为"P6"


distance = 47
block = 32
ShiftX = 50
ShiftY = 0

# 生成九宫格的区域位置
def generate_centered_rois(width, height, b, k):
    rois = []

    # 计算每个ROI中心的位置偏移
    # offset = (b - k) // 2

    # 计算整个3x3矩阵的宽度和高度
    total_width = 3 * b
    total_height = 3 * b

    # 计算左上角的起始点，使矩阵居中
    start_x = (width - total_width) // 2 + ShiftX
    start_y = (height - total_height) // 2 + ShiftY

    for i in range(3):
        row = []
        for j in range(3):
            x_center = start_x + j * b + b // 2
            y_center = start_y + i * b + b // 2
            x = x_center - k // 2
            y = y_center - k // 2
            row.append((x, y, k, k))
        rois.append(row)

    return rois


# 九宫格的区域位置
rois = generate_centered_rois(sensor.width(), sensor.height(), distance, block)


# 棋盘数组
# 黑子：X
# 白子：O
# 没有棋子：空字符串
board = [
     [" "," "," "],
     [" "," "," "],
     [" "," "," "],
]


#等开关按下并松开
def wait_key():
    ad = ((adc.read() * 3.3) / 4095)
    while ad > 0.5:
        ad = ((adc.read() * 3.3) / 4095)
        # print(ad)
        img = sensor.snapshot()
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                img.draw_rectangle(rois[y][x])

with open('labels_color.txt','r') as file:
    labels = [line.strip()for line in file if line.strip()]
    print(labels)
model = ml.Model("color_model.tflite", load_to_fb=True)
print(model)
norm = ml.Normalization(scale = (0.0,1.0))

def Net(img2):
    results = []  # 存储识别结果
    # 进行10次识别
    for _ in range(10):
        input = [norm(img2)]  # scale 0~255 to 0.0~1.0
        scores = model.predict(input)[0].flatten().tolist()
        # 找到最高分标签
        max_score = 0
        max_label = None
        for label, score in zip(labels, scores):
            if score > max_score:
                max_score = score
                max_label = label

        # 仅记录置信度高的结果
        if max_score > 0.8:
            results.append(max_label)

    # 计算众数（最频繁出现的标签）
    if not results:
        return None

    # 使用简单计数找出出现次数最多的标签
    count_dict = {}
    for label in results:
        count_dict[label] = count_dict.get(label, 0) + 1

    # 找出最高频率
    max_count = 0
    best_label = None
    for label, count in count_dict.items():
        if count > max_count:
            max_count = count
            best_label = label

    return best_label


def get_color():
    # 图像识别得到棋盘数组
    for y in range(len(rois)):
        for x in range(len(rois[y])):
            img2 = img.copy(roi=rois[y][x])
            label = Net(img2)
            print(label)
            if label == "blue":
                board[y][x] = "X"
            elif label == "yellow":
                board[y][x] = "O"
            else:
                board[y][x] = " "


a = 0
while(True):
    wait_key()
    img = sensor.snapshot()
    for y in range(len(rois)):
        for x in range(len(rois[y])):
            img.draw_rectangle(rois[y][x])
    time.sleep_ms(1000)
    get_color()
    # 打印当前棋盘数组
    for line in board:
        print(line)
    print()

    # 画棋盘数组
    for y in range(len(rois)):
        for x in range(len(rois[y])):
            if board[y][x] == "X":
                color = (255,0,0)
            elif board[y][x] == "O":
                color = (0,0,255)
            elif board[y][x] == " ":
                color = (0,255,0)
            img.draw_rectangle(rois[y][x], color=color)

    # 下棋策略
    if chess.check_win(board, 'O'):
        print("你赢啦!")
        a = 0
        wait_key()
    elif chess.check_win(board, 'X'):
        print("我赢啦！")
        a = 0
        wait_key()
    elif chess.check_draw(board):
        print("平局啦！")
        a = 0
        wait_key()
    elif chess.check_turn(board) == "X":
        # 计算下一步棋子放在哪里
        line,row = chess.computer_move(board)
        print(line,row)
        # 目标棋盘上画十字
        img.draw_cross(int(rois[line][row][0]+block/2), int(rois[line][row][1]+block/2), size=block, color=0)
        move.get_qizi(a)
        move.move2pan(line,row)
        time.sleep_ms(1000)
        a = a + 1
        # 机器人拾取并放置棋子

    elif chess.check_turn(board) == "O":
        print("该你下了！")
