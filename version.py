import time
import os

import tkinter as tk
from tkinter import ttk  
from tkinter import messagebox as mBox

from window import *
from network import *


#全局变量
Win = None
file_name = None
toplevel_down = None
canvas_status = None
canvas_rectangle = None
label_total = None
label_speed = None
start_time = None
run_flag = False


#关闭退出并自动启动新版本
def Close(event):
    global Win,Win,run_flag

    #不判断会多次重复执行
    if run_flag == False:
        run_flag = True
        
        os.system("start \"\" \"%s\"" % file_name)

    if toplevel_down:
        toplevel_down.destroy()
    Win.destroy()


'''
 urllib.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''
def Schedule(blocknum, blocksize, totalsize):
    global file_name,toplevel_down,canvas_status,label_total,label_speed
    
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = "下载速度：%.2f" % speed
    speed_str = " 下载速度：%s" % format_size(speed)
    recv_size = blocknum * blocksize
     
    # 设置下载进度条
    pervent = recv_size / totalsize
    pervent = pervent * 100
    if pervent >= 100:
        pervent = 100

    percent_str = "%.2f%%" % (pervent)

    label_total.config(text=percent_str)
    label_speed.config(text=speed_str)
    canvas_status.delete(canvas_rectangle)
    ccanvas_rectangle = canvas_status.create_rectangle(0, 0, pervent*2, 15, outline='red', fill="red")
    toplevel_down.update()
 
# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fGb/s" % (G)
        else:
            return "%.2fMb/s" % (M)
    else:
        return "%.2fKb/s" % (kb)

#查询新版本
def GetVersion(win, is_show, process_name, icon_name, version_cur, check_url, down_url):
    global Win,file_name,toplevel_down,canvas_status,canvas_rectangle,label_total,label_speed,start_time
    Win = win
    s,r = HttpFile(check_url)
    #s,r = 200,b'2.0'
    if s != 200:
        if is_show:
            mBox.showwarning("网络提示", "连接失败，请检查网络！")
        return
    
    version_new = float(r.decode('utf-8')) 
    if version_cur >= version_new:
        if is_show:
            mBox.showinfo("版本提示", "已是最新版！")
        return
    
    file_name = process_name + "_" + str(version_new) + ".exe"
    if os.path.exists(file_name):
        answer = mBox.askyesno("版本提示", "本地有新版本v%s存在！是否打开？" % version_new)   
        if answer == True:
            Close("")
            return
        else:
            return
        
    answer = mBox.askyesno("版本提示", "有新版本v%s发布！是否更新？" % version_new)   
    if answer == False:
        return
    
    toplevel_down = tk.Toplevel(win)
    toplevel_down.title("下载提示")
    WindowSizeCenter(toplevel_down, 350, 200)
    toplevel_down.iconbitmap(WindowResourcePath(icon_name))
    toplevel_down.grab_set()
    toplevel_down.focus()

    ttk.Label(toplevel_down, text="进度：", anchor=tk.E).grid(column=0, row=0, padx=20, pady=40, stick='E')
                
    canvas_status = tk.Canvas(toplevel_down, bg='white', width=200, height=15)
    canvas_rectangle = canvas_status.create_rectangle(0, 0, 0, 15, outline='red', fill="red")
    canvas_status.grid(column=1, row=0, padx=0, pady=40, stick='W')
                
    label_total = ttk.Label(toplevel_down, text="0.00%", anchor=tk.E)
    label_total.grid(column=2, row=0, padx=0, pady=40)

    label_speed = ttk.Label(toplevel_down, text="下载速度：0.00Kb/s", anchor=tk.CENTER)
    label_speed.grid(column=0, columnspan=2, row=1, padx=0, pady=0, sticky=tk.N+tk.S)
                                    
    start_time = time.time()
    try:
        path,header = HttpDownload(down_url, file_name, Schedule)
        label_speed.config(text="下载完成，请打开【%s】" % file_name)
        toplevel_down.bind('<Destroy>',Close)
        ttk.Button(toplevel_down,text="打开新版本", command=lambda:Close("")).grid(column=1, row=2, sticky=tk.N+tk.S, padx=0, pady=20)
    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
                
