def setup(): 
    global maxThickness, offset, spray_radius, dot_count  
    size(1200, 700)  
    strokeWeight(5)  # 设置线条粗细
    background(255)  
    maxThickness = 25  # 最粗笔触
    offset = 2  # 用于画偏移分叉线
    spray_radius = 20  # 喷枪的半径，控制喷枪效果的范围
    dot_count = 50  # 每次绘制时生成的点的数量


def draw():  # 绘制函数，每帧重复运行
    return  # 函数直接返回

def mousePressed():  # 当鼠标按键时
    global lastX, lastY, vx, vy, lastThickness  
    lastX = mouseX  
    lastY = mouseY
    # 移动的速度初始化
    vx = 0  
    vy = 0
    lastThickness = 1  # 鼠标刚按下时，笔触粗细为1


def mouseDragged():  # 当鼠标按键后拖动时
    global lastX, lastY, vx, vy, lastThickness, brush_type, spray_radius, dot_count
    vx = 0.7 * vx + 0.3 * (mouseX - lastX)  # 获得当前移动速度，保持连续插值
    vy = 0.7 * vy + 0.3 * (mouseY - lastY)
    v = sqrt(vx * vx + vy * vy)  # 当前移动速度的模
    
    # 速度越快，笔触越细
    nextThickness = maxThickness - v
    if nextThickness < 0:  # 防止粗细小于0
        nextThickness = 0
    # 笔触的粗细也需要连续，防止变化太剧烈
    nextThickness = 0.5 * nextThickness + 0.5 * lastThickness

    n = 10 + int(v / 2)  # 速度越快，分段数越高
    for i in range(1, n + 1):  # 将鼠标前后两个点间分成n段绘制
        x1 = map(i - 1, 0, n, lastX, mouseX)  # 对应的前后两个顶点坐标
        y1 = map(i - 1, 0, n, lastY, mouseY)
        x2 = map(i, 0, n, lastX, mouseX)
        y2 = map(i, 0, n, lastY, mouseY)
        # 对应的这一小段的粗细
        thickness = map(i - 1, 0, n, lastThickness, nextThickness)
        
        # 蜡笔效果：随机绘制小点模拟颗粒感
        if brush_type == 'crayon':
            for _ in range(int(thickness)):
                dx = random(-thickness / 2, thickness / 2)
                dy = random(-thickness / 2, thickness / 2)
                point(x1 + dx, y1 + dy)
                
        # 粉笔效果：半透明线条和随机偏移
        elif brush_type == 'chalk':
            stroke(0, 100)  # 半透明黑色
            strokeWeight(thickness)
            dx = random(-thickness / 2, thickness / 2)
            dy = random(-thickness / 2, thickness / 2)
            line(x1 + dx, y1 + dy, x2 + dx, y2 + dy)
            
        # 油画笔效果：多个重叠线条模拟厚实感
        elif brush_type == 'oil_painting':
            for j in range(int(thickness / 2)):
                dx = random(-thickness / 4, thickness / 4)
                dy = random(-thickness / 4, thickness / 4)
                strokeWeight(thickness - j)
                line(x1 + dx, y1 + dy, x2 + dx, y2 + dy)
                
        # 喷枪效果
        elif brush_type == 'spray_gun':
            for _ in range(dot_count):
                # 随机生成在喷枪半径范围内的偏移量
                dx = random(-spray_radius, spray_radius)
                dy = random(-spray_radius, spray_radius)
                # 计算点的实际位置
                x = x1 + dx
                y = y1 + dy
                # 确保点在画布范围内
                if 0 <= x < width and 0 <= y < height:
                    # 设置绘制颜色为黑色
                    stroke(0)
                    # 设置点的大小
                    strokeWeight(2)
                    # 绘制点
                    point(x, y)
                    
        # 毛笔效果
        else:
            strokeWeight(thickness + offset)
            line(x1, y1, x2, y2) # 画主线
            strokeWeight(thickness)
            line(x1 + offset * 2, y1 + offset * 2, x2 + offset * 2, y2 + offset * 2)
            line(x1 - offset, y1 - offset, x2 - offset, y2 - offset)

    lastX = mouseX  # 更新前一个点的坐标
    lastY = mouseY
    lastThickness = nextThickness


def keyPressed():  # 当按下任意键盘按键时
    global brush_type
    if key == '1':  # 切换到蜡笔效果
        brush_type = 'crayon'
    elif key == '2':  # 切换到粉笔效果
        brush_type = 'chalk'
    elif key == '3':  # 切换到油画笔效果
        brush_type = 'oil_painting'
    elif key == '4':  # 切换到毛笔效果
        brush_type = 'brush'
    elif key == '5':  # 切换到喷枪效果
        brush_type = 'spray_gun'
    elif key == ' ':  # 清空画布
        background(255)


brush_type = 'brush'
    
