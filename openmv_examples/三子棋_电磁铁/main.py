# main.py
import sensor, ml
import Robot_arm as rb
import chess
import move
import display
import machine
import image
Actuator = 75

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
robot.home_setting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

img = sensor.snapshot()

lcd = display.SPIDisplay()    # 创建SPI显示屏对象

distance = 50
block = 32
ShiftX = 27
ShiftY = -3


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
    for _ in range(50):
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
            if label == "black":
                board[y][x] = "black"
            elif label == "white":
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
    return flag


def put_piece(color,n):
    x = 1
    y = 1
    while True:
        key = choice_even()
        if key !=0 and key != None :
            if key == 1:
                x = 0
                y = 0
            elif key == 2:
                x = 0
                y = 1
            elif key == 3:
                x = 0
                y = 2
            elif key == 4:
                x = 1
                y = 0
            elif key == 5:
                x = 1
                y = 1
            elif key == 6:
                x = 1
                y = 2
            elif key == 7:
                x = 2
                y = 0
            elif key == 8:
                x = 2
                y = 1
            elif key == 9:
                x = 2
                y = 2
            break
    print(x,y)
    if color == 'black':
        move.get_piece_black(n)
    elif color == 'white':
        move.get_piece_white(n)
    move.move2pan(x,y)


def img_show(player):
    img = sensor.snapshot()
    img.draw_string(0,120,"DEMO",scale = 1  ,color=(255,0,0))  # 在图像上显示欢迎语
    img.draw_string(0,140,f"EVEN:{int(flag)}",color=(255,0,0))
    img.draw_string(0,160,"USER:"+player,color=(255,0,0))
    lcd.write(img.copy(hint=image.ROTATE_90))


def Even_1():
    put_piece('black',0)
    n=1
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
                elif board[y][x] == None or board[y][x] == "background" :
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)

        # print("当前胜利者为：",chess.check_winner(board))
        if chess.check_winner(board) != None:
            while True:
                key = robot.ad_key_control()
                print("当前胜利者为：",chess.check_winner(board))
                img.draw_string(0,180,"WINNER:"+chess.check_winner(board),color=(255,0,0))
                lcd.write(img.copy(hint=image.ROTATE_90))
                if key !=0 and key != None :
                    machine.reset()
                    break
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
                move.get_piece_black(n)
                move.move2pan(y,x)
                n = n + 1
        else:
            # 这里可以等待人类输入落子（如通过按键或界面）
            pass
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break


def Even_2():
    n = 0
    img_show('black')
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

        if chess.check_winner(board) != None:
            while True:
                key = robot.ad_key_control()
                print("当前胜利者为：",chess.check_winner(board))
                img.draw_string(0,180,"WINNER:"+chess.check_winner(board),color=(255,0,0))
                lcd.write(img.copy(hint=image.ROTATE_90))
                if key !=0 and key != None :
                    machine.reset()
                    break
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
                move.get_piece_white(n)
                move.move2pan(y,x)
                n = n + 1
        else:
            # 这里可以等待人类输入落子（如通过按键或界面）
            pass
        while True:
            key = robot.ad_key_control()
            if key !=0 and key != None :
                break


img_show('WAITING')

#等待任务选择
choice_even()

if flag == 1:
    print("Even 1")
    img_show('WHITE')
    Even_1()

elif flag == 2:
    print("Even 2")
    img_show('BLACK')
    Even_2()

elif flag == 3:
    color = (0,255,0)
    while True:
        img = sensor.snapshot()
        get_color()
        for line in board:
            print(line)
        for y in range(len(rois)):
            for x in range(len(rois[y])):
                if board[y][x] == "black":
                    color = (255,0,0)
                elif board[y][x] == "white":
                    color = (0,0,255)
                elif board[y][x] == None:
                    color = (0,255,0)
                img.draw_rectangle(rois[y][x], color=color)
else:
    machine.reset()
