import ddf.minim.*;
import ddf.minim.analysis.*;

// 音频处理与可视化的全局变量
Minim minim;           // Minim 音频库实例
AudioPlayer player;    // 音频播放器
FFT fft;               // 快速傅里叶变换，用于频谱分析
float aX, aY, scl = 1, mX, mY, rSpeed = 0.005, zSpeed = 0.002;  // 视角控制参数
float pmX, pmY;        // 鼠标位置记录
int res = 128, bands = 512;  // 分辨率和频谱分析频段数
float rBase = 150, wAmp = 60, sAmp = 30, rThick = 20, rDepth = 30;  // 可视化几何参数
float[] wf, spec, sSpec, sWf;  // 存储波形和频谱数据的数组
color[] cols;                  // 存储颜色的数组
int spCount = 5, spSeg = 150;  // 螺旋线数量和分段数
float spColSpeed = 0.005;      // 螺旋线颜色变化速度
float[] sX, sY, sZ, sSize;     // 星星(背景点)的位置和大小
int sCount = 400;              // 星星数量
Particle[] parts;              // 粒子系统

// 粒子类 - 代表可视化中的动态粒子元素
class Particle {
  float x, y, z, spd, hue, sz;  // 粒子属性：位置、速度、色调、大小
  
  // 粒子构造函数，初始化随机位置、速度等属性
  Particle() {
    x = random(-width, width); y = random(-height, height); z = random(-width, width);
    spd = random(0.5, 2); hue = random(360); sz = random(1, 3);
  }
  // 粒子更新方法 - 每帧更新粒子位置和大小
  void update() {
    x += spd * cos(frameCount * 0.002 + z * 0.01);  // 基于时间和深度的水平移动
    y += spd * sin(frameCount * 0.002 + z * 0.01);  // 基于时间和深度的垂直移动
    // 如果粒子移出边界，重新随机初始化
    if (x < -width || x > width || y < -height || y > height) {
      x = random(-width, width); y = random(-height, height); z = random(-width, width);
    }
    // 根据粒子深度位置获取对应频段的频谱值，并调整粒子大小
    int b = (int)map(z, -width, width, 0, bands);
    if (b < bands) sz = map(sSpec[b], 0, 1, 0.5, 4);
  }
  // 粒子渲染方法 - 在3D空间中绘制粒子
  void display() {
    pushMatrix(); translate(x, y, z);  // 移动到粒子位置
    fill(hue, 60, 80, 80); ellipse(0, 0, sz, sz);  // 绘制半透明圆形表示粒子
    popMatrix();  // 恢复之前的变换矩阵
  }
}

void setup() {
  size(800, 800, P3D);  // 创建800x800的3D画布
  hint(ENABLE_DEPTH_TEST);  // 启用深度测试，确保3D对象正确显示
  minim = new Minim(this);  // 初始化Minim音频库
  player = minim.loadFile("color-x.mp3", 1024);  // 加载音频文件
  player.loop();  // 设置音频循环播放
  fft = new FFT(player.bufferSize(), player.sampleRate());  // 初始化FFT频谱分析
  fft.logAverages(10, 10);  // 设置对数平均频谱分析
  
  // 初始化各种数据数组
  wf = new float[player.bufferSize()]; spec = new float[bands];
  sSpec = new float[bands]; sWf = new float[player.bufferSize()];
  cols = new color[res];
  
  // 初始化星星(背景点)的位置和大小
  sX = new float[sCount]; sY = new float[sCount];
  sZ = new float[sCount]; sSize = new float[sCount];
  
  // 初始化粒子系统
  parts = new Particle[100];
  for (int i = 0; i < sCount; i++) {
    float a = random(TWO_PI); float d = random(width/2);
    sX[i] = cos(a) * d; sY[i] = sin(a) * d;  // 星星在圆形区域内随机分布
    sZ[i] = random(-width, width); sSize[i] = random(1, 3);  // 随机深度和大小
  }
  
  // 创建粒子对象
  for (int i = 0; i < parts.length; i++) parts[i] = new Particle();
  
  // 设置HSB颜色模式并初始化颜色数组
  colorMode(HSB, 360, 100, 100);
  for (int i = 0; i < res; i++) cols[i] = color(map(i, 0, res, 0, 360), 60, 85);
  noStroke();  // 不绘制描边
}

