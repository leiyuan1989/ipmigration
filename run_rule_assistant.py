import re
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from ollama import Client
from ipmigration.rule.svrf_reader import RuleFile


logo_path = "ipmigration/rule/rs/astri-2024-6.webp"

host = 'http://10.6.126.115:11434'
model = 'deepseek-r1:32b'

chat_dict_file = 'ipmigration/rule'

client = Client(host)


#fc.json
#pre_load.json
#



class InterfaceApp:
    def __init__(self, root, client, model):
        self.root = root
        self.client = client
        self.model = model

        self.root.title("半导体工艺文件提取工具")
        self.root.geometry("1200x600")
        
        self.drc_path='No file selected'
        self.drc_path='demo/rule/decks/c153.rul'
        self.layer_def_path = 'No file selected'
        self.layer_def_path = 'demo/rule/decks/c153_ldef.csv'  
        
        self.save_dir = './demo/rule/output'
        self.host = host
        self.dr_files = []
        self.load_files = []
        
        self.init_message()  # TODO: add out path
        self.create_top_frame()
        self.create_content_frame()
    
        self.check_folder()

    def init_message(self):
        self.messages = [
            {"role": "system", "content": "你是一个半导体工艺专家"},
            {"role": "assistant", "content": "你好，我是半导体设计规则提取大模型助手。我将基于半导体制造工艺知识，为您提供设计规则提取的专业支持。"},
            {"role": "assistant", "content": "如需开始提取半导体工艺，请完成相关工具设置并输入:START"}
        ]

    def create_top_frame(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # logo 区域
        logo_frame = tk.Frame(top_frame)
        logo_frame.pack(side=tk.LEFT)
        try:
            logo_image = Image.open("ipmigration/rule/rs/astri-2024-6.jpg")
            logo_image = logo_image.resize((300, 50))
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(logo_frame, image=logo_photo)
            logo_label.image = logo_photo
            logo_label.pack(side=tk.LEFT)
        except FileNotFoundError:
            logo_label = tk.Label(logo_frame, text="Logo Placeholder")
            logo_label.pack(side=tk.LEFT)

        # 文件读取按钮与文件地址显示区域
        file_frame = tk.Frame(top_frame)
        file_frame.pack(side=tk.RIGHT)

        # 使用 grid 布局排列按钮和输入框
        open_button0 = tk.Button(file_frame, text="%30s"%("Input Tech Name"))
        open_button0.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        open_button0.config(state=tk.DISABLED)
        self.file_entry0 = tk.Entry(file_frame, width=80)
        self.file_entry0.insert(0, 'tech name')
        self.file_entry0.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        
        open_button1 = tk.Button(file_frame, text="%30s"%("Load DRC Deck"), command=self.open_file1)
        open_button1.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.file_entry1 = tk.Entry(file_frame, width=80)
        self.file_entry1.insert(0, self.drc_path)
        self.file_entry1.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        open_button2 = tk.Button(file_frame, text="%30s"%("Load Layer Definition"), command=self.open_file2)
        open_button2.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.file_entry2 = tk.Entry(file_frame, width=80)
        self.file_entry2.insert(0, self.layer_def_path)
        self.file_entry2.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    def open_file1(self):
        # print(self.file_entry1.get())
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry1.delete(0, tk.END)
            self.file_entry1.insert(0, file_path)
            
            

    def open_file2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry2.delete(0, tk.END)
            self.file_entry2.insert(0, file_path)

    def create_content_frame(self):
        content_frame = tk.Frame(self.root)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧部分
        left_frame = tk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 对话记录
        self.chat_history = tk.Text(left_frame, height=20, width=40)
        self.chat_history.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.init_chat_history()
        # 输入框和按钮
        input_frame = tk.Frame(left_frame)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.entry = tk.Entry(input_frame, width=30)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        send_button = tk.Button(input_frame, text="发送", command=self.send_message)
        send_button.pack(side=tk.RIGHT)

        clear_button = tk.Button(input_frame, text="Clear", command=self.clear_chat)
        clear_button.pack(side=tk.RIGHT, padx=5)

        # 右侧部分
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # 表格
        columns = ('layer','layer_def','dr','category','description','symbol','value')
        columns_width = [50,50,50,50,300,50,50]
        
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings')
        style = ttk.Style()
        style.configure("Treeview", rowheight=50)  # 设置行高以容纳多行文本
        
        for col,col_w in zip(columns,columns_width):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_w, stretch=True)  # 设置列宽并允许拉伸

        # 创建横向滚动条
        x_scrollbar = ttk.Scrollbar(right_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=x_scrollbar.set)

        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 预设数据
        data = [
            # ('DR001', 'Minimum Metal1 Line Width', 'Metal1', 'Minimum', 'Minimum width for Metal1 layer lines', '≥',
            #  '0.18μm')
        ]

        for item in data:
            self.tree.insert('', tk.END, values=item)

        # Save as 按钮
        save_button = tk.Button(right_frame, text="Save as", command=self.save_table)
        save_button.pack(side=tk.BOTTOM, pady=10)

    def init_chat_history(self):
        for msg in self.messages:
            role = msg['role']
            content = msg['content']
            if role == 'user':
                self.chat_history.insert(tk.END, f"\nYou: {content}\n")
            if role == 'assistant':
                self.chat_history.insert(tk.END, f"\nBOT: {content}\n")
            

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            #calling
            if message.strip() == 'START':

                answer = '开始提取'
                self.messages.append({"role": "assistant", "content": answer})
                self.chat_history.insert(tk.END, f"\nBOT: {answer}\n")
                self.entry.delete(0, tk.END)
                
                tech_name =  self.file_entry0.get()
                drc_deck = self.file_entry1.get()
                layer_def = self.file_entry2.get()
                # try:
                self.read_drc_deck(tech_name,drc_deck,layer_def)
                # except:
                #     content = '提取错误，请检查输入文件并出现输入 START'
                #     self.chat_history.insert(tk.END, f"\nBOT: {content}\n")
    
            
            else:
            
                self.chat_history.insert(tk.END, f"\nYou: {message}\n")
                self.messages.append({"role": "user", "content": message})
                self.entry.delete(0, tk.END)
                try:
                    response = self.client.chat(self.model, self.messages)
    
                    answer = response.message.content
                    print(answer)
                    answer = self.remove_think_content(answer)
                    self.messages.append({"role": "assistant", "content": answer})
                    self.chat_history.insert(tk.END, f"\nBOT: {answer}\n")
    
                except Exception as e:
                    print(f"发生错误: {e}")

    def clear_chat(self):
        self.chat_history.delete(1.0, tk.END)

    def remove_think_content(self, text):
        # 正则表达式：匹配以 `</think>` 开头，到第一个 `\n\n` 之间的内容（包括换行）
        pattern = r'<think>.*?</think>'
        # re.DOTALL 标志让点号匹配所有字符（包括换行），re.MULTILINE 处理多行模式（可选，视情况）
        cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
        lines = cleaned_text.splitlines()  #
        non_empty_lines = [line for line in lines if (line.strip())]
        return '\n'.join(non_empty_lines)

    def save_table(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                columns = self.tree["columns"]
                file.write(','.join(columns) + '\n')
                for item in self.tree.get_children():
                    values = self.tree.item(item, "values")
                    file.write(','.join(map(str, values)) + '\n')

    def read_drc_deck(self,tech_name,drc_deck,layer_def):
        rf = RuleFile(tech_name, 
                      drc_deck, 
                      layer_def, 
                      self.host,
                      self.save_dir, 
                      '', 
                      'INFO')
        for layer in rf.layers:
            self.dr_files.append(os.path.join(self.save_dir, tech_name + '_' + layer + '.csv'))
        rf.extract_rules()
        
    def check_folder(self):

        # try:
        new_files = []
        for file in self.dr_files:
            if os.path.exists(file):
                if not(file in self.load_files):
                    new_files.append(file)
                    self.load_files.append(file)
        
        for file in new_files:
            print(file)
            file_name = os.path.basename(file)[:-4]
            answer = "已完成 %s 的提取。"%(file_name)
            self.chat_history.insert(tk.END, f"\nBOT: {answer}\n")
            self.messages.append({"role": "assistant", "content": answer})


            df = pd.read_csv(file)
            content = "内容是如下设计规则表格：\n" + df.to_csv(sep=',')
            self.messages.append({"role": "assistant", "content": content})
            for i,r in df.iterrows():
                self.tree.insert('', tk.END, values=r.tolist())
            # self.tree.insert('', 'end', values=(file, file_size, modified_time))

            # # 更新 Text 控件
            # info = f"发现新文件: {file}, 大小: {file_size} 字节, 修改时间: {modified_time}\n"
            # self.text.insert(tk.END, info)

        # except Exception as e:
        #     error_info = f"检查文件夹时出错: {e}\n"
        #     self.text.insert(tk.END, error_info)

        # 每隔 5 秒检查一次
        self.root.after(5000, self.check_folder)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceApp(root, client, model)
    root.mainloop()
    