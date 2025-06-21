def setup():
    global img, density, max_length, pixel_positions, current_index
    size(800, 600)
    background(255)
    
    img = loadImage("image1.jpg")
    img.resize(width, height)
    
    density = 4  # 更密的采样
    max_length = 40  # 更短的线条提高细节
    
    # 预计算所有需要绘制的像素位置并随机排序
    pixel_positions = []
    for y in range(0, height, density):
        for x in range(0, width, density):
            pixel_positions.append((x, y))
    # 随机打乱绘制顺序
    from random import shuffle
    shuffle(pixel_positions)
    
    current_index = 0
    
    strokeWeight(0.8)
    frameRate(2)  # 绘制速度

def draw():
    global current_index
    
    # 每次绘制更多线条
    for _ in range(500):
        if current_index >= len(pixel_positions):
            noLoop()
            print("素描完成!")
            save("improved_pencil_sketch.png")
            return
        
        x, y = pixel_positions[current_index]
        c = img.get(x, y)
        brightness_value = brightness(c)
        
        if brightness_value < 245:  # 更低的亮度阈值保留更多细节
            # 更自然的铅笔颜色变化
            r = red(c) + random(-15, 15)
            g = green(c) + random(-15, 15)
            b = blue(c) + random(-15, 15)
            pencil_color = color(
                constrain(r, 0, 255),
                constrain(g, 0, 255),
                constrain(b, 0, 255),
                120 + random(80))
            
            stroke(pencil_color)
            strokeWeight(0.5 + random(1.5))  # 更细的线条
            
            # 随机选择线条类型
            line_type = random(1)
            if line_type < 0.7:  # 画曲线
                draw_curved_line(x, y, brightness_value)
            elif line_type < 0.9:  # 画钟摆线
                draw_pendulum_line(x, y, brightness_value)
            else:  # 画直线
                draw_straight_line(x, y, brightness_value)
        
        current_index += 1

def draw_straight_line(x, y, brightness_val):
    angle = random(TWO_PI)
    length = random(3, max_length * (1.2 - brightness_val/255))  # 调整长度计算
    x2 = x + cos(angle) * length
    y2 = y + sin(angle) * length
    line(x, y, x2, y2)

def draw_curved_line(x, y, brightness_val):
    length = random(5, max_length * (1.1 - brightness_val/255))
    # 创建控制点产生曲线效果
    cx1 = x + random(-length, length)
    cy1 = y + random(-length, length)
    cx2 = x + random(-length, length)
    cy2 = y + random(-length, length)
    x2 = x + random(-length, length)
    y2 = y + random(-length, length)
    noFill()
    beginShape()
    curveVertex(x, y)
    curveVertex(x, y)
    curveVertex(cx1, cy1)
    curveVertex(cx2, cy2)
    curveVertex(x2, y2)
    curveVertex(x2, y2)
    endShape()

def draw_pendulum_line(x, y, brightness_val):
    length = random(10, max_length * (1 - brightness_val/255))
    angle = random(PI/6, PI/3)  # 初始角度
    segments = int(random(3, 8))  # 线段数量
    
    prev_x, prev_y = x, y
    for i in range(segments):
        # 模拟钟摆运动的角度变化
        angle += random(-0.3, 0.3)
        segment_length = length/segments * random(0.8, 1.2)
        next_x = prev_x + cos(angle) * segment_length
        next_y = prev_y + sin(angle) * segment_length
        line(prev_x, prev_y, next_x, next_y)
        prev_x, prev_y = next_x, next_y

def mousePressed():
    global current_index
    background(255)
    # 重新随机化绘制顺序
    from random import shuffle
    shuffle(pixel_positions)
    current_index = 0
    loop()