// 主循环方法 - 每帧调用一次
void draw() {
  background(0);  // 清屏为黑色
  drawParts(); drawStars();  // 绘制粒子和星星背景
  
  // 设置3D变换 - 平移、缩放和旋转
  translate(width/2 + mX, height/2 + mY);  // 平移到画布中心并应用用户偏移
  scale(scl);  // 应用缩放
  rotateY(rSpeed * frameCount + aY);  // 绕Y轴旋转(水平旋转)
  rotateX(zSpeed * frameCount + aX);  // 绕X轴旋转(垂直旋转)
  
  updateAudio();  // 更新音频数据
  drawSpirals();  // 绘制螺旋线
  drawWaveRing();  // 绘制波形环
  drawSpecCircle();  // 绘制频谱圆
  drawControl();  // 绘制控制界面
}

// 绘制粒子系统
void drawParts() {
  pushMatrix(); translate(width/2 + mX, height/2 + mY); scale(scl);  // 应用变换
  for (Particle p : parts) { p.update(); p.display(); }  // 更新并显示所有粒子
  popMatrix();  // 恢复变换
}

// 更新音频数据 - 从音频缓冲区获取波形和频谱
void updateAudio() {
  // 获取波形数据并平滑处理
  for (int i = 0; i < player.bufferSize(); i++)
    sWf[i] = lerp(sWf[i], player.left.get(i), 0.2);  // 线性插值平滑波形
  
  // 执行FFT频谱分析并平滑处理频谱数据
  fft.forward(player.mix);
  for (int i = 0; i < bands; i++) {
    int idx = (int)map(i, 0, bands, 0, fft.specSize()-1);
    sSpec[i] = lerp(sSpec[i], fft.getBand(idx), 0.3);  // 线性插值平滑频谱
  }
}

// 绘制星星背景
void drawStars() {
  pushMatrix(); translate(width/2 + mX, height/2 + mY); scale(scl);  // 应用变换
  
  // 绘制所有星星，部分星星亮度随音频变化
  for (int i = 0; i < sCount; i++) {
    float mx = sin(frameCount * 0.001 + i) * 0.5;  // 轻微的水平抖动
    float my = cos(frameCount * 0.001 + i) * 0.5;  // 轻微的垂直抖动
    
    // 每隔几个星星使用音频频谱控制亮度
    fill(i % 8 == 0 ? color(255, map(sSpec[i % bands], 0, 1, 50, 255)) : color(255, 100));
    ellipse(sX[i] + mx, sY[i] + my, sSize[i] + sin(frameCount * 0.005 + i) * 0.3, 
           sSize[i] + sin(frameCount * 0.005 + i) * 0.3);  // 绘制星星，大小随时间轻微变化
  }
  
  // 计算平均频谱值，用于控制脉冲效果
  float avg = 0; for (int i = 0; i < bands; i++) avg += sSpec[i];
  avg /= bands; float pulse = map(avg, 0, 0.5, 0.95, 1.05);
  
  // 绘制两个脉冲圆环，大小随音频强度变化
  noFill(); stroke(100, 100, 255, 10); strokeWeight(2);
  ellipse(0, 0, width * 1.2 * pulse, width * 1.2 * pulse);
  stroke(240, 100, 255, 15); strokeWeight(1);
  ellipse(0, 0, width * 0.8 * pulse, width * 0.8 * pulse);
  
  popMatrix();  // 恢复变换
}

// 绘制螺旋线 - 随音频节奏波动的线条
void drawSpirals() {
  for (int s = 0; s < spCount; s++) {  // 绘制多条螺旋线
    float r = 250 + s * 15;  // 每条螺旋线的基础半径
    float ph = s * TWO_PI / spCount + frameCount * 0.005;  // 螺旋线的相位，随时间变化
    float fa = fft.getAvg(s % fft.avgSize());  // 获取特定频段的平均值，控制波动幅度
    
    beginShape(LINES);  // 开始绘制线段
    for (int i = 0; i < spSeg; i++) {  // 每条螺旋线由多个线段组成
      float t = i * TWO_PI / spSeg;  // 当前角度
      float z = map(i, 0, spSeg, -400, 400);  // Z轴位置，形成3D效果
      float w = map(fa, 0, 50, 0, 20) * sin(t + frameCount * 0.03 + ph);  // 基于音频的波动
      float x = (r + w) * cos(t + ph);  // 计算X坐标
      float y = (r + w) * sin(t + ph);  // 计算Y坐标
      
      // 基于时间和位置计算颜色
      float h = map(sin(t + frameCount * spColSpeed), -1, 1, 180, 300);
      float b = map(fa, 0, 50, 50, 90);  // 亮度随音频变化
      
      stroke(h, 70, b); strokeWeight(map(fa, 0, 50, 1, 3));  // 线条颜色和粗细随音频变化
      vertex(x, y, z);  // 添加线段顶点
    }
    endShape();  // 结束绘制
  }
}

