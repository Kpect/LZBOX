#coding=utf-8
#import libs 
import sys
import Project2_cmd
import Project2_sty
import Fun
import EXUIControl
import requests
import tkinter as tk
import yaml
EXUIControl.G_ExeDir = Fun.G_ExeDir
EXUIControl.G_ResDir = Fun.G_ResDir
import os
import tkinter
from   tkinter import *
import tkinter.ttk
import tkinter.font
#Add your Varial Here: (Keep This Line of comments)
#Define UI Class
def read_server_list():
    server_list = {}
    with open("room.yml", 'r', encoding='utf-8') as file:
        server_list = yaml.safe_load(file)
    return server_list

def get_server_list():
    server_list_url = "http://naruto.w1.luyouxia.net/sava/room.yml"
    response = requests.get(server_list_url)
    server_list = {}
    if response.status_code == 200:
        server_list = yaml.safe_load(response.text)
    return server_list

def show_all_servers():
    global listbox  # 将listbox声明为全局变量
    server_list = get_server_list()
    server_names = list(server_list.keys())
    if len(server_names) > 0:
        listbox.delete(0, tk.END)
        for name in server_names:
            listbox.insert(tk.END, name)
    else:
        messagebox.showinfo("服务器列表", "没有找到服务器")

def download_server():
    selected_servers = listbox.curselection()
    if len(selected_servers) == 0:
        messagebox.showerror("下载服务器", "请先选择一个服务器")
        return
    
    server_name = listbox.get(selected_servers[0])
    server_list = get_server_list()
    if server_name in server_list:
        server_url = server_list[server_name]
        messagebox.showinfo("下载服务器", f"正在下载服务器 {server_name} 的客户端...")
        response = requests.get(server_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024*1024  # 每次读取的块大小
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取程序所在目录的绝对路径
        server_dir = os.path.join(base_dir, "server")  # 保存文件的目录
        os.makedirs(server_dir, exist_ok=True)  # 确保目录存在
        with open(os.path.join(server_dir, f"{server_name}.zip"), 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        messagebox.showinfo("下载完成", "下载完成！")
    else:
        messagebox.showerror("找不到服务器", f"找不到服务器：{server_name}")

def download_servers():
    selected_servers = listbox.curselection()
    if len(selected_servers) == 0:
        messagebox.showerror("批量下载服务器", "请先选择一个或多个服务器")
        return
    
    server_names = [listbox.get(index) for index in selected_servers]
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures_to_server_names = {}
        for server_name in server_names:
            futures = executor.submit(download_server, server_name)
            futures_to_server_names[futures] = server_name

        for future in as_completed(futures_to_server_names):
            server_name = futures_to_server_names[future]
            try:
                _ = future.result()
            except Exception as exc:
                messagebox.showerror("下载失败", f"下载服务器 {server_name} 失败: {exc}")
            else:
                messagebox.showinfo("下载成功", f"下载服务器 {server_name} 成功!")
class  Project2:
    def __init__(self,root,isTKroot = True):
        uiName = self.__class__.__name__
        self.uiName = uiName
        Fun.Register(uiName,'UIClass',self)
        self.root = root
        self.isTKroot = isTKroot
        Fun.G_UICommandDictionary[uiName]=Project2_cmd
        Fun.Register(uiName,'root',root)
        style = Project2_sty.SetupStyle()
        if isTKroot == True:
            root.title("ZLBOX")
            root.overrideredirect(True)
            Fun.WindowDraggable(root,False,0,'#00ffff')
            root.resizable(False,False)
            root.wm_attributes("-transparentcolor","#00ffff")
            Fun.CenterDlg(uiName,root,700,500)
            root.state("zoomed")
            root['background'] = '#5271ff'
        root.bind('<Configure>',self.Configure)
        Form_1= tkinter.Canvas(root,width = 10,height = 4)
        Form_1.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)
        Form_1.configure(width = 700)
        Form_1.configure(height = 500)
        Form_1.configure(bg = "#00ffff")
        Fun.SetRootRoundRectangle(Form_1,False,0,0,700,500,radius=5,fill='#5271ff',outline='#00ffff',width=0)
        Form_1.configure(highlightthickness = 0)
        Fun.Register(uiName,'Form_1',Form_1)
        Fun.G_RootSize=[700,500]
        #Create the elements of root 
        Button_5 = tkinter.Button(Form_1,text="❌")
        Fun.Register(uiName,'Button_5',Button_5,'Button_1')
        Fun.SetControlPlace(uiName,'Button_5',667,0,33,43)
        Button_5.configure(bg = "#5371ff")
        Button_5.configure(activebackground = "#95a8ff")
        Button_5.configure(relief = "flat")
        Button_5.bind("<Button-1>",Fun.EventFunction_Adaptor(Project2_cmd.Button_5_onButton1,uiName=uiName,widgetName="Button_5"))
        Button_8 = tkinter.Button(Form_1,text="搜索")
        Fun.Register(uiName,'Button_8',Button_8,'搜索')
        Fun.SetControlPlace(uiName,'Button_8',614,43,71,39)
        Button_8.configure(bg = "#a2b1ff")
        Button_8.configure(relief = "flat")
        Fun.SetRoundedRectangle(Button_8,5,5)
        Label_6 = tkinter.Label(Form_1,text="ZLBOX")
        Fun.Register(uiName,'Label_6',Label_6,'Label_1')
        Fun.SetControlPlace(uiName,'Label_6',-54,-2,200,48)
        Label_6.configure(bg = "#5371ff")
        Label_6.configure(fg = "#ffffff")
        Label_6.configure(relief = "flat")
        Label_6_Ft=tkinter.font.Font(family='Microsoft YaHei UI', size=15,weight='bold',slant='roman',underline=0,overstrike=0)
        Label_6.configure(font = Label_6_Ft)
        Entry_7= EXUIControl.CustomEntry(Form_1)
        Fun.Register(uiName,'Entry_7',Entry_7,'Entry_1')
        Entry_7.SetBGColor("#FFFFFF")
        Entry_7.SetFGColor("#000000")
        Entry_7.SetTipFGColor("#888888")
        Entry_7.SetRelief("sunken")
        Entry_7.SetRoundRadius(5)
        Fun.SetControlPlace(uiName,'Entry_7',284,46,320,34)
        #Inital all element's Data 
        Fun.InitElementData(uiName)
        #Add Some Logic Code Here: (Keep This Line of comments)
        #Exit Application: (Keep This Line of comments)
        if self.isTKroot == True and Fun.GetElement(self.uiName,"root"):
            self.root.protocol('WM_DELETE_WINDOW', self.Exit)
            self.root.bind('<Escape>',self.Escape)  
    def GetRootSize(self):
        return Fun.G_RootSize[0],Fun.G_RootSize[1]
    def GetAllElement(self):
        return Fun.G_UIElementDictionary[self.__class__.__name__]
    def Escape(self,event):
        if Fun.AskBox('提示','确定退出程序？') == True:
            self.Exit()
    def Exit(self):
        if self.isTKroot == True:
            Fun.DestroyUI(self.uiName)

    def Configure(self,event):
        Form_1 = Fun.GetElement(self.uiName,'Form_1')
        if Form_1 == event.widget:
            Fun.ReDrawCanvasRecord(self.uiName)
        if self.root == event.widget:
            Fun.G_RootSize=[event.width,event.height]
            uiName = self.uiName
            Fun.SetControlPlace(uiName,'Label_6',-54,-2,200,48)
            pass
#Create the root of Kinter 
if  __name__ == '__main__':
    root = tkinter.Tk()
    MyDlg = Project2(root)
    root.mainloop()
