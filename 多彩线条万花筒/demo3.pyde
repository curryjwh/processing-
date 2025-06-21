import math
import random

# 定义线条的数量
num_lines = 100
# 定义旋转速度，控制图案旋转的快慢
rotation_speed = 0.05
# 定义线条长度比例，用于控制线条的长度
line_length_ratio = 0.8

def setup():
    size(600, 600)
    background(255)
    noFill()
    frameRate(35)
    strokeWeight(1)

def draw():
    background(255)
    # 将坐标系的原点移动到画布中心（默认为左上角）
    translate(width / 2, height / 2)
    # 外层循环，控制线条的数量
    for i in range(num_lines):
        # 计算当前线条的起始角度，使线条按等角度分布
        angle = i * (2 * math.pi / num_lines)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        # 设置当前线条的颜色
        stroke(r, g, b)
        # 内层循环，控制线条的不同长度层次
        for j in range(1, 10):
            # 计算线条起点到中心的距离
            r1 = j * width / 10
            # 计算线条终点到中心的距离，根据长度比例计算
            r2 = r1 * line_length_ratio
            # 
            x1 = r1 * math.cos(angle)
            y1 = r1 * math.sin(angle)
            # 根据弧度计算实际坐标系下终点坐标
            x2 = r2 * math.cos(angle + rotation_speed * frameCount)
            y2 = r2 * math.sin(angle + rotation_speed * frameCount)
            # 绘制线条，连接起点和终点
            line(x1, y1, x2, y2)
    # 每绘制一帧就旋转一定角度，从而实现动态的旋转效果
    rotate(rotation_speed*PI)
