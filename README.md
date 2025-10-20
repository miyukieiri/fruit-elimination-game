# 砖了个砖 - 水果消除游戏

这是一个基于Python和Tkinter开发的水果消除游戏，使用A*算法自动求解最优路径。

## 功能特点

- 支持4x4到8x8不同大小的棋盘
- 1-5种不同类型的水果
- 随机摆放或手动摆放模式
- 自定义每种水果的移动代价
- A*算法自动求解最优路径
- 路径可视化演示功能

## 运行要求

- Python 3.7+
- tkinter (通常随Python安装)
- numpy
- PIL/Pillow

## 安装运行

1. 克隆仓库：
```bash
git clone https://github.com/miyukieiri/fruit-elimination-game.git
cd fruit-elimination-game
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行游戏：
```bash
python 砖了个砖.py
```

## 下载可执行文件

你可以在[Releases页面](https://github.com/miyukieiri/fruit-elimination-game/releases)下载Windows可执行文件，无需安装Python即可运行。

## 游戏规则

1. 每种水果在棋盘上有两个
2. 将相同的水果移动到同一行或同一列
3. 当两个相同水果在同一行/列且中间所有格子的数值总和等于该水果数值的2倍时，水果会自动消除
4. 目标是消除所有水果

## 算法说明

使用A*搜索算法自动寻找最优解路径，启发函数考虑了：
- 相同水果之间的曼哈顿距离
- 每种水果的移动代价
- 当前路径的累计代价

## 许可证

MIT License