import tkinter as tk
from tkinter import ttk  
from tkinter import messagebox as mBox

from window import *
from network import *
from process import PROCESS_NAME


#查询新版本
def GetVersion(win, VERSION):
    url = "https://github.com/lingliqianxun/game-buyhouse/blob/master/version.txt?raw=true"
    s,r = HttpFile(url)
    if s==200:
        version_new = float(r.decode('utf-8'))
        if VERSION < version_new :      
            answer = mBox.askyesno("版本提示", "有新版本发布！是否更新？")   
            if answer == True:
                toplevel_down = tk.Toplevel(win)
                toplevel_down.title("下载提示")
                WindowSizeCenter(toplevel_down, 220, 120)
                toplevel_down.grab_set()
                toplevel_down.focus()
    
                ttk.Label(toplevel_down, text="下载中，请耐心等待...", width=25, anchor=tk.CENTER).grid(column=0, columnspan=2, row=0, padx=20, pady=40)
                url = "https://github.com/lingliqianxun/game-buyhouse/blob/master/dist/buyhouse.exe?raw=true"
                s,r = HttpFile(url)
                if s==200:
                    file_name = PROCESS_NAME + "_" + str(version_new) + ".exe"
                    try:
                        f = open(file_name,'bw')
                        f.write(r)
                        f.close()
                    except:
                        toplevel_down.destroy()
                        mBox.showinfo('下载提示', '下载失败！请检查文件权限...', parent=win)
                        return
                    toplevel_down.destroy()
                    mBox.showinfo('下载提示', '下载成功！请重新打开游戏%s'%file_name, parent=win)
                else:
                    toplevel_down.destroy()
                    mBox.showwarning('下载提示', '下载失败！请检查网络...', parent=win) 
            else:  
                pass
