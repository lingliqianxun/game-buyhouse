
#窗口居中
def WindowCenter(widget):
    window_width = widget.winfo_screenwidth()
    window_height = widget.winfo_screenheight()
    width = widget.winfo_width()
    height = widget.winfo_height()
    x = (window_width/2) - (width/2)
    y = (window_height/2) - (height/2)
    widget.geometry('+%d+%d' % (x,y))
    
#窗口设置大小并居中
def WindowSizeCenter(widget, width, height):
    window_width = widget.winfo_screenwidth()
    window_height = widget.winfo_screenheight()
    x = (window_width/2) - (width/2)
    y = (window_height/2) - (height/2)
    widget.geometry('%dx%d+%d+%d' % (width,height,x,y))
