'''
Fuction：客户端发送图片和数据
Date：2018.9.8
Author：snowking
'''
###客户端client.py
import socket
import os
import sys
import struct
import wave

import keyboard
import pyaudio


def play():
    p = pyaudio.PyAudio()  # 实例化
    wf = wave.open('c.wav', 'rb')  # 读 wav 文件
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)  # 读数据
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()  # 关闭资源
    stream.close()
    p.terminate()


def save_audio():
    try:
        """ 录音功能 """
        CHUNK = 1024  # 每个缓冲区的帧数
        FORMAT = pyaudio.paInt16  # 采样位数
        CHANNELS = 1  # 单声道
        RATE = 16000  # 采样频率
        p = pyaudio.PyAudio()  # 实例化对象
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  # 打开流，传入响应参数
        wf = wave.open('mx.wav', 'wb')  # 打开 wav 文件。
        wf.setnchannels(CHANNELS)  # 声道设置
        wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
        wf.setframerate(RATE)  # 采样频率设置

        for _ in range(0, int(RATE * 1000 / CHUNK)):
            data = stream.read(CHUNK)
            wf.writeframes(data)  # 写入数据
        stream.stop_stream()  # 关闭流
        stream.close()
        p.terminate()
        wf.close()
    except KeyboardInterrupt:
        print('close')


def sock_client_image():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.20.13.130', 9458))  # 服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
        # s.connect(('127.0.0.1', 6666))  #服务器和客户端都在一个系统下时使用的ip和端口
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))
    filepath = 'mx.wav'  # 输入当前目录下的图片名 xxx.jpg
    fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                        os.stat(filepath).st_size)  # 将xxx.jpg以128sq的格式打包
    s.send(fhead)

    fp = open(filepath, 'rb')  # 打开要传输的图片
    while True:
        data = fp.read(1024)  # 读入图片数据
        if not data:
            print('{0} send over...'.format(filepath))
            break
        s.send(data)  # 以二进制格式发送图片数据

    # -------- 接收server端发送的结果文件数据 --------
    while True:
        fileinfo_size = struct.calcsize('128sq')
        buf = s.recv(fileinfo_size)  # 接收图片名
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.decode().strip('\x00')
            new_filename = os.path.join('c.wav')

            recvd_size = 0
            fp = open(new_filename, 'wb')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = s.recv(1024)
                    recvd_size += len(data)
                else:
                    data = s.recv(1024)
                    recvd_size = filesize
                fp.write(data)  # 写入结果文件数据
            print('{} saved.'.format(new_filename))
            fp.close()
            break

    s.close()
    return
    # break    #循环发送


if __name__ == '__main__':
    save_audio()
    try:
        sock_client_image()
    except:
        print('网络连接错误')
    play()
    input("任意键继续")
