# 砖了个砖 - 水果消除游戏

## 简介
这是一个基于Python和Tkinter开发的水果消除游戏，使用A*算法求解最优路径。

## 安装和运行

### 方法1：直接运行Python脚本
确保您的系统已安装Python 3.7+和以下依赖：
```bash
pip install numpy tkinter
python 砖了个砖.py
```

### 方法2：使用PyInstaller打包

#### 在Windows上：
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="砖了个砖" 砖了个砖.py
```
生成的exe文件在`dist`目录下。

#### 在macOS上：
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="砖了个砖" 砖了个砖.py
```
生成的app文件在`dist`目录下。

#### 在Linux上：
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="砖了个砖" 砖了个砖.py
```

### 方法3：使用Docker
如果您需要在不同平台上打包，可以使用Docker：
```bash
docker build -t fruit-game .
docker run -v $(pwd)/dist:/app/dist fruit-game
```

## 游戏特性
- 支持4x4到8x8的棋盘
- 1-5种不同水果
- 随机摆放或手动摆放
- 可自定义滑动代价
- A*算法求解最优路径
- 可视化演示解题过程

## 系统要求
- Python 3.7+
- numpy
- tkinter (通常随Python一起安装)

## 注意事项
- 确保游戏目录下有水果图片文件(fruit1.png, fruit2.png等)和button.png
- 如果没有图片文件，游戏会使用默认图像