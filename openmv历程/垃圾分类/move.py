# move.py - 机械臂垃圾分拣动作控制模块
"""
该模块包含了不同类型垃圾的机械臂抓取和分拣动作序列
支持四种垃圾分类：厨余垃圾、其他垃圾、有害垃圾、可回收垃圾
"""

import time

def move_kitchen_garbage(robot, actuator):
    """
    厨余垃圾分拣动作序列
    
    参数:
        robot: 机械臂控制对象
        actuator: 执行器高度偏移量
    
    动作流程:
        1. 移动到抓取准备位置
        2. 下降并打开夹爪
        3. 夹紧垃圾
        4. 移动到厨余垃圾桶（左前方位置 -120,124）
        5. 释放垃圾并返回初始位置
    """
    print("执行厨余垃圾分拣动作...")
    
    # 移动到抓取准备位置（中心上方）
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 下降到抓取高度
    robot.set_xyz_point(0, 217, 50+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 打开夹爪准备抓取
    robot.mv_servo(10)
    time.sleep_ms(1000)
    
    # 进一步下降接近垃圾
    robot.set_xyz_point(0, 217, 18+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 夹紧夹爪抓取垃圾
    robot.mv_servo(46)
    time.sleep_ms(1000)
    
    # 抬升到安全运输高度
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 移动到厨余垃圾桶上方（左前方）
    robot.set_xyz_point(-120, 124, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 下降到垃圾桶内
    robot.set_xyz_point(-120, 124, 150+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 松开夹爪释放垃圾
    robot.mv_servo(20)
    time.sleep_ms(1000)
    
    # 返回初始位置
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)


def move_other_garbage(robot, actuator):
    """
    其他垃圾分拣动作序列
    
    参数:
        robot: 机械臂控制对象
        actuator: 执行器高度偏移量
    
    动作流程:
        1. 移动到抓取准备位置
        2. 下降并打开夹爪
        3. 夹紧垃圾
        4. 移动到其他垃圾桶（左后方位置 -120,220）
        5. 释放垃圾并返回初始位置
    """
    print("执行其他垃圾分拣动作...")
    
    # 移动到抓取准备位置
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 下降到抓取高度
    robot.set_xyz_point(0, 217, 50+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 打开夹爪
    robot.mv_servo(10)
    time.sleep_ms(1000)
    
    # 进一步下降
    robot.set_xyz_point(0, 217, 18+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 夹紧垃圾
    robot.mv_servo(46)
    time.sleep_ms(1000)
    
    # 抬升到安全高度
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 移动到其他垃圾桶上方（左后方）
    robot.set_xyz_point(-120, 220, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 下降到垃圾桶内
    robot.set_xyz_point(-120, 220, 150+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 释放垃圾
    robot.mv_servo(20)
    time.sleep_ms(1000)
    
    # 返回初始位置
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)


def move_harmful_waste(robot, actuator):
    """
    有害垃圾分拣动作序列
    
    参数:
        robot: 机械臂控制对象
        actuator: 执行器高度偏移量
    
    动作流程:
        1. 移动到抓取准备位置
        2. 下降并打开夹爪
        3. 夹紧垃圾
        4. 移动到有害垃圾桶（右前方位置 120,124）
        5. 释放垃圾并返回初始位置
    """
    print("执行有害垃圾分拣动作...")
    
    # 移动到抓取准备位置
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 下降到抓取高度
    robot.set_xyz_point(0, 217, 50+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 打开夹爪
    robot.mv_servo(10)
    time.sleep_ms(1000)
    
    # 进一步下降
    robot.set_xyz_point(0, 217, 18+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 夹紧垃圾
    robot.mv_servo(46)
    time.sleep_ms(1000)
    
    # 抬升到安全高度
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 移动到有害垃圾桶上方（右前方）
    robot.set_xyz_point(120, 124, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 下降到垃圾桶内
    robot.set_xyz_point(120, 124, 150+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 释放垃圾
    robot.mv_servo(20)
    time.sleep_ms(1000)
    
    # 返回初始位置
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)


def move_recyclable_garbage(robot, actuator):
    """
    可回收垃圾分拣动作序列
    
    参数:
        robot: 机械臂控制对象
        actuator: 执行器高度偏移量
    
    动作流程:
        1. 移动到抓取准备位置
        2. 下降并打开夹爪
        3. 夹紧垃圾
        4. 移动到可回收垃圾桶（右后方位置 120,220）
        5. 释放垃圾并返回初始位置
    """
    print("执行可回收垃圾分拣动作...")
    
    # 移动到抓取准备位置
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 下降到抓取高度
    robot.set_xyz_point(0, 217, 50+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 打开夹爪
    robot.mv_servo(10)
    time.sleep_ms(1000)
    
    # 进一步下降
    robot.set_xyz_point(0, 217, 18+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 夹紧垃圾
    robot.mv_servo(46)
    time.sleep_ms(1000)
    
    # 抬升到安全高度
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 移动到可回收垃圾桶上方（右后方）
    robot.set_xyz_point(120, 220, 222+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 下降到垃圾桶内
    robot.set_xyz_point(120, 220, 150+actuator, 0, 0)
    time.sleep_ms(1000)
    
    # 释放垃圾
    robot.mv_servo(20)
    time.sleep_ms(1000)
    
    # 返回初始位置
    robot.set_xyz_point(0, 174, 222+actuator, 0, 0)
    time.sleep_ms(1000)


def execute_garbage_sorting(robot, actuator, garbage_type):
    """
    根据垃圾类型执行相应的分拣动作
    
    参数:
        robot: 机械臂控制对象
        actuator: 执行器高度偏移量
        garbage_type: 垃圾类型字符串
    
    支持的垃圾类型:
        - "kitchen_garbage": 厨余垃圾
        - "other": 其他垃圾
        - "harmful_waste": 有害垃圾
        - "recyclable_garbage": 可回收垃圾
    """
    if garbage_type == "kitchen_garbage":
        move_kitchen_garbage(robot, actuator)
    elif garbage_type == "other":
        move_other_garbage(robot, actuator)
    elif garbage_type == "harmful_waste":
        move_harmful_waste(robot, actuator)
    elif garbage_type == "recyclable_garbage":
        move_recyclable_garbage(robot, actuator)
    else:
        print(f"未识别的垃圾类型: {garbage_type}")