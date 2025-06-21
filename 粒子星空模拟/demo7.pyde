particles = []
stars = []
meteors = []

def setup():
    size(1000, 800)
    noStroke()
    smooth()
    
    # 创建普通粒子
    for i in range(800):
        x = random(0, width)
        y = random(0, height)
        v_mag = random(0.5, 1.5)
        v_angle = random(-PI, PI)
        c = color(random(150, 255), random(150, 255), random(150, 255), 150)
        particle = [x, y, v_mag, v_angle, c, random(1, 3)]  # 增加大小参数
        particles.append(particle)
    
    # 创建星星
    for i in range(200):
        x = random(0, width)
        y = random(0, height)
        size = random(0.5, 2.5)
        twinkle_speed = random(0.01, 0.05)
        c = color(255, 255, 255)
        stars.append([x, y, size, twinkle_speed, c, 0])  # 最后一个是闪烁状态
    
    # 创建流星
    for i in range(3):
        create_meteor()

def create_meteor():
    x = random(-100, width + 100)
    y = random(-100, -50)
    speed = random(5, 10)
    angle = random(PI/6, PI/3)  # 30-60度角
    length = random(50, 150)
    c = color(random(200, 255), random(200, 255), 255)
    lifespan = int(random(100, 200))
    meteors.append([x, y, speed, angle, length, c, lifespan])

def draw():
    # 深色背景
    fill(5, 10, 20, 25)
    rect(0, 0, width, height)
    
    # 绘制星星
    for star in stars:
        # 星星闪烁效果
        star[5] += star[3]
        alpha = 100 + 155 * abs(sin(star[5]))
        fill(red(star[4]), green(star[4]), blue(star[4]), alpha)
        circle(star[0], star[1], star[2])
    
    # 绘制流星
    for meteor in meteors[:]:
        # 流星头部
        fill(meteor[5])
        circle(meteor[0], meteor[1], 5)
        
        # 流星尾巴
        for i in range(1, int(meteor[4]/5)):
            tail_x = meteor[0] - i * 5 * cos(meteor[3])
            tail_y = meteor[1] - i * 5 * sin(meteor[3])
            tail_alpha = 255 * (1 - i/(meteor[4]/5))
            fill(red(meteor[5]), green(meteor[5]), blue(meteor[5]), tail_alpha)
            circle(tail_x, tail_y, 3 * (1 - i/(meteor[4]/5)))
        
        # 移动流星
        meteor[0] += meteor[2] * cos(meteor[3])
        meteor[1] += meteor[2] * sin(meteor[3])
        meteor[6] -= 1
        
        # 移除寿命结束的流星
        if meteor[6] <= 0 or meteor[0] > width + 100 or meteor[1] > height + 100:
            meteors.remove(meteor)
            # 有概率创建新流星
            if random(1) < 0.5:
                create_meteor()
    
    # 绘制粒子
    for particle in particles:
        # 使用噪声控制运动方向
        noiseValue = noise(0.001 * particle[0], 10 + 0.001 * particle[1], frameCount * 0.003)
        particle[3] = map(noiseValue, 0, 1, -PI, PI)
        
        # 计算速度分量
        vx = particle[2] * cos(particle[3])
        vy = particle[2] * sin(particle[3])
        
        # 更新位置
        particle[0] += vx
        particle[1] += vy
        
        # 边界检查
        if particle[0] < 0 or particle[0] > width or particle[1] < 0 or particle[1] > height:
            if random(1) < 0.1:  # 10%概率从边缘重生
                if random(1) < 0.5:
                    particle[0] = 0 if random(1) < 0.5 else width
                    particle[1] = random(0, height)
                else:
                    particle[0] = random(0, width)
                    particle[1] = 0 if random(1) < 0.5 else height
            else:  # 90%概率随机重生
                particle[0] = random(0, width)
                particle[1] = random(0, height)
            
            # 随机颜色变化
            r = map(sin(frameCount / 75.0 + random(-1, 1)), -1, 1, 100, 255)
            g = map(sin(frameCount / 101.0 + random(-1, 1)), -1, 1, 100, 255)
            b = map(sin(frameCount / 151.0 + random(-1, 1)), -1, 1, 100, 255)
            particle[4] = color(r, g, b, 150)
        
        # 绘制粒子
        fill(particle[4])
        circle(particle[0], particle[1], particle[5])
        
        # 随机连接附近的粒子
        if random(1) < 0.02:  # 2%的概率绘制连接线
            for other in particles:
                if other != particle and dist(particle[0], particle[1], other[0], other[1]) < 50:
                    stroke(red(particle[4]), green(particle[4]), blue(particle[4]), 50)
                    line(particle[0], particle[1], other[0], other[1])
                    noStroke()
    
    # 偶尔添加新流星
    if frameCount % 120 == 0 and random(1) < 0.7:
        create_meteor()
