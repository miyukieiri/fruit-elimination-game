#!/bin/bash

echo "开始本地打包测试..."

# 检查是否安装了pyinstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "正在安装pyinstaller..."
    pip install pyinstaller
fi

# 清理之前的构建文件
rm -rf build dist *.spec

echo "正在使用pyinstaller打包..."

# 基本打包命令
pyinstaller --onefile --windowed \
    --add-data "*.png:." \
    --name "砖了个砖" \
    "砖了个砖.py"

if [ $? -eq 0 ]; then
    echo "✅ 打包成功！"
    echo "可执行文件位于: dist/砖了个砖"
    echo "文件大小: $(du -h dist/砖了个砖 | cut -f1)"
else
    echo "❌ 打包失败"
    exit 1
fi

echo "测试完成！"