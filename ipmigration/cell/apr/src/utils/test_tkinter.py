

from tkinter import *
from PIL import ImageTk, Image
 
W = 300
H = 150
 
root = Tk()
root.resizable(False, False)
root.title('显示图片')
 
root.geometry('{}x{}+200+200'.format(W, H))
# 打开图片        图片路径+后缀   更改图片大小
img = Image.open("logo.png").resize((W, H))
 
# 加载图片
photo = ImageTk.PhotoImage(img)
 
 
Label(root, image=photo, bd=10).pack()
 
 
mainloop()



import tkinter as tk
from tkinter import ttk


def start_progress():
    progress['value'] = 0
    max_value = 100
    step = 10

    for i in range(0, max_value, step):
        progress['value'] += step
        root.update_idletasks()
        root.after(500)  # 模拟一些处理时间


root = tk.Tk()
root.title("进度条示例")

# 创建一个进度条
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20)

# 创建一个按钮，点击后开始进度
start_button = tk.Button(root, text="开始", command=start_progress)
start_button.pack(pady=10)

root.mainloop()




import tkinter as tk
from tkinter import filedialog
 
def open_file():
    # 弹出文件选择对话框并获取用户选择的文件路径
    file_path = filedialog.askopenfilename()
    if file_path:
        print("Selected file:", file_path)
 
def save_file():
    # 弹出文件保存对话框并获取用户选择的保存路径
    file_path = filedialog.asksaveasfilename()
    if file_path:
        print("Selected save path:", file_path)
 
def open_multiple_files():
    # 弹出文件选择对话框并获取用户选择的多个文件路径
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        print("Selected files:", file_paths)
 
def choose_directory():
    # 弹出目录选择对话框并获取用户选择的目录路径
    directory_path = filedialog.askdirectory()
    if directory_path:
        print("Selected directory:", directory_path)
 
# 创建主窗口
root = tk.Tk()
root.title("File Dialog Example")
 
# 创建框架以容纳按钮，并设置左对齐
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, anchor="w")
 
# 创建按钮并绑定事件，每个按钮调用相应的函数
btn_open_file = tk.Button(frame, text="Open File", command=open_file, width=20)
btn_open_file.pack(pady=5, anchor="w")
 
btn_save_file = tk.Button(frame, text="Save File", command=save_file, width=20)
btn_save_file.pack(pady=5, anchor="w")
 
btn_open_multiple_files = tk.Button(frame, text="Open Multiple Files", command=open_multiple_files, width=20)
btn_open_multiple_files.pack(pady=5, anchor="w")
 
btn_choose_directory = tk.Button(frame, text="Choose Directory", command=choose_directory, width=20)
btn_choose_directory.pack(pady=5, anchor="w")
 
# 运行主循环，使应用程序保持运行状态
root.mainloop()




#选择文件并展示

import tkinter as tk
from tkinter import filedialog
 
 
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
 
 
# 创建主窗口
root = tk.Tk()
root.title("读取TXT文件")
 
# 创建一个按钮用于打开文件
btn_open = tk.Button(root, text="选择TXT文件", command=open_file)
btn_open.pack()
 
# 创建一个多行文本框用于显示文件内容
text_box = tk.Text(root, wrap=tk.WORD)
text_box.pack(fill=tk.BOTH, expand=1)
 
# 运行主循环
root.mainloop()



import tkinter as tk

window = tk.Tk()

frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
frame1.pack(side=tk.LEFT)

frame2 = tk.Frame(master=window, width=100, bg="yellow")
frame2.pack(fill=tk.Y, side=tk.LEFT)

frame3 = tk.Frame(master=window, width=50, bg="blue")
frame3.pack(fill=tk.Y, side=tk.LEFT)

window.mainloop()











