#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import tkinter

 
top = tkinter.Tk()

def helloCallBack():
   while True:
      print('a')

def test():
   while True:
      print('b')

B = tkinter.Button(top, text ="点我a", command = helloCallBack)

C = tkinter.Button(top, text ="点我b", command = test)
B.pack()
C.pack()
top.mainloop()