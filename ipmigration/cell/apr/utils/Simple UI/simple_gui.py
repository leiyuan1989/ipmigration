# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 16:49:53 2024

@author: leiyuan
"""



import os

from tkinter import *
from tkinter import ttk
from tkinter import filedialog


data = [
        ['Tech Name','c153'], 
        ['Netlist', 'example/c153_sl.cdl'],
        ['Cfg Dir','example/ascell'],
        ['Save Dir','output/test'],
        ['Tech Align','data/tech_align.csv'],
        ['Pin Align','data/pin_align.csv'],
       ]




class App:
    def __init__(self):
        pass
    
    
    def run(self, data):
        log_path = 'log.txt'
        
        def start_progress():
            text_box.delete(1.0, END)
            root.update_idletasks()
            # self.ascell(args,app=self)
            
            
            
            progress['value'] = 0
            max_value = 100
            step = 10
        
        
                
            for i in range(0, max_value, step):
                progress['value'] += step
                root.update_idletasks()
                root.after(1000)  # 模拟一些处理时间
        
            #finished
        
            
            with open(log_path, 'r', encoding='utf-8') as file:
                # 清空文本框内容
                text_box.delete(1.0, END)
                # 读取文件内容并插入到文本框
                content = file.read()
                text_box.insert(END, content)    
            
        
        
        
        def view_layout():
            
            #layout
            klayout_exe = 'C://Users//leiyuan//AppData//Roaming//KLayout//klayout_app.exe'
            save_dir = 'output/test/Jul_18_c153/'
            cmd = klayout_exe + ' -s ' + save_dir+'top.gds' + ' -l ' + save_dir+'kl_c153.lyp'
            os.system(cmd)
        
        def open_file():
            # 打开文件对话框，让用户选择文件
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
         
            if file_path:  # 如果用户选择了文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    # 清空文本框内容
                    text_box.delete(1.0, tk.END)
                    # 读取文件内容并插入到文本框
                    content = file.read()
                    text_box.insert(tk.END, content)    
        
        
        def select_file(entry):
            # 打开文件对话框，让用户选择文件
            file_path = filedialog.askopenfilename()
        
            if file_path:  # 如果用户选择了文件
                # text = StringVar(value='1234')
                print(file_path)
                entry.delete(0,END)
                entry.insert(0,file_path)
        
        
        
        root = Tk()
        self.root = root
        
        root.title("ASTRI Standard Cell Tool")
        W = 700
        H = 360
         
        # root.resizable(False, False) 
        root.geometry('{}x{}+200+200'.format(W, H))
        
        x = [10,80,280]
        y_space = 50
        y = 20
        
        
        
        #1
        d = data[0]
        L1 = Label(root, text=d[0])
        L1.place(x=x[0],y=y)
        
        text = StringVar(value=d[1])
        E1 = Entry(root, bd =5, width= 30,  textvariable=text)
        E1.place(x=x[1],y=y)
        
        # B1 = Button(root, text="select", command=lambda: select_file(E1))
        # B1.place(x=x[2],y=y)
        
        y = y + y_space
        
        #1
        d = data[1]
        L2 = Label(root, text=d[0])
        L2.place(x=x[0],y=y)
        
        text = StringVar(value=d[1])
        E2 = Entry(root, bd =5, width= 30,  textvariable=text)
        E2.place(x=x[1],y=y)
        
        B2 = Button(root, text="select", command=lambda: select_file(E2))
        B2.place(x=x[2],y=y)
        
        y = y + y_space
        
        #1
        d = data[2]
        L3 = Label(root, text=d[0])
        L3.place(x=x[0],y=y)
        
        text = StringVar(value=d[1])
        E3 = Entry(root, bd =5, width= 30,  textvariable=text)
        E3.place(x=x[1],y=y)
        
        B3 = Button(root, text="select", command=lambda: select_file(E3))
        B3.place(x=x[2],y=y)
        
        y = y + y_space
        
        #1
        d = data[3]
        L4 = Label(root, text=d[0])
        L4.place(x=x[0],y=y)
        
        text = StringVar(value=d[1])
        E4 = Entry(root, bd =5, width= 30,  textvariable=text)
        E4.place(x=x[1],y=y)
        
        B4 = Button(root, text="select", command=lambda: select_file(E4))
        B4.place(x=x[2],y=y)
        
        y = y + y_space
        
        #1
        d = data[4]
        L5 = Label(root, text=d[0])
        L5.place(x=x[0],y=y)
        
        text = StringVar(value=d[1])
        E5 = Entry(root, bd =5, width= 30,  textvariable=text)
        E5.place(x=x[1],y=y)
        
        B5 = Button(root, text="select", command=lambda: select_file(E5))
        B5.place(x=x[2],y=y)
        
        y = y + y_space
        
        #1
        d = data[5]
        L6 = Label(root, text=d[0])
        L6.place(x=x[0],y=y)
        
        text = StringVar(value=d[1])
        E6 = Entry(root, bd =5, width= 30,  textvariable=text)
        E6.place(x=x[1],y=y)
        
        B6 = Button(root, text="select", command=lambda: select_file(E6))
        B6.place(x=x[2],y=y)
        
        y = y + y_space
        
        
        
        
        
        LC1 = Label(root, text='Routing Style:')
        LC1.place(x=340,y=20)
        
        #check box
        CheckVar1 = IntVar(value=1)
        C1 = Checkbutton(root, text = "Only M1", variable = CheckVar1, \
                         onvalue = 1, offvalue = 0)
        C1.place(x=440,y=20)
        
        CheckVar2 = IntVar()
        C2 = Checkbutton(root, text = "M1 and M2", variable = CheckVar2, \
                         onvalue = 1, offvalue = 0,state=DISABLED)
        C2.place(x=440,y=40)
        
        CheckVar3 = IntVar()
        C3 = Checkbutton(root, text = "Ploy for clock signal", variable = CheckVar3, \
                         onvalue = 1, offvalue = 0,state=DISABLED)
        C3.place(x=440,y=60)
        
        
        
        
        # 创建一个按钮，点击后开始进度
        start_button = Button(root, text="Generate Layout", command=start_progress)
        start_button.place(x=10, y=y)
        # 创建一个进度条
        progress = ttk.Progressbar(root, orient="horizontal", length=280, mode="determinate")
        progress.place(x=120, y=y+2)
        self.progress = progress
        
        
        from PIL import ImageTk, Image
        #insert logo
        img = Image.open("logo.png").resize((140, 20))
        photo = ImageTk.PhotoImage(img)
        Label(root, image=photo, bd=10).place(x=530,y=y-5)
         
         
         
        #text
        text_box = Text(root, wrap=WORD)
        text_box.place(x=340,y=100,width=320,height=200)
         
        self.text_box = text_box
        
        
        view_button = Button(root, text="View Layout", command=view_layout)
        view_button.place(x=450, y=y)
        
        root.mainloop()
        
        # label= Label(frame1,text="Label1",justify=LEFT)
        # label.pack(side=LEFT)
        
        # # 创建一个按钮用于打开文件
        # btn_open = Button(frame1, text="选择TXT文件", command=open_file)
        # btn_open.pack(side=LEFT)
        
        
#
app = App()
app.run(data)
