import os
import socket
import struct
import wave
from tkinter import *

import threading
import time

import pyaudio


class GUI():

    def __init__(self, root):
        self.initGUI(root)

    def initGUI(self, root):
        root.title("语音对话")
        root.geometry("400x200+700+500")
        root.resizable = False

        label = Label(root, text='点击“开始录音”后你有大约五秒讲话时间')  # text为显示的文本内容
        label.pack()
        self.button_1 = Button(root, text="开始录音", width=10, command=self.A)
        self.button_1.pack(side="top")

        #self.button_2 = Button(root, text="结束录音", width=10, command=self.B)
        #self.button_2.pack(side="top")

        #self.button_2 = Button(root, text="run C", width=10, command=self.C)
        #self.button_2.pack(side="top")

        root.mainloop()

    def __A(self):
        try:
            CHUNK = 1024  # 每个缓冲区的帧数
            FORMAT = pyaudio.paInt16  # 采样位数
            CHANNELS = 1  # 单声道
            RATE = 16000
            a = 100
            b = 0
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
            wf = wave.open('mx.wav', 'wb')
            """ 录音功能 """
            wf.setnchannels(CHANNELS)  # 声道设置
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            for _ in range(0, int(RATE * 5 / CHUNK)):
                b=_
                data = stream.read(CHUNK)
                wf.writeframes(data)
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()
        except :
            print('close')

        try:
            self.sock_client_image()
        except:
            print('网络连接错误')

        self.play()
        time.sleep(3)


    def A(self):
        T = threading.Thread(target=self.__A)
        #TT=threading.Thread(target=self.__D)
        T.start()
        #TT.start()

    def __D(self):
        while True:
            a=1
    def __B(self):

        try:
            self.sock_client_image()
        except:
            print('网络连接错误')

        self.play()
        time.sleep(3)
    def play(self):
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




    def sock_client_image(self):
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

    def B(self):
        T = threading.Thread(target=self.__B)
        T.start()

    def __C(self):
        print("start to run proc C")

        # time.sleep(3)
        # print("proc C finished")


    def C(self):
        T = threading.Thread(target=self.__C)
        T.start()


if __name__ == "__main__":
    root = Tk()
    myGUI = GUI(root)
