class MagneticParticle:
    def __init__(self):
        self.pos = PVector(random(width), random(height))
        self.vel = PVector.random2D().mult(random(0.5, 2))
        self.acc = PVector(0, 0)
        self.maxspeed = 3
        self.size = random(2, 5)
        self.color = color(random(100, 200), random(100, 200), random(200, 255), 150)
    
    def update(self):
        # 计算鼠标对粒子的引力
        mouse = PVector(mouseX, mouseY)
        dir = PVector.sub(mouse, self.pos)
        distance = dir.mag()
        dir.normalize()
        
        # 距离越近引力越大
        if distance < 200:
            force = map(distance, 0, 200, 0.5, 0)
            dir.mult(force)
            self.acc.add(dir)
        
        # 物理运动
        self.vel.add(self.acc)
        self.vel.limit(self.maxspeed)
        self.pos.add(self.vel)
        self.acc.mult(0)
        
        # 边界检查
        self.bounce_edges()
    
    def bounce_edges(self):
        if self.pos.x < 0 or self.pos.x > width:
            self.vel.x *= -0.8
        if self.pos.y < 0 or self.pos.y > height:
            self.vel.y *= -0.8
        self.pos.x = constrain(self.pos.x, 0, width)
        self.pos.y = constrain(self.pos.y, 0, height)
    
    def display(self):
        noStroke()
        fill(self.color)
        ellipse(self.pos.x, self.pos.y, self.size, self.size)
    
    def connect(self, particles):
        for other in particles:
            d = PVector.dist(self.pos, other.pos)
            if d < 50 and self != other:
                stroke(random(50,255), random(50,255), random(50,255), map(d, 0, 50, 100, 50))
                line(self.pos.x, self.pos.y, other.pos.x, other.pos.y)

particles = []

def setup():
    size(1000, 600)
    for _ in range(250):
        particles.append(MagneticParticle())

def draw():
    background(20)
    for p in particles:
        p.update()
        p.display()
        p.connect(particles)
    
    # 显示鼠标影响范围
    noFill()
    stroke(255, 50)
    ellipse(mouseX, mouseY, 400, 400)
