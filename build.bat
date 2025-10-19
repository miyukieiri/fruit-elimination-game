@echo off
echo 正在安装PyInstaller...
pip install pyinstaller

echo 正在打包应用...
pyinstaller --onefile --windowed --name="砖了个砖" 砖了个砖.py

echo 打包完成！
echo 可执行文件位置: dist\砖了个砖.exe
echo 您可以双击运行或通过命令行运行: dist\砖了个砖.exe

pause