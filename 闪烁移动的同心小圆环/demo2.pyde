# 定义每个圆的基础尺寸
circle_size = 25
# 初始化水平方向圆的数量为 0
num_circles_x = 0
# 初始化垂直方向圆的数量为 0
num_circles_y = 0
# 用于存储每个圆的移动方向，是一个二维列表
circle_directions = []

def setup():
    # 声明使用全局变量 num_circles_x 和 num_circles_y
    global num_circles_x, num_circles_y
    size(600, 600)
    frameRate(20)
    # 计算水平方向的圆的数量
    num_circles_x = width // circle_size
    # 计算垂直方向的圆的数量
    num_circles_y = height // circle_size
    # 遍历水平方向的圆
    for i in range(num_circles_x):
        # 初始化一个空列表来存储当前行的圆的移动方向
        row = []
        # 遍历垂直方向的圆
        for j in range(num_circles_y):
            # 为每个圆随机生成一个 x 方向的移动速度
            # 为每个圆随机生成一个 y 方向的移动速度
            # 将这两个速度组成一个列表并添加到当前行的列表中
            row.append([random(-5, 5), random(-4, 4)])
        # 将当前行的圆的移动方向列表添加到 circle_directions 列表中
        circle_directions.append(row)

def draw():
    background(0)
    # 遍历水平方向的圆
    for i in range(num_circles_x):
        # 遍历垂直方向的圆
        for j in range(num_circles_y):
            # 从 circle_directions 列表中获取当前圆的 x 和 y 方向的移动速度
            dx, dy = circle_directions[i][j]
            # 计算当前圆在的位置，使用取模运算确保圆在画布内循环移动
            x = (i * circle_size + dx * frameCount) % width
            y = (j * circle_size + dy * frameCount) % height
            r = random(255)
            g = random(255)
            b = random(255)
            fill(r, g, b)
            circle(x + circle_size / 2, y + circle_size / 2, circle_size)
            # 定义同心小圆的数量
            num = 4
            # 循环绘制同心小圆
            for k in range(num):
                # 计算每个同心小圆的半径
                radius = circle_size / 2 - (k + 1) * (circle_size / (2 * (num + 1)))
                r_small = random(255)
                g_small = random(255)
                b_small = random(255)
                fill(r_small, g_small, b_small)
                circle(x + circle_size / 2, y + circle_size / 2, 2 * radius,)
    
