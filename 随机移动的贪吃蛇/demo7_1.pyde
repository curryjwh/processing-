particles = []
NUM_PARTICLES = 200  # 增加粒子数量
MAX_SPEED = 6        # 最大速度
MIN_SIZE = 1         # 最小尺寸
MAX_SIZE = 10        # 增加最大尺寸

# 颜色配置
COLOR_VARIATION = 25  # 颜色随机波动范围
HUE_SPEED = 0.7       # 色调变化速度
GLOW_INTENSITY = 1.5  # 发光强度

def setup():
    size(1000, 800)
    colorMode(HSB, 360, 100, 100, 100)
    noStroke()
    smooth()
    
    # 创建初始粒子
    for _ in range(NUM_PARTICLES):
        create_particle()

def create_particle():
    x = random(width)
    y = random(height)
    angle = random(TWO_PI)
    speed = random(1, MAX_SPEED)
    hue = random(360)
    size = random(MIN_SIZE, MAX_SIZE)
    hue_offset = random(-COLOR_VARIATION, COLOR_VARIATION)
    particles.append([
        x, y, 
        cos(angle) * speed, 
        sin(angle) * speed, 
        hue, size,
        [],  # 轨迹点
        random(100),  # 噪声种子
        hue_offset,   # 颜色偏移
        random(0.005, 0.02),  # 个体颜色变化速度
        random(0.5, 1.5),      # 个体大小变化系数
        random(0.7, 1.3),      # 个体速度变化系数
        random(0.01, 0.03),    # 颜色波动速度
        random(0.8, 1.2),      # 颜色波动强度
        random(0.9, 1.1)       # 大小波动系数
    ])

def draw():
    background(0, 0, 3, 20)  # 降低背景不透明度，增强轨迹效果
    
    # 更新和绘制粒子
    for p in particles:
        # 使用改进的噪声函数产生更自然的运动
        n = noise(p[7]) * TWO_PI * 2
        p[2] = cos(n) * MAX_SPEED * 0.8 * p[10]  # 应用个体速度系数
        p[3] = sin(n) * MAX_SPEED * 0.8 * p[10]
        p[7] += 0.015  # 更新噪声种子
        
        # 添加颜色变化 - 更丰富的波动效果
        hue_wave = sin(frameCount * p[11]) * p[12] * 10
        p[4] = (p[4] + HUE_SPEED * p[9] + hue_wave) % 360
        
        # 大小波动
        size_wave = sin(frameCount * p[11] * 0.7) * 0.2 * p[14]
        p[5] = constrain(p[5] + size_wave, MIN_SIZE, MAX_SIZE)
        
        # 添加当前位置到轨迹
        p[6].append((p[0], p[1]))
        if len(p[6]) > 80:  # 增加轨迹长度
            p[6].pop(0)
        
        # 更新位置
        p[0] += p[2]
        p[1] += p[3]
        
        # 边界反弹(更自然的反弹)
        if p[0] < 0: 
            p[0] = 0
            p[2] = abs(p[2]) * random(0.7, 0.9)
        elif p[0] > width: 
            p[0] = width
            p[2] = -abs(p[2]) * random(0.7, 0.9)
        if p[1] < 0: 
            p[1] = 0
            p[3] = abs(p[3]) * random(0.7, 0.9)
        elif p[1] > height: 
            p[1] = height
            p[3] = -abs(p[3]) * random(0.7, 0.9)
        
        # 绘制渐变轨迹(使用更丰富的颜色映射)
        for i, (tx, ty) in enumerate(p[6]):
            alpha = map(i, 0, len(p[6]), 20, 100)  # 透明度渐变
            radius = map(i, 0, len(p[6]), p[5]*0.3, p[5]*1.5)  # 大小渐变
            hue = (p[4] + i * 1.5 + frameCount * 0.2) % 360  # 轨迹颜色渐变
            saturation = constrain(80 + i * 0.5, 70, 100)
            fill(hue, saturation, 100, alpha)
            circle(tx, ty, radius)
        
        # 绘制增强的发光效果
        enhanced_glow(p[0], p[1], p[5], p[4], p[8], p[13])

def enhanced_glow(x, y, size, hue, hue_offset, glow_intensity):
    """增强的发光效果，使用多层光晕和不同透明度"""
    # 外层大光晕 - 添加动态变化
    for i in range(7, 2, -1):
        dynamic_hue = (hue + sin(frameCount * 0.02 + i) * 10) % 360
        fill(dynamic_hue, 50 + hue_offset, 100, 5/i * glow_intensity)
        circle(x + random(-2, 2), y + random(-2, 2), size * i * 3)
    
    # 中层光晕 - 添加闪烁效果
    for i in range(5, 0, -1):
        flash = sin(frameCount * 0.05 + i) * 0.2 + 0.8
        dynamic_hue = (hue + sin(frameCount * 0.03 + i) * 15) % 360
        fill(dynamic_hue, 70 + hue_offset, 100, 15/i * flash * glow_intensity)
        circle(x + random(-1, 1), y + random(-1, 1), size * i * 2.5)
    
    # 内层光晕 - 更明亮的中心
    flash = sin(frameCount * 0.07) * 0.3 + 0.7
    fill(hue, 90 + hue_offset, 100, 40 * flash * glow_intensity)
    circle(x, y, size * 3)
    
    # 粒子核心 - 添加高光点
    core_brightness = 100 - (size * 5)
    fill(hue, 100, core_brightness)
    circle(x, y, size * 1.2)
    
    # 高光点 - 动态变化
    highlight_size = size * 0.5 * (sin(frameCount * 0.1) * 0.3 + 0.7)
    fill(hue, 30, 100, 90)
    circle(x + size * 0.3 * cos(frameCount * 0.1), 
           y + size * 0.3 * sin(frameCount * 0.1), 
           highlight_size)
