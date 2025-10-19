# 使用Windows容器基础镜像
FROM python:3.9-windowsservercore

# 设置工作目录
WORKDIR /app

# 复制Python文件
COPY 砖了个砖.py .
COPY fruit*.png . 
COPY button.png .

# 安装依赖
RUN pip install pyinstaller numpy tkinter

# 打包成exe
RUN pyinstaller --onefile --windowed --name="砖了个砖" 砖了个砖.py

# 输出文件会在dist目录下