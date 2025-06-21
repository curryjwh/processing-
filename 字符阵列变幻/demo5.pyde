def setup():
    size(500, 500)
    background(255)
    textSize(14)
    textAlign(CENTER, CENTER)
    colorMode(HSB, 360, 100, 100)
    frameRate(40)
    
    # 定义文字字符集
    global chars
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def draw():
    background(0)
    speed = radians(frameCount * 0.8)
    
    for x in range(50, 451, 30):
        for y in range(50, 451, 30):
            # 根据位置和时间计算字符索引
            charIndex = int(map(sin(speed + x*0.03 + y*0.05), -1, 1, 0, len(chars)-1))
            currentChar = chars[charIndex]
            
            # 根据位置和时间计算颜色
            hue = map(sin(speed + x*0.01), -1, 1, 0, 360)
            brightness = map(sin(speed + y*0.01), -1, 1, 50, 100)
            fill(hue, 80, brightness)
            
            # 根据位置和时间计算旋转角度和大小
            rotateAngle = speed * (x/500) * (y/500)
            sizeFactor = map(sin(speed + x*0.02 - y*0.02), -1, 1, 1, 3)
            
            pushMatrix()
            translate(x, y)
            rotate(rotateAngle)
            scale(sizeFactor)
            text(currentChar, 0, 0)
            popMatrix()
