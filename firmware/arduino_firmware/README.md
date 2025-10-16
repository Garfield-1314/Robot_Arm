# Arduino Robot Arm Firmware / Arduino 机械臂固件

## 简介 | Introduction
本项目为基于 Arduino 平台的机械臂控制固件，适用于 ESP32（如 Wemos D1 R32）等主控板。固件实现了机械臂的基本运动控制、插补算法、末端执行器（如舵机夹爪）控制、限位检测、命令解析等功能。

This project is a robot arm control firmware based on the Arduino platform, suitable for ESP32 (such as Wemos D1 R32) and other mainboards. The firmware implements basic motion control, interpolation algorithms, end-effector (such as servo gripper) control, endstop detection, command parsing, and more.

## 主要功能 | Main Features
- 多轴步进电机控制，支持 Ramps 驱动板
- 运动插补算法，实现平滑轨迹规划
- 舵机夹爪控制
- 端点限位检测，保证运动安全
- 命令解析与队列管理，支持外部串口/网络指令
- 日志记录与调试输出

- Multi-axis stepper motor control, supports Ramps driver board
- Motion interpolation algorithm for smooth trajectory planning
- Servo gripper control
- Endstop detection for safe operation
- Command parsing and queue management, supports external serial/network commands
- Logging and debug output

## 主要文件说明 | Main Files
- `arduino_firmware.ino`：主程序入口 | Main program entry
- `RampsStepper.*`：步进电机控制与驱动 | Stepper motor control and driver
- `interpolation.*`：插补算法实现 | Interpolation algorithm
- `servo_gripper.*`：舵机夹爪控制 | Servo gripper control
- `endstop.*`：限位开关检测 | Endstop detection
- `command.*`：命令解析与执行 | Command parsing and execution
- `equipment.*`：机械臂设备抽象 | Robot arm equipment abstraction
- `logger.*`：日志与调试输出 | Logging and debug output
- `config*.h`：硬件配置（如引脚定义、参数设置）| Hardware configuration (pin definitions, parameters)
- `pinout/`：不同主控板的引脚映射 | Pin mapping for different mainboards

## 使用说明 | Usage
1. 根据实际硬件修改 `config.h` 和 `pinout/` 下的引脚定义。
2. 使用 Arduino IDE 或 PlatformIO 编译并上传固件到主控板。
3. 通过串口或网络发送控制指令，实现机械臂运动。

1. Modify `config.h` and pin definitions in `pinout/` according to your hardware.
2. Compile and upload the firmware to the mainboard using Arduino IDE or PlatformIO.
3. Send control commands via serial or network to operate the robot arm.

## 适用硬件 | Supported Hardware
- 主控板：ESP32 等
- 舵机、限位开关等外设

- Mainboard: ESP32 (e.g. Wemos D1 R32), Arduino Mega, etc.
- Servo, endstop switches, and other peripherals
