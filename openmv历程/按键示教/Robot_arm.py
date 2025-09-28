from pyb import UART,Servo,ADC
import time , re
import sensor

base_h = 290 - 172 + 52

Actuator = 0

ON = 1

"""
机械臂只可在第一、二、三象限活动,第四象限由于Z轴限位开关阻挡的原因无法活动,即270°的旋转范围。
Y轴正方向为机械臂正前方
X轴正方向为机械臂右侧
Z轴正方向为机械臂向上
"""

# 机械臂活动范围参数
# h_max/h_min: Z轴（垂直方向）最大/最小高度
# x_max/x_min: X轴（左右方向）最大/最小坐标
# y_max/y_min: Y轴（前后方向）最大/最小坐标
# Servo_max/Servo_min: 舵机夹爪最小/最大角度

h_max = 322
h_min = 32
x_max = 280
x_min = -280
y_max = 280
y_min = -280
Servo_max = 60
Servo_min = 0






def parse_position(data):
    """
    解析位置字符串并返回坐标字典
    :param data: 包含坐标信息的字符串 (格式: "INFO: CURRENT POSITION: [X:0.00 Y:174.00 Z:120.00 E:0.00]")
    :return: 包含X, Y, Z, E坐标的字典
    """
    try:
        # 找到方括号内的内容
        start_index = data.find('[') + 1
        end_index = data.find(']')

        # 验证字符串格式
        if start_index == -1 or end_index == -1 or start_index >= end_index:
            raise ValueError("无效的输入格式 - 缺少方括号")

        coordinates_str = data[start_index:end_index]

        # 分割键值对
        pairs = coordinates_str.split()

        # 验证元素数量
        if len(pairs) < 4:
            raise ValueError(f"无效的输入格式 - 需要4个元素，实际找到{len(pairs)}")

        # 提取每个值
        result = {
            'X': float(pairs[0].split(':')[1]),
            'Y': float(pairs[1].split(':')[1]),
            'Z': float(pairs[2].split(':')[1]) + base_h - Actuator,
            'E': float(pairs[3].split(':')[1])
        }

        return result

    except Exception as e:
        return {'error': str(e), 'input': data}


class CoordRecorder:
    def __init__(self, max_points=20):
        self.coord_list = []
        self.max_points = max_points

    def record(self, x, y, z):
        """
        记录一个坐标点，最多max_points个。连续相邻相同点只存一个。
        """
        new_point = (x, y, z)
        if len(self.coord_list) == 0 or self.coord_list[-1] != new_point:
            if len(self.coord_list) < self.max_points:
                self.coord_list.append(new_point)
            else:
                print("坐标记录已满（%d个点）" % self.max_points)

    def get(self, idx):
        """
        按索引查找已记录的坐标点
        """
        if 0 <= idx < len(self.coord_list):
            return self.coord_list[idx]
        else:
            print("索引超出范围")
            return None
        
    def clear(self):
        """
        清空所有已记录坐标点
        """
        self.coord_list = []

