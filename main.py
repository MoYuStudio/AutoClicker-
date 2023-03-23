
# === MoYuToolBox 摸鱼工具箱 ===
#   Develop BY WilsonVinson      

import sys
import datetime
import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font

from PIL import Image, ImageTk
from ttkbootstrap import Style
import screeninfo

import module.json_driver as json_driver
import module.recorder as recorder
import module.executor as executor

def start_recording(recorder_obj, status_label_var):
    recorder_obj.recording = True
    recorder_obj.events.clear()
    recorder_obj.start_time = datetime.datetime.now()
    status_label_var.set('记录中')

def stop_recording(recorder_obj, status_label_var, file_name_entry):
    recorder_obj.recording = False
    file_name = file_name_entry.get()
    if not file_name:
        file_name = 'user'
    data = {'input_event': recorder_obj.events}
    json_driver.json_write(f'data/{file_name}.json', data)
    status_label_var.set('就绪')

def start_execution(status_label_var):
    file_name = file_name_entry.get()
    if not file_name:
        file_name = 'user'
    data = json_driver.json_read(f'data/{file_name}.json')
    loop_count = loop_var.get()
    executor_obj = executor.Executor(data, loop_count)
    threading2 = threading.Thread(target=executor_obj.run)
    threading2.start()
    status_label_var.set('执行中')

def clear_records(recorder_obj):
    recorder_obj.events.clear()
    
def on_closing():
    root.destroy()

if __name__ == '__main__':
    
    recorder_obj = recorder.Recorder()
    threading1 = threading.Thread(target=recorder_obj.run)
    threading1.start()
    
    # root = tk.Tk()
    style = Style(theme='darkly')# python -m ttkbootstrap
    root = style.master
    
    notebook = ttk.Notebook(root)
    
    page1 = tk.Frame(notebook)
    page2 = tk.Frame(notebook)
    page3 = tk.Frame(notebook)
    page4 = tk.Frame(notebook)
    page5 = tk.Frame(notebook)
    page6 = tk.Frame(notebook)
    
    custom_font_0 = font.Font(family='黑体', size=12)#, weight='bold'
    custom_font_1 = font.Font(family='黑体', size=9)
    custom_font_2 = font.Font(family='黑体', size=24)
    
    root.title('MoYu ToolBox 摸鱼工具箱')
    root.iconbitmap("icon.ico")
    root.geometry("600x600")
    # root.resizable(False, False)
    root.configure(bg='#F0F0F0')
    root.attributes("-alpha", 0.95)
    
    notebook.add(page1, text="主页")
    notebook.add(page2, text="点击器")
    notebook.add(page6, text="关于")
    notebook.place(x=0, y=0)
    
    monitors = screeninfo.get_monitors()
    
    image_file = Image.open("icon_x500.png")
    tk_image = ImageTk.PhotoImage(image_file)
    icon_label = tk.Label(page6, image=tk_image)
    icon_label.place(x=5, y=5)
    icon_label.config(bg=page6['bg'])
    
    title_label = Label(page6, text='MoYu ToolBox', font=custom_font_2)
    title_label.place(x=95, y=200)
    title_label.config(bg=page6['bg'])
    
    copyright_label = Label(page6, text='Power BY ChatGPT   Develop BY WilsonVinson', font=custom_font_1)
    copyright_label.place(x=100, y=560)
    copyright_label.config(bg=page6['bg'])
    
    monitor_var = IntVar(value=0)
    monitor_spinbox = Spinbox(page2, from_=0, to=len(monitors), width=1, font=custom_font_0, textvariable=monitor_var)
    monitor_spinbox.place(x=25, y=100)
    
    monitorl_abel = Label(page2, text=('屏幕分辨率 '+str(monitors[monitor_var.get()].width)+'x'+str(monitors[monitor_var.get()].height)), font=custom_font_0)
    monitorl_abel.place(x=65, y=100)
    monitorl_abel.config(bg=page2['bg'])
    
    status_label_var = StringVar()
    status_label_var.set('就绪')
    status_label = Label(page2, textvariable=status_label_var, bd=1, relief=SUNKEN, anchor=W, font=custom_font_0)
    status_label.place(x=500, y=100)
    
    file_name_label = Label(page2, text='输入文件名(默认user):', font=custom_font_0)
    file_name_label.place(x=25, y=150)
    file_name_label.config(bg=page2['bg'])
    
    file_name_entry = Entry(page2, width=24)
    file_name_entry.place(x=300, y=150)

    record_button = Button(page2, text='开始记录',width=15, height=2, font=custom_font_0, command=lambda: start_recording(recorder_obj, status_label_var))
    record_button.place(x=25, y=200)

    stop_button = Button(page2, text='结束记录',width=15, height=2, font=custom_font_0, command=lambda: stop_recording(recorder_obj, status_label_var, file_name_entry))
    stop_button.place(x=300, y=200)
    
    loop_label = Label(page2, text='循环次数(-1无限循环):', font=custom_font_0)
    loop_label.place(x=25, y=290)
    loop_label.config(bg=page2['bg'])

    loop_var = IntVar(value=1)
    loop_spinbox = Spinbox(page2, from_=-1, to=1000, width=21, font=custom_font_0, textvariable=loop_var)
    loop_spinbox.place(x=300, y=290)

    execute_button = Button(page2, text='开始执行',width=15, height=2, font=custom_font_0, command=lambda: start_execution(status_label_var))
    execute_button.place(x=25, y=350)

    clear_button = Button(page2, text='清空记录',width=15, height=2, font=custom_font_0, command=lambda: clear_records(recorder_obj))
    clear_button.place(x=300, y=350)

    notebook.pack(expand=True, fill="both")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

    sys.exit(0)
