def setup():
    size(800, 800)
    colorMode(HSB, 360, 100, 100)
    noLoop()

def draw():
    background(0)
    translate(width/2, height/2)
    
    # 根据鼠标位置决定参数
    petalCount = int(map(mouseX, 0, width, 3, 12))
    recursionDepth = int(map(mouseY, 0, height, 2, 6))
    
    drawFlower(0, 0, 200, petalCount, recursionDepth)

def drawFlower(x, y, size, petals, depth):
    if depth == 0:
        return
    
    # 绘制花瓣
    for i in range(petals):
        angle = TWO_PI * i / petals
        nx = x + cos(angle) * size
        ny = y + sin(angle) * size
        
        # 设置颜色
        hue = (angle * 180/PI + frameCount) % 360
        fill(hue, 80, 90, 150)
        noStroke()
        ellipse(nx, ny, size, size)
        
        # 递归调用
        newSize = size * 0.6
        drawFlower(nx, ny, newSize, petals, depth-1)
    
    # 中心点
    fill(60, 80, 100)
    ellipse(x, y, size*0.3, size*0.3)

def mouseMoved():
    redraw()
