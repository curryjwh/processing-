class FluidParticle:
    def __init__(self):
        self.pos = PVector(random(width), random(height))
        self.prev_pos = self.pos.copy()
        self.vel = PVector(0, 0)
        self.acc = PVector(0, 0)
        self.max_speed = 4
        self.hue = random(255)
    
    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(self.max_speed)
        self.prev_pos = self.pos.copy()
        self.pos.add(self.vel)
        self.acc.mult(0)
        self.edges()
    
    def apply_force(self, force):
        self.acc.add(force)
    
    def follow(self, vectors, scl, cols):
        x = int(self.pos.x / scl)
        y = int(self.pos.y / scl)
        index = x + y * cols
        if 0 <= index < len(vectors):
            force = vectors[index]
            self.apply_force(force)
    
    def edges(self):
        if self.pos.x > width:
            self.pos.x = 0
            self.prev_pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width
            self.prev_pos.x = width
        if self.pos.y > height:
            self.pos.y = 0
            self.prev_pos.y = 0
        if self.pos.y < 0:
            self.pos.y = height
            self.prev_pos.y = height
    
    def show(self):
        stroke(self.hue, 255, 255, 25)
        strokeWeight(1)
        line(self.pos.x, self.pos.y, self.prev_pos.x, self.prev_pos.y)
    
    def show_point(self):
        stroke(self.hue, 255, 255)
        strokeWeight(2)
        point(self.pos.x, self.pos.y)

def setup():
    size(1000, 600)
    colorMode(HSB, 255)
    background(0)
    
    global particles, scl, cols, rows, zoff, flow_field
    
    scl = 20
    cols = width // scl
    rows = height // scl
    zoff = 0
    flow_field = [PVector() for _ in range(cols * rows)]
    
    particles = [FluidParticle() for _ in range(5000)]

def draw():
    global zoff
    
    # 更新流场
    yoff = 0
    for y in range(rows):
        xoff = 0
        for x in range(cols):
            index = x + y * cols
            angle = noise(xoff, yoff, zoff) * TWO_PI * 4
            v = PVector.fromAngle(angle)
            v.setMag(1)
            flow_field[index] = v
            xoff += 0.1
        yoff += 0.1
    zoff += 0.01
    
    # 更新粒子
    for p in particles:
        p.follow(flow_field, scl, cols)
        p.update()
        p.show()
    
    # 显示鼠标位置的流场向量
    if mousePressed:
        mx = mouseX // scl
        my = mouseY // scl
        if 0 <= mx < cols and 0 <= my < rows:
            index = mx + my * cols
            v = flow_field[index]
            stroke(255)
            strokeWeight(2)
            pushMatrix()
            translate(mx * scl + scl/2, my * scl + scl/2)
            rotate(v.heading())
            line(0, 0, scl/2, 0)
            popMatrix()