// 绘制波形环 - 基于音频波形数据的环形可视化
void drawWaveRing() {
  for (int i = 0; i < res; i++) {  // 沿圆周均匀分布多个扇形
    float a = map(i, 0, res, 0, TWO_PI);  // 当前角度
    float r = rBase + sWf[(int)map(i, 0, res, 0, sWf.length-1)] * wAmp;  // 基于波形数据的半径
    fill(cols[i % res]);  // 使用预定义的颜色
    pushMatrix(); rotate(a);  // 旋转到当前角度
    beginShape();  // 开始绘制扇形
    vertex(r, 0, 0); vertex(r, 0, -rDepth);  // 外边缘
    vertex(r - rThick, 0, -rDepth); vertex(r - rThick, 0, 0);  // 内边缘
    endShape();  // 结束绘制
    popMatrix();  // 恢复旋转
  }
}

// 绘制频谱圆 - 基于音频频谱数据的圆形可视化
void drawSpecCircle() {
  for (int i = 0; i < res; i++) {  // 沿圆周均匀分布多个矩形条
    float a = map(i, 0, res, 0, TWO_PI);  // 当前角度
    float h = min(sSpec[(int)map(i, 0, res, 0, bands-1)] * sAmp, rBase * 0.6);  // 基于频谱数据的高度
    fill(cols[i % res]);  // 使用预定义的颜色
    pushMatrix(); rotate(a); translate(rBase * 0.8, 0); rotate(HALF_PI);  // 定位并旋转矩形条
    rect(0, 0, TWO_PI / res * (rBase * 0.8), h);  // 绘制矩形条
    popMatrix();  // 恢复变换
  }
}

// 绘制控制界面 - 显示播放状态和进度条
void drawControl() {
  pushMatrix(); translate(0, 0, 50);  // 在Z轴上向前移动，确保显示在前面
  
  // 绘制播放/暂停按钮
  fill(0, 80, 90);
  if (player.isPlaying()) {
    rect(-15, -15, 10, 30);  // 暂停按钮
    rect(5, -15, 10, 30);
  } else {
    triangle(-15, -15, -15, 15, 15, 0);  // 播放按钮
  }
  
  // 绘制进度条背景
  fill(100);
  rect(-100, 30, 200, 10);
  
  // 绘制进度条填充
  fill(0, 80, 90);
  rect(-100, 30, 200 * (float)player.position() / player.length(), 10);
  
  popMatrix();  // 恢复变换
}

// 鼠标按下事件处理
void mousePressed() {
  // 检测是否点击了播放/暂停按钮
  if (dist(mouseX, mouseY, width/2, height/2) < 20) {
    if (player.isPlaying()) {
      player.pause();  // 暂停播放
    } else {
      player.play();  // 开始播放
    }
  } else {
    pmX = mouseX;  // 记录鼠标位置用于拖拽旋转
    pmY = mouseY;
  }
}

// 鼠标拖拽事件处理 - 用于旋转视角
void mouseDragged() {
  aY += (mouseX - pmX) * 0.01;  // 计算水平旋转角度
  aX += (mouseY - pmY) * 0.01;  // 计算垂直旋转角度
  pmX = mouseX;  // 更新鼠标位置
  pmY = mouseY;
}

// 键盘按下事件处理
void keyPressed() {
  if (key == ' ') {  // 空格键控制播放/暂停
    if (player.isPlaying()) {
      player.pause();
    } else {
      player.play();
    }
  } else if (key == '+') {  // 加号键放大
    scl *= 1.1;
  } else if (key == '-') {  // 减号键缩小
    scl /= 1.1;
  } else if (keyCode == UP) {  // 方向键控制平移
    mY -= 5;
  } else if (keyCode == DOWN) {
    mY += 5;
  } else if (keyCode == LEFT) {
    mX -= 5;
  } else if (keyCode == RIGHT) {
    mX += 5;
  }
}

// 鼠标滚轮事件处理 - 控制缩放
void mouseWheel(MouseEvent e) {
  scl += e.getCount() > 0 ? -0.1 : 0.1;  // 根据滚轮方向调整缩放比例
  scl = constrain(scl, 0.5, 2);  // 限制缩放范围
}

// 程序终止时的清理工作
void stop() {
  player.close();  // 关闭音频播放器
  minim.stop();    // 停止Minim音频库
  super.stop();    // 调用父类的stop方法
}
