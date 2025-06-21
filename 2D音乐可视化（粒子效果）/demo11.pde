import ddf.minim.*;

Minim minim;
AudioPlayer player;
ArrayList<MagneticParticle> particles;

void setup() {
    size(1000, 800);
    background(0);
    
    minim = new Minim(this);  
    player = minim.loadFile("believer.mp3");
    particles = new ArrayList<MagneticParticle>();
    
    // 创建粒子
    for (int i = 0; i < 150; i++) {
        particles.add(new MagneticParticle(random(width), random(height)));
    }
    
    if (player == null) {
        println("无法加载音乐文件");
        exit();
    }
    
    player.play();
}

void draw() {
    fill(0, 30);
    rect(0, 0, width, height);
    
    float audioLevel = player.mix.level();
    
    // 更新所有粒子
    for (int i = 0; i < particles.size(); i++) {
        MagneticParticle p = particles.get(i);
        
        // 计算磁场力（基于其他粒子位置）
        float totalForceX = 0;
        float totalForceY = 0;
        
        for (int j = 0; j < particles.size(); j++) {
            if (i != j) {
                MagneticParticle other = particles.get(j);
                float dx = other.x - p.x;
                float dy = other.y - p.y;
                float distance = sqrt(dx*dx + dy*dy);
                
                if (distance > 10 && distance < 100) {
                    // 音频影响磁场强度
                    float force = audioLevel * 50 / distance;
                    totalForceX += (dx / distance) * force;
                    totalForceY += (dy / distance) * force;
                }
            }
        }
        
        p.update(totalForceX, totalForceY, audioLevel);
        p.display();
    }
    
    // 绘制磁场线
    if (audioLevel > 0.05) {
        drawMagneticField(audioLevel);
    }
}

void drawMagneticField(float intensity) {
    stroke(100, 150, 255, intensity * 300);
    strokeWeight(1);
    
    for (int i = 0; i < particles.size()-1; i++) {
        MagneticParticle p1 = particles.get(i);
        for (int j = i+1; j < particles.size(); j++) {
            MagneticParticle p2 = particles.get(j);
            float distance = dist(p1.x, p1.y, p2.x, p2.y);
            
            if (distance < 80 && distance > 20) {
                float alpha = map(distance, 20, 80, 100, 10) * intensity;
                stroke(150, 200, 255, alpha);
                line(p1.x, p1.y, p2.x, p2.y);
            }
        }
    }
}

class MagneticParticle {
    float x, y;
    float vx, vy;
    float charge; // 电荷（正负影响吸引/排斥）
    color col;
    float size;
    ArrayList<PVector> trail;
    
    MagneticParticle(float x, float y) {
        this.x = x;
        this.y = y;
        this.vx = random(-1, 1);
        this.vy = random(-1, 1);
        this.charge = random(-1, 1);
        this.size = random(3, 8);
        this.trail = new ArrayList<PVector>();
        
        // 根据电荷设置颜色
        if (charge > 0) {
            this.col = color(255, 100, 100); // 红色为正电荷
        } else {
            this.col = color(100, 100, 255); // 蓝色为负电荷
        }
    }
    
    void update(float forceX, float forceY, float audioLevel) {
        // 施加磁场力
        vx += forceX * charge * 0.01;
        vy += forceY * charge * 0.01;
        
        // 音频影响运动
        vx += random(-audioLevel, audioLevel) * 2;
        vy += random(-audioLevel, audioLevel) * 2;
        
        // 位置更新
        x += vx;
        y += vy;
        
        // 边界处理
        if (x < 0 || x > width) vx *= -0.8;
        if (y < 0 || y > height) vy *= -0.8;
        x = constrain(x, 0, width);
        y = constrain(y, 0, height);
        
        // 阻尼
        vx *= 0.95;
        vy *= 0.95;
        
        // 更新轨迹
        trail.add(new PVector(x, y));
        if (trail.size() > 15) {
            trail.remove(0);
        }
        
        // 音频影响大小
        size = 3 + audioLevel * 10;
    }
    
    void display() {
        // 绘制轨迹
        noFill();
        strokeWeight(1);
        for (int i = 1; i < trail.size(); i++) {
            PVector current = trail.get(i);
            PVector previous = trail.get(i-1);
            float alpha = map(i, 0, trail.size(), 0, 150);
            stroke(red(col), green(col), blue(col), alpha);
            line(previous.x, previous.y, current.x, current.y);
        }
        
        // 绘制粒子
        fill(col, 200);
        noStroke();
        ellipse(x, y, size, size);
        
        // 电荷标识
        fill(255);
        textAlign(CENTER);
        text(charge > 0 ? "+" : "-", x, y + 3);
    }
}

void stop() {
    if (player != null) player.close();
    minim.stop();
    super.stop();
}
