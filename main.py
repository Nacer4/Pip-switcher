import tkinter as tk
from tkinter import ttk
import subprocess
import os
import configparser
import requests
from threading import Thread
from queue import Queue

# 定义国内常用的镜像源
sources = {
    '阿里云': 'https://mirrors.aliyun.com/pypi/simple/',
    '清华大学': 'https://pypi.tuna.tsinghua.edu.cn/simple/',
    '中国科技大学': 'https://pypi.mirrors.ustc.edu.cn/simple/',
    '豆瓣': 'https://pypi.douban.com/simple/',
    '华中科技大学': 'https://pypi.hustunique.com/',
    '山东理工大学': 'https://pypi.sdutlinux.org/simple/',
}

# 定义pip源
pip_sources = {
    "清华大学": sources['清华大学'],
    "阿里云": sources['阿里云'],
    "中国科技大学": sources['中国科技大学'],
    "豆瓣": sources['豆瓣'],
    "华中科技大学": sources['华中科技大学'],
    "山东理工大学": sources['山东理工大学'],
}


class PipSourceSwitcher:
    def __init__(self, master):
        self.master = master
        master.title("Pip 源切换器")

        # 居中显示窗口
        self.center_window()

        # 创建表格
        self.table = ttk.Treeview(master, columns=("名称", "URL"), show="headings")
        self.table.heading("名称", text="名称")
        self.table.heading("URL", text="URL")
        self.table.grid(row=0, column=0, columnspan=2, sticky="ew")

        # 添加数据到表格
        self.fill_table()

        # 创建下拉框
        self.source_var = tk.StringVar()
        self.source_var.set(list(pip_sources.keys())[0])  # 默认值
        self.dropdown = ttk.Combobox(master, textvariable=self.source_var, values=list(pip_sources.keys()))
        self.dropdown.grid(row=1, column=0, sticky="ew")

        # 创建按钮
        self.temp_button = ttk.Button(master, text="临时切换", command=self.switch_temporarily)
        self.temp_button.grid(row=2, column=0, sticky="ew")

        self.permanent_button = ttk.Button(master, text="永久切换", command=self.switch_permanently)
        self.permanent_button.grid(row=2, column=1, sticky="ew")

        # 创建文本框
        self.text_box = tk.Text(master, height=5, width=50)
        self.text_box.grid(row=3, column=0, columnspan=2, sticky="ew")

        # 创建自动选择按钮
        self.auto_select_button = ttk.Button(master, text="自动选择最优源", command=self.select_best_source)
        self.auto_select_button.grid(row=1, column=1, sticky="ew")

    def center_window(self):
        window_width = 600
        window_height = 400
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    def fill_table(self):
        for name, url in sources.items():
            self.table.insert("", "end", values=(name, url))

    def switch_temporarily(self):
        source_url = pip_sources[self.source_var.get()]
        if not source_url:
            self.text_box.insert(tk.END, "使用默认pip源。\n")
        else:
            subprocess.run(['pip', 'config', 'set', 'global.index-url', source_url])
            self.text_box.insert(tk.END, f"已临时切换到 {source_url}\n")

    def switch_permanently(self):
        source_url = pip_sources[self.source_var.get()]
        if not source_url:
            self.text_box.insert(tk.END, "使用默认pip源。\n")
            return

        config_file = os.path.expanduser("~/.config/pip/pip.conf")
        config = configparser.ConfigParser()
        if not os.path.exists(config_file):
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            config['global'] = {'index-url': source_url}
        else:
            config.read(config_file)
            config.set('global', 'index-url', source_url)

        with open(config_file, 'w') as configfile:
            config.write(configfile)

        self.text_box.insert(tk.END, f"已永久切换到 {source_url}\n")

    def select_best_source(self):
        # 使用线程来避免阻塞GUI
        thread = Thread(target=self._select_best_source)
        thread.start()

    def _select_best_source(self):
        best_source = None
        min_response_time = float('inf')
        response_times = {}

        # 使用队列来存储响应时间
        q = Queue()

        def measure_source(url, q):
            try:
                response = requests.head(url, timeout=5)
                response_time = response.elapsed.total_seconds()
                q.put((url, response_time))
            except requests.exceptions.RequestException:
                q.put((url, float('inf')))

        threads = []
        for url in sources.values():
            t = Thread(target=measure_source, args=(url, q))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        while not q.empty():
            url, response_time = q.get()
            response_times[url] = response_time
            if response_time < min_response_time:
                min_response_time = response_time
                best_source = url

        self.text_box.insert(tk.END, "测量完成，最佳源是: " + best_source + "\n")
        self.text_box.insert(tk.END, "响应时间: " + str(min_response_time) + " 秒\n")
        self.text_box.insert(tk.END, "所有源的响应时间: \n")
        for url, time in response_times.items():
            self.text_box.insert(tk.END, f"{url}: {time:.2f}秒\n")

        # 设置最佳源为下拉框的选中项
        for key, value in pip_sources.items():
            if value == best_source:
                self.source_var.set(key)
                break


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = PipSourceSwitcher(root)
    root.mainloop()
