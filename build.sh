#!/bin/bash

# 一键打包脚本 - macOS/Linux版本

echo "正在安装PyInstaller..."
pip install pyinstaller

echo "正在打包应用..."
pyinstaller --onefile --windowed --name="砖了个砖" 砖了个砖.py

echo "打包完成！"
echo "可执行文件位置: dist/砖了个砖"

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "在macOS上，您可以运行: ./dist/砖了个砖"
    echo "或者双击dist目录下的应用文件"
else
    echo "在Linux上，您可以运行: ./dist/砖了个砖"
fi