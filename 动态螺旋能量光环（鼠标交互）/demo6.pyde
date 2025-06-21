def setup():
    size(800, 800)
    background(0)
    colorMode(HSB, 360, 100, 100)
    noFill()
    strokeWeight(2)
    
def draw():
    fill(0, 15)
    rect(0, 0, width, height)
    translate(width/2, height/2)
    # 鼠标交互控制参数
    twist = map(mouseX, 0, width, -3, 3)
    layers = int(map(mouseY, 0, height, 3, 10))
    for layer in range(layers):
        # 动态颜色（每层不同）
        hue = (frameCount * 0.7 + layer * 30) % 360
        stroke(hue, 100, 100)
        
        beginShape()
        for angle in range(0, 360, 2):
            rad = radians(angle)
            # 动态扭曲效果
            twisted_rad = rad + twist * sin(rad * 4 + frameCount * 0.02)
            # 脉冲半径
            pulse = sin(rad * 6 + frameCount * 0.05) * 30
            radius = 150 + layer * 30 + pulse
            x = radius * cos(twisted_rad)
            y = radius * sin(twisted_rad)
            curveVertex(x, y)
        endShape(CLOSE)
        
        # 添加随机光点
        if random(1) < 0.03:
            random_angle = random(TWO_PI)
            r = 150 + layer * 30 + pulse
            fill(hue, 100, 100, 150)
            noStroke()
            circle(r * cos(random_angle), r * sin(random_angle), random(2, 5))
            noFill()
            stroke(hue, 100, 100)