class Robot:
    def ad_key_control(self):
        """
        通过ADC模拟按键控制机械臂动作，集成长按功能
        """
        LONG_PRESS_MS = 500
        CHECK_INTERVAL_MS = 100
        # 静态变量存储上一次动作和持续时间
        if not hasattr(self, '_last_action'):
            self._last_action = None
        if not hasattr(self, '_press_time'):
            self._press_time = 0

        ad_list = []
        for _ in range(20):
            ad_list.append((self.adc.read() * 3.3) / 4095)
            time.sleep_ms(1)
        ad_list.sort()
        filtered = ad_list[1:-1]
        mid_idx = len(filtered) // 2
        if len(filtered) % 2 == 0:
            ad = round((filtered[mid_idx - 1] + filtered[mid_idx]) / 2, 2)
        else:
            ad = round(filtered[mid_idx], 2)

        # 判断动作类型
        if 0.3 > ad > 0.18:
            action = "Z+"
            print("short Z+")
            self.z = self.z + 2

        elif ad < 0.1:
            action = "Z-"
            print("short Z-")
            self.z = self.z - 2

        elif 1.7 > ad > 1.4:
            action = "Y+"
            print("short Y+")
            self.y = self.y + 2

        elif 1.3 > ad > 1:
            action = "Y-"
            print("short Y-")
            self.y = self.y - 2

        elif 0.6 > ad > 0.5:
            action = "X+"
            print("short X+")
            self.x = self.x - 2

        elif 1 > ad > 0.8:
            action = "X-"
            print("short X-")
            self.x = self.x + 2

        elif 2 > ad > 1.7:
            action = "Open"
            self.get_coord(0)
            print(self.get_coord(1))
            print("short Open")

        elif 2.3 > ad > 2.1:
            action = "Close"
            self.record_coord()
            print("short Close")


        elif 2.6 > ad > 2.45:
            action = "Home"
            print("short Home")
        else:
            action = None

        self.set_xyz_point(self.x, self.y, self.z, 0, 0)
        self.get_xyz_point()

        if action == self._last_action and action is not None:
            self._press_time += CHECK_INTERVAL_MS
        else:
            self._press_time = 0
            self._last_action = action

        # 长按判定
        if self._press_time >= LONG_PRESS_MS and action is not None:
            if action == "Open":
                print("long Open")
                self.angle = self.angle - 2
                self.mv_servo(self.angle)

            elif action == "Close":
                print("long Close")
                self.angle = self.angle + 2
                self.mv_servo(self.angle)

            elif action == "Home":
                print("long Home")
                self.home_setting()
                self.clear_coords()
                time.sleep_ms(1000)

            self._press_time = 0  # 触发后重置

    def __init__(self, nums):
        self.coord_recorder = CoordRecorder()
        
        self.uart1 = UART(nums, 115200, timeout_char=1)
        self.servo = Servo(1)
        self.angle = 45
        self.servo.angle(self.angle)
        self.adc = ADC("P6")  # ADC初始化，必须为"P6"
        self.x = 0
        self.y = 174
        self.z = 292

    def record_coord(self):
        """
        记录当前X,Y,Z坐标到CoordRecorder
        """
        self.coord_recorder.record(self.x, self.y, self.z)

    def get_coord(self, idx):
        """
        按索引查找已记录的坐标点
        """
        return self.coord_recorder.get(idx)
    
    def clear_coords(self):
        """
        清空所有已记录的坐标点
        """
        self.coord_recorder.clear()

    def home_setting(self):
        data_to_send = "G28\r\n"
        print(data_to_send, "复位......")
        self.uart1.write(data_to_send)
        start = time.ticks_ms()
        timeout = 12000  # 12秒超时
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                self.x = 0
                self.y = 174
                self.z = 292
                print(string_data)
                break
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                self.x = 0
                self.y = 174
                self.z = 292
                print("复位超时，无数据返回")
                break

    def get_xyz_point(self):
        data_to_send = "M114\r\n"
        # print(data_to_send, "查询当前坐标......")
        self.uart1.write(data_to_send)
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                # 串口可能返回多行数据，逐行处理
                for line in string_data.split('\n'):
                    line = line.strip()
                    if 'CURRENT POSITION' in line:
                        position = parse_position(line)
                        if 'error' in position:
                            print(f"坐标解析失败: {position['error']} 原始数据: {position['input']}")
                            continue
                        # print(f"X: {position['X']} Y: {position['Y']} Z: {position['Z']} E: {position['E']}")
                        self.x = position['X']
                        self.y = position['Y']
                        self.z = position['Z']
                        return self.x, self.y, self.z
                        break

    def get_key_val(self):
        data_to_send = "M119\r\n"
        print(data_to_send,"查询当前限位开关......")
        self.uart1.write(data_to_send)
        while(True):
            if self.uart1.any():
                 data = self.uart1.read()
                 string_data = data.decode('utf-8').strip()
                 print(string_data)
                 break

    def set_xyz_point(self,X,Y,Z,E,F):
        data_to_send = "G1 X{} Y{} Z{} E{} F{}\r\n".format(X, Y, Z-base_h+Actuator, E, F)
        self.x = X
        self.y = Y
        self.z = Z
        self.uart1.write(data_to_send)
        time.sleep_ms(10)

    def relay(self,state):
        if state == ON :
            data_to_send = "M1\r\n"
        else:
            data_to_send = "M2\r\n"
        print(data_to_send)
        self.uart1.write(data_to_send)

    def Servo(self,state):
        if state == ON :
            data_to_send = "M3\r\n"
        else:
            data_to_send = "M5\r\n"
        print(data_to_send)
        self.uart1.write(data_to_send)

    def mv_servo(self,angle):
        self.servo.angle(angle)

