
# 导入硬件相关库
from pyb import UART, ADC   # 串口、舵机、ADC模块
import time, re                    # 时间和正则表达式模块
import sensor                      # 摄像头模块
import machine                    # 机器相关模块
# 机械臂坐标系参数
base_h = 290 - 172 + 52            # 基准高度修正值
Actuator = 0                       # 滑轨坐标，默认0
ON = 1                             # 继电器开关常量

"""
机械臂只可在第一、二、三象限活动，第四象限由于Z轴限位开关阻挡无法活动，即270°旋转范围。
Y轴正方向为机械臂正前方
X轴正方向为机械臂右侧
Z轴正方向为机械臂向上
"""

# 机械臂活动范围参数
h_max = 322        # Z轴最大高度
h_min = 32         # Z轴最小高度
x_max = 280        # X轴最大坐标
x_min = -280       # X轴最小坐标
y_max = 280        # Y轴最大坐标
y_min = -280       # Y轴最小坐标
Servo_max = 60     # 舵机夹爪最大角度
Servo_min = 0      # 舵机夹爪最小角度



def parse_position(data):
    """
    解析机械臂串口返回的坐标字符串，提取X、Y、Z、E坐标。
    :param data: 形如 "INFO: CURRENT POSITION: [X:0.00 Y:174.00 Z:120.00 E:0.00]" 的字符串
    :return: 坐标字典 {'X':..., 'Y':..., 'Z':..., 'E':...} 或错误信息
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
        # 提取每个值并修正Z轴高度
        result = {
            'X': float(pairs[0].split(':')[1]),
            'Y': float(pairs[1].split(':')[1]),
            'Z': float(pairs[2].split(':')[1]) + base_h - Actuator,
            'E': float(pairs[3].split(':')[1])
        }
        return result
    except Exception as e:
        return {'error': str(e), 'input': data}



class Robot:
    def ad_key_control(self):
        """
        通过ADC模拟按键控制机械臂动作，集成长按功能
        """
        LONG_PRESS_MS = 400
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

        a = 0

        # 判断动作类型
        if 0.3 > ad > 0.2:
            action = "Z+"
            a = 9
            # print("9")
            time.sleep_ms(200)

        elif ad < 0.1:
            action = "Z-"
            a = 3
            # print("3")
            time.sleep_ms(200)

        elif 1.7 > ad > 1.4:
            action = "Y+"
            a = 4
            # print("4")
            time.sleep_ms(200)

        elif 1.3 > ad > 1:
            action = "Y-"
            a = 6
            # print("6")
            time.sleep_ms(200)

        elif 0.6 > ad > 0.5:
            action = "X+"
            a = 2
            # print("2")
            time.sleep_ms(200)

        elif 1 > ad > 0.8:
            action = "X-"
            a = 8
            # print("8")
            time.sleep_ms(200)

        elif 2 > ad > 1.7:
            action = "Open"
            a = 1
            # print("1")
            time.sleep_ms(200)

        elif 2.3 > ad > 2.15:
            action = "Close"
            a = 7
            # print("7")  
            time.sleep_ms(200)


        elif 2.6 > ad > 2.45:
            action = "Home"
            a = 5
            # print("5")
            time.sleep_ms(200)
        else:
            action = None

        if action == self._last_action and action is not None:
            self._press_time += CHECK_INTERVAL_MS
        else:
            self._press_time = 0
            self._last_action = action

        # 长按判定
        if self._press_time >= LONG_PRESS_MS and action is not None:
            if action == "Open":
                a = 10
                # print("OpenMV Reset")

            elif action == "Close":
                a = 11
                # print("long Close")

            elif action == "Home":
                a = 12
                # print("long Home")
                # machine.reset()

            self._press_time = 0  # 触发后重置
        return a 
    def __init__(self, nums):
        """
        构造函数，初始化串口、舵机、ADC及机械臂初始坐标。
        :param nums: 串口号（如3）
        """
        self.uart1 = UART(nums, 115200, timeout_char=1)  # 初始化串口                        # 初始夹爪角度
        self.adc = ADC("P6")                            # ADC初始化，必须为"P6"
        self.x = 0                                       # 初始X坐标
        self.y = 174                                     # 初始Y坐标
        self.z = 292                                     # 初始Z坐标
        self.angle = 0                                   # 初始夹爪角度

    def home_setting(self):
        """
        机械臂复位，发送G28指令，等待串口返回。
        超时未返回则直接复位坐标。
        """
        data_to_send = "G28\r\n"
        print(data_to_send, "复位......")
        self.uart1.write(data_to_send)
        start = time.ticks_ms()
        timeout = 15000  # 15秒超时
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                self.angle = 45
                self.Servo(self.angle)
                self.x = 0
                self.y = 174
                self.z = 292
                print(string_data)
                break
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                self.angle = 45
                self.Servo(self.angle)
                self.x = 0
                self.y = 174
                self.z = 292
                print("复位超时，无数据返回")
                break

    def get_xyz_point(self):
        """
        查询机械臂当前坐标，发送M114指令，解析串口返回坐标。
        :return: (X, Y, Z) 坐标元组
        """
        data_to_send = "M114\r\n"
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
                        self.x = position['X']
                        self.y = position['Y']
                        self.z = position['Z']
                        return self.x, self.y, self.z
                        break

    def get_key_val(self):
        """
        查询机械臂限位开关状态，发送M119指令。
        """
        data_to_send = "M119\r\n"
        print(data_to_send, "查询当前限位开关......")
        self.uart1.write(data_to_send)
        while(True):
            if self.uart1.any():
                 data = self.uart1.read()
                 string_data = data.decode('utf-8').strip()
                 print(string_data)
                 break

    def set_xyz_point(self, X, Y, Z, E, F):
        """
        设置机械臂目标坐标，发送G1指令。
        :param X, Y, Z, E, F: 目标坐标与速度参数
        """
        data_to_send = "G1 X{} Y{} Z{} E{} F{}\r\n".format(X, Y, Z-base_h+Actuator, E, F)
        self.x = X
        self.y = Y
        self.z = Z
        self.uart1.write(data_to_send)
        time.sleep_ms(10)

    def relay(self, state):
        """
        控制机械臂主板继电器开关。
        :param state: ON为开，其他为关
        """
        if state == ON:
            data_to_send = "M1\r\n"
        else:
            data_to_send = "M2\r\n"
        print(data_to_send)
        self.uart1.write(data_to_send)

    def Servo(self, angle):
        """
        控制主板舵机角度，发送M280指令。
        :param angle: 舵机角度
        """
        data_to_send = "M280 P{}\r\n".format(angle)
        print(data_to_send)
        self.uart1.write(data_to_send)
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                print(string_data)
                break
