# main.py
import sensor, time, ml
from pyb import Pin
import Robot_arm as rb
import chess
import move
import display

Actuator = 75

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
robot.home_setting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行
time.sleep_ms(1000)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

img = sensor.snapshot()

lcd = display.SPIDisplay()    # 创建SPI显示屏对象

distance = 47
block = 32
ShiftX = 25
ShiftY = -12


# 生成九宫格的区域位置
def generate_centered_rois(width, height, b, k):
    rois = []
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

with open('labels.txt','r') as file:
    labels = [line.strip()for line in file if line.strip()]
    print(labels)
model = ml.Model("model.tflite", load_to_fb=True)
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
                board[y][x] = "black"
            elif label == "yellow":
                board[y][x] = "white"
            else:
                board[y][x] = None

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


#等待任务选择
choice_even()


def Even_4():
    # while True:
    #     key = choice_even()
    #     if key !=0 and key != None :
    #         break
    #     move.move2pan(0,0)
    while True:
        img = sensor.snapshot()
        global board
        # 识别棋盘
        get_color()
        for line in board:
            print(line)
        # 画棋盘数组
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None:
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)

        print("当前胜利者为：",chess.check_winner(board))
        # 判断当前轮到谁
        player = chess.get_current_player(board)
        print("当前轮到:", player)

        # 如果是AI执子（如white），则AI落子
        if player == "black":
            move_pos = chess.best_move(board, player)
            print("AI选择位置:", move_pos)
            if move_pos is not None:
                y, x = move_pos
                board[y][x] = player
        else:
            # 这里可以等待人类输入落子（如通过按键或界面）
            pass
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break

def Even_5():
    while True:
        img = sensor.snapshot()
        global board
        # 识别棋盘
        get_color()
        for line in board:
            print(line)
        # 画棋盘数组
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None:
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)

        print("当前胜利者为：",chess.check_winner(board))
        # 判断当前轮到谁
        player = chess.get_current_player(board)
        print("当前轮到:", player)

        # 如果是AI执子（如white），则AI落子
        if player == "white":
            move_pos = chess.best_move(board, player)
            print("AI选择位置:", move_pos)
            if move_pos is not None:
                y, x = move_pos
                board[y][x] = player
        else:
            # 这里可以等待人类输入落子（如通过按键或界面）
            pass
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break

if flag == 1:
    print("Even 1")

elif flag == 2:
    print("Even 2")

elif flag == 3:
    print("Even 3")

elif flag == 4:
    print("Even 4")
    Even_4()

elif flag == 5:
    print("Even 5")
    Even_5()

elif flag == 6:
    print("Even 6")
