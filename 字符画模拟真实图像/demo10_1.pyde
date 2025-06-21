def setup():
  global img, string  # 全局变量
  img = loadImage("eason.jpg")  # 导入图片文件
  size(673, 718)  # 画面大小
  myFont = createFont("simsun.ttc", 13)  # 导入宋体，设置字体大小
  textFont(myFont)  # 设置文字字体
  textAlign(CENTER)  # 文字居中对齐
  # 从文本文件加载字符串
  lines = loadStrings("song.txt")  # 假设文件名为 poem.txt
  string = ''.join(lines)  # 将文件所有行合并为一个字符串

def draw():
  background(255)  # 白色背景
  stringId = 0  # string中要显示的字符序号
  step = int(map(mouseX, 0, width, 5, 20))  # 鼠标左右位置设置文字大小
  space = map(mouseY, 0, height, 0, step/2)  # 鼠标上下位置设置文字行间距离
  y = 0  # y坐标从0开始
  while y <= height:  # 当y坐标不超过height时循环
    x = space * noise(100 + 0.1 * y)  # 每一行x坐标从随机位置开始
    while x <= width:  # 当x坐标不超过width时循环
      yNoise = noise(0.1 * x, 0.1 * y) * space * 2  # y坐标加一些随机扰动
      c = img.get(int(x), int(y + yNoise))  # 获得这个采样点的颜色
      fill(c)  # 设置文字颜色
      bright = brightness(c)  # 当前像素的亮度值
      ts = map(bright, 0, 255, step * 1.5, step * 0.5)  # 越暗文字越大
      textSize(ts)  # 设置文字大小
      letter = string[stringId]  # 取对应序号的文字
      text(letter, x, y + yNoise)  # 在对应位置上显示文字
      stringId += 1  # 对应字符序号加1
      if stringId > len(string) - 1:  # 字符序号超出范围
        stringId = 0  # 重新设为0
        # 每次字符串结束后空随机大小
        x += 2 * space * noise(100 + 0.1 * x, 100 + 0.1 * y)
      # x坐标向右，跨过文字宽度，有一定随机性
      x += textWidth(letter) + 0.5 * space * noise(0.1 * x, 0.1 * y)
    y += step + space  # 一行处理好后，y坐标增加
