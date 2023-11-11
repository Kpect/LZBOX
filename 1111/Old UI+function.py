import tkinter as tk
from tkinter import messagebox
import requests
import yaml
import ctypes
import sys
import time
import urllib.request
import concurrent.futures
import tkinter.ttk as ttk
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

entry_search = None
frame_server_list = None

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

def get_notice():
    notice_url = "https://naruto.w1.luyouxia.net/G/g.yml"
    response = requests.get(notice_url)
    notice = ""
    if response.status_code == 200:
        notice = response.text
    return notice

def show_all_servers():
    global frame_server_list
    server_list = get_server_list()
    server_names = list(server_list.keys())
    if len(server_names) > 0:
        for widget in frame_server_list.winfo_children():
            widget.destroy()

        page_size = 8
        num_pages = (len(server_names) + page_size - 1) // page_size

        notebook = ttk.Notebook(frame_server_list)
        notebook.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        for page in range(num_pages):
            start_index = page * page_size
            end_index = min((page + 1) * page_size, len(server_names))
            servers_on_page = server_names[start_index:end_index]

            page_frame = tk.Frame(notebook, bg="white")
            notebook.add(page_frame, text=f"Page {page+1}")

            for name in servers_on_page:
                server_frame = tk.Frame(page_frame, bd=2, relief=tk.GROOVE, cursor="hand2", width=104, height=89)
                server_frame.pack(pady=5, padx=10, fill=tk.X)
                server_frame.bind("<Button-1>", lambda event, server_name=name: download_server(server_name))

                image_url = server_list[name]["image"]
                image_data = urllib.request.urlopen(image_url).read()
                photo = tk.PhotoImage(data=image_data)

                server_label = tk.Label(server_frame, text=name, font=("微软雅黑", 12))
                server_label.pack(pady=5)

                image_label = tk.Label(server_frame, image=photo)
                image_label.pack(pady=5)

                image_label.image = photo

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("微软雅黑", 12))

    else:
        messagebox.showinfo("服务器列表", "没有找到服务器")

def download_server(server_name):
    server_list = get_server_list()
    if server_name in server_list:
        server_url = server_list[server_name]["url"]
        messagebox.showinfo("下载服务器", f"正在下载服务器 {server_name} 的客户端...")
        response = requests.get(server_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024*1024
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        server_dir = os.path.join(base_dir, "server")
        os.makedirs(server_dir, exist_ok=True)
        with open(os.path.join(server_dir, f"{server_name}.zip"), 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        messagebox.showinfo("下载完成", "下载完成！")
    else:
        messagebox.showerror("找不到服务器", f"找不到服务器：{server_name}")

def search_servers():
    global entry_search, frame_server_list
    server_list = get_server_list()
    keyword = entry_search.get().strip()
    if keyword:
        matched_servers = [name for name in server_list.keys() if keyword.lower() in name.lower()]
        if matched_servers:
            show_search_results(matched_servers)
        else:
            messagebox.showinfo("搜索结果", "没有找到匹配的服务器")
    else:
        messagebox.showwarning("搜索关键字为空", "请输入要搜索的关键字")

def show_search_results(server_names):
    global frame_server_list
    for widget in frame_server_list.winfo_children():
        widget.destroy()

    for name in server_names:
        server_frame = tk.Frame(frame_server_list, bd=2, relief=tk.GROOVE, cursor="hand2", width=104, height=89)
        server_frame.pack(pady=5, padx=10, fill=tk.X)
        server_frame.bind("<Button-1>", lambda event, server_name=name: download_server(server_name))

        image_url = server_list[name]["image"]
        image_data = urllib.request.urlopen(image_url).read()
        photo = tk.PhotoImage(data=image_data)

        server_label = tk.Label(server_frame, text=name, font=("微软雅黑", 12))
        server_label.pack(pady=5)

        image_label = tk.Label(server_frame, image=photo)
        image_label.pack(pady=5)

        image_label.image = photo

def refresh_servers():
    show_all_servers()

def main():
    global entry_search, frame_server_list
    window_title = "Minecraft-ZLBOX"
    ctypes.windll.kernel32.SetConsoleTitleW(window_title)
    
    window = tk.Tk()

    window_width = 500
    window_height = 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_offset = (screen_width - window_width) // 2
    y_offset = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
    
    window.title(window_title)

    style = ttk.Style()
    style.theme_use('clam')

    bg_color = "#EBEBEB"
    window.configure(bg=bg_color)

    exit_button = tk.Button(
        window,
        text="退出", 
        command=window.quit,
        bg="red",
        fg="white",
        borderwidth=0,
        padx=10,
        pady=5,
        activebackground="#FF3333",
        activeforeground="white",
        cursor="hand2"
    )
    exit_button.pack(side=tk.RIGHT, padx=10, pady=10)

    frame_search = tk.Frame(window, bg=bg_color)
    frame_search.pack(fill=tk.X, padx=10, pady=10)

    label_search = tk.Label(frame_search, text="搜索服务器:", font=("微软雅黑", 12), bg=bg_color)
    label_search.pack(side=tk.LEFT)

    entry_search = tk.Entry(frame_search, font=("微软雅黑", 12), width=30)
    entry_search.pack(side=tk.LEFT, padx=5)

    button_search = tk.Button(
        frame_search,
        text="搜索",
        command=search_servers,
        bg="#4CAF50",
        fg="white",
        borderwidth=0,
        padx=10,
        pady=5,
        activebackground="#45A049",
        activeforeground="white",
        cursor="hand2"
    )
    button_search.pack(side=tk.LEFT)

    button_refresh = tk.Button(
        window,
        text="刷新",
        command=refresh_servers,
        bg="#2196F3",
        fg="white",
        borderwidth=0,
        padx=10,
        pady=5,
        activebackground="#1976D2",
        activeforeground="white",
        cursor="hand2"
    )
    button_refresh.pack(side=tk.RIGHT, padx=10, pady=10)

    frame_server_list = tk.Frame(window, bg=bg_color)
    frame_server_list.pack(fill=tk.BOTH, expand=True, padx=10)

    show_all_servers()

    notice = get_notice()
    if notice:
        messagebox.showinfo("公告", notice)

    window.mainloop()

if __name__ == "__main__":
    main()
