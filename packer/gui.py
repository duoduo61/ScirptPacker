import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Menu, ttk
import threading
import webbrowser
from pathlib import Path
from .core import pack_script
from .utils import get_resource_path
from PIL import Image, ImageTk

class PackerGUI:
    def __init__(self, root):
        self.root = root
        self.lang = 'zh'
        self.lang_var = tk.StringVar(value='zh')
        self.strings = {
            'zh': {
                'app_title': 'ScriptPacker - 一键打包工具',
                'loading_text': '正在初始化...',
                'script_label': '脚本:',
                'output_label': '输出:',
                'name_label': '名称:',
                'icon_label': '图标:',
                'options_onefile': '打包为单文件 (--onefile)',
                'options_console': '显示控制台 (--console)',
                'resources_label': '附加资源:',
                'btn_browse': '浏览...',
                'btn_add_file': '添加文件',
                'btn_add_dir': '添加目录',
                'btn_remove': '移除选中',
                'btn_pack': '开始打包',
                'btn_clear_log': '清空日志',
                'log_label': '打包日志:',
                'menu_help': '帮助',
                'menu_about': '关于',
                'menu_language': '语言',
                'menu_zh': '中文',
                'menu_en': 'English',
                'about_title': '关于 ScriptPacker',
                'about_version': 'ScriptPacker v1.0.0',
                'about_link_text': '开源地址',
                'about_author': '作者：duoduo61',
                'about_license': '许可：MIT',
                'optional_label': '(可选)',
                'error_no_script_title': '错误',
                'error_no_script_msg': '请选择要打包的脚本文件',
                'error_pack_fail_title': '打包失败',
            },
            'en': {
                'app_title': 'ScriptPacker - One-Click Packer',
                'loading_text': 'Initializing...',
                'script_label': 'Script:',
                'output_label': 'Output:',
                'name_label': 'Name:',
                'icon_label': 'Icon:',
                'options_onefile': 'Package as one file (--onefile)',
                'options_console': 'Show console (--console)',
                'resources_label': 'Additional Resources:',
                'btn_browse': 'Browse...',
                'btn_add_file': 'Add File',
                'btn_add_dir': 'Add Directory',
                'btn_remove': 'Remove Selected',
                'btn_pack': 'Start Packing',
                'btn_clear_log': 'Clear Log',
                'log_label': 'Packaging Log:',
                'menu_help': 'Help',
                'menu_about': 'About',
                'menu_language': 'Language',
                'menu_zh': '中文',
                'menu_en': 'English',
                'about_title': 'About ScriptPacker',
                'about_version': 'ScriptPacker v1.0.0',
                'about_link_text': 'Source Code',
                'about_author': 'Author: duoduo61',
                'about_license': 'License: MIT',
                'optional_label': '(optional)',
                'error_no_script_title': 'Error',
                'error_no_script_msg': 'Please select a script file to pack',
                'error_pack_fail_title': 'Packaging Failed',
            }
        }

        # 变量
        self.script_path = tk.StringVar()
        self.output_dir = tk.StringVar(value="./dist")
        self.app_name = tk.StringVar()
        self.icon_path = tk.StringVar()
        self.onefile = tk.BooleanVar(value=False)
        self.console = tk.BooleanVar(value=True)
        self.extra_resources = []

        # 设置全局字体和窗口大小
        default_font = ("微软雅黑", 10)
        root.option_add("*Font", default_font)
        root.geometry("580x620")
        root.resizable(False, False)

        self._show_loading()
        root.after(1000, self._init_ui)

    def _show_loading(self):
        self.root.title(self.strings[self.lang]['app_title'])
        canvas = tk.Canvas(self.root, width=580, height=620, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        img_path = get_resource_path("image/start.png")
        try:
            if img_path.exists():
                img = Image.open(img_path)
                img = img.resize((580, 620), Image.Resampling.LANCZOS)
                self.bg_img = ImageTk.PhotoImage(img)
                canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_img)
            else:
                canvas.create_rectangle(0, 0, 580, 620, fill="#2b2b2b")
        except Exception:
            canvas.create_rectangle(0, 0, 580, 620, fill="#2b2b2b")

        loading_txt = self.strings[self.lang]['loading_text']
        canvas.create_text(290, 320, text=loading_txt, font=("微软雅黑", 28, "bold"), fill="#333333")
        canvas.create_text(290, 318, text=loading_txt, font=("微软雅黑", 28, "bold"), fill="white")
        self.loading_canvas = canvas

    def _init_ui(self):
        if hasattr(self, 'loading_canvas'):
            self.loading_canvas.destroy()
            del self.loading_canvas

        self.create_widgets()
        self.update_ui()
        # 确保主界面与加载界面尺寸完全一致
        self.root.geometry("580x620")

    def create_menu(self):
        menubar = Menu(self.root, font=("微软雅黑", 10))
        self.root.config(menu=menubar)
        self.menubar = menubar

        s = self.strings[self.lang]

        help_menu = Menu(menubar, tearoff=0, font=("微软雅黑", 10))
        menubar.add_cascade(label=s['menu_help'], menu=help_menu)
        help_menu.add_command(label=s['menu_about'], command=self.show_about)

        lang_menu = Menu(menubar, tearoff=0, font=("微软雅黑", 10))
        menubar.add_cascade(label=s['menu_language'], menu=lang_menu)
        lang_menu.add_radiobutton(
            label=s['menu_zh'],
            variable=self.lang_var,
            value='zh',
            command=lambda: self.change_language('zh')
        )
        lang_menu.add_radiobutton(
            label=s['menu_en'],
            variable=self.lang_var,
            value='en',
            command=lambda: self.change_language('en')
        )

    def show_about(self):
        about_win = tk.Toplevel(self.root)
        about_win.title(self.strings[self.lang]['about_title'])
        about_win.geometry("300x200")
        about_win.resizable(False, False)

        tk.Label(about_win, text=self.strings[self.lang]['about_version'], font=("微软雅黑", 12)).pack(pady=(20, 5))

        link_text = self.strings[self.lang]['about_link_text']
        link_lbl = tk.Label(about_win, text=link_text, fg="blue", cursor="hand2", font=("微软雅黑", 10, "underline"))
        link_lbl.pack(pady=5)
        link_lbl.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/duoduo61/ScirptPacker"))

        tk.Label(about_win, text=self.strings[self.lang]['about_author'], font=("微软雅黑", 10)).pack(pady=2)
        tk.Label(about_win, text=self.strings[self.lang]['about_license'], font=("微软雅黑", 10)).pack(pady=2)

        tk.Button(about_win, text="OK", command=about_win.destroy, width=10).pack(pady=15)

        about_win.transient(self.root)
        about_win.grab_set()
        self.root.wait_window(about_win)

    def change_language(self, lang):
        if lang != self.lang:
            self.lang = lang
            self.lang_var.set(lang)
            self.update_ui()

    def update_ui(self):
        self.root.title(self.strings[self.lang]['app_title'])
        self.create_menu()

        s = self.strings[self.lang]

        self.lbl_script.config(text=s['script_label'])
        self.btn_browse_script.config(text=s['btn_browse'])

        self.lbl_output.config(text=s['output_label'])
        self.btn_browse_output.config(text=s['btn_browse'])

        self.lbl_name.config(text=s['name_label'])
        self.lbl_optional.config(text=s['optional_label'])

        self.lbl_icon.config(text=s['icon_label'])
        self.btn_browse_icon.config(text=s['btn_browse'])

        self.chk_onefile.config(text=s['options_onefile'])
        self.chk_console.config(text=s['options_console'])

        self.lbl_resources.config(text=s['resources_label'])
        self.btn_add_file.config(text=s['btn_add_file'])
        self.btn_add_dir.config(text=s['btn_add_dir'])
        self.btn_remove_res.config(text=s['btn_remove'])

        if self.pack_btn['state'] != tk.DISABLED:
            self.pack_btn.config(text=s['btn_pack'])

        self.lbl_log.config(text=s['log_label'])
        self.btn_clear_log.config(text=s['btn_clear_log'])

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        s = self.strings[self.lang]

        # 脚本文件
        row1 = tk.Frame(main_frame)
        row1.pack(fill=tk.X, pady=2)
        self.lbl_script = tk.Label(row1, text=s['script_label'], width=6, anchor='w')
        self.lbl_script.pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.script_path, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn_browse_script = tk.Button(row1, text=s['btn_browse'], command=self.browse_script)
        self.btn_browse_script.pack(side=tk.LEFT, padx=5)

        # 输出目录
        row2 = tk.Frame(main_frame)
        row2.pack(fill=tk.X, pady=2)
        self.lbl_output = tk.Label(row2, text=s['output_label'], width=6, anchor='w')
        self.lbl_output.pack(side=tk.LEFT)
        tk.Entry(row2, textvariable=self.output_dir, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn_browse_output = tk.Button(row2, text=s['btn_browse'], command=self.browse_output)
        self.btn_browse_output.pack(side=tk.LEFT, padx=5)

        # 程序名称
        row3 = tk.Frame(main_frame)
        row3.pack(fill=tk.X, pady=2)
        self.lbl_name = tk.Label(row3, text=s['name_label'], width=6, anchor='w')
        self.lbl_name.pack(side=tk.LEFT)
        tk.Entry(row3, textvariable=self.app_name, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.lbl_optional = tk.Label(row3, text=s['optional_label'])
        self.lbl_optional.pack(side=tk.LEFT, padx=5)

        # 图标文件
        row4 = tk.Frame(main_frame)
        row4.pack(fill=tk.X, pady=2)
        self.lbl_icon = tk.Label(row4, text=s['icon_label'], width=6, anchor='w')
        self.lbl_icon.pack(side=tk.LEFT)
        tk.Entry(row4, textvariable=self.icon_path, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn_browse_icon = tk.Button(row4, text=s['btn_browse'], command=self.browse_icon)
        self.btn_browse_icon.pack(side=tk.LEFT, padx=5)

        # 选项
        row5 = tk.Frame(main_frame)
        row5.pack(fill=tk.X, pady=8)
        self.chk_onefile = tk.Checkbutton(row5, text=s['options_onefile'], variable=self.onefile)
        self.chk_onefile.pack(side=tk.LEFT, padx=2)
        self.chk_console = tk.Checkbutton(row5, text=s['options_console'], variable=self.console)
        self.chk_console.pack(side=tk.LEFT, padx=20)

        # 附加资源（微调宽度，避免遮挡文本）
        res_frame = tk.Frame(main_frame)
        res_frame.pack(fill=tk.X, pady=5)
        self.lbl_resources = tk.Label(res_frame, text=s['resources_label'], width=8, anchor='w')
        self.lbl_resources.pack(side=tk.LEFT)
        self.res_listbox = tk.Listbox(res_frame, height=3, width=32)
        self.res_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        btn_frame = tk.Frame(res_frame)
        btn_frame.pack(side=tk.RIGHT)
        self.btn_add_file = tk.Button(btn_frame, text=s['btn_add_file'], command=self.add_resource_file)
        self.btn_add_file.pack(side=tk.TOP, fill=tk.X, pady=1)
        self.btn_add_dir = tk.Button(btn_frame, text=s['btn_add_dir'], command=self.add_resource_dir)
        self.btn_add_dir.pack(side=tk.TOP, fill=tk.X, pady=1)
        self.btn_remove_res = tk.Button(btn_frame, text=s['btn_remove'], command=self.remove_resource)
        self.btn_remove_res.pack(side=tk.TOP, fill=tk.X, pady=1)

        # 打包按钮
        btn_frame2 = tk.Frame(main_frame)
        btn_frame2.pack(fill=tk.X, pady=10)
        self.pack_btn = tk.Button(btn_frame2, text=s['btn_pack'], command=self.start_pack,
                                  bg="lightblue", font=("微软雅黑", 11, "bold"))
        self.pack_btn.pack()

        # 日志区域
        log_frame = tk.Frame(main_frame)
        log_frame.pack(fill=tk.X, pady=(10, 0))
        self.lbl_log = tk.Label(log_frame, text=s['log_label'], anchor='w')
        self.lbl_log.pack(side=tk.LEFT)
        self.progress = ttk.Progressbar(log_frame, mode='indeterminate', length=100)
        self.progress.pack(side=tk.RIGHT, padx=5)
        self.progress.pack_forget()

        self.log_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=14, state='normal')
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

        self.btn_clear_log = tk.Button(main_frame, text=s['btn_clear_log'], command=self.clear_log)
        self.btn_clear_log.pack(pady=2)

    # ----- 资源管理 -----
    def add_resource_file(self):
        path = filedialog.askopenfilename(title="选择附加资源文件")
        if path:
            self.extra_resources.append(path)
            self.res_listbox.insert(tk.END, path)

    def add_resource_dir(self):
        path = filedialog.askdirectory(title="选择附加资源目录")
        if path:
            self.extra_resources.append(path)
            self.res_listbox.insert(tk.END, path)

    def remove_resource(self):
        selection = self.res_listbox.curselection()
        if selection:
            index = selection[0]
            self.res_listbox.delete(index)
            del self.extra_resources[index]

    # ----- 浏览函数 -----
    def browse_script(self):
        path = filedialog.askopenfilename(
            title="选择 Python 脚本",
            filetypes=[("Python 文件", "*.py"), ("所有文件", "*.*")]
        )
        if path:
            self.script_path.set(path)
            if not self.app_name.get():
                self.app_name.set(Path(path).stem)

    def browse_output(self):
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_dir.set(path)

    def browse_icon(self):
        path = filedialog.askopenfilename(
            title="选择图标文件 (.ico)",
            filetypes=[("图标文件", "*.ico"), ("所有文件", "*.*")]
        )
        if path:
            self.icon_path.set(path)

    # ----- 日志操作 -----
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def append_log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_progress(self):
        self.progress.pack(side=tk.RIGHT, padx=5)
        self.progress.start(10)

    def stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()

    # ----- 打包启动 -----
    def start_pack(self):
        s = self.strings[self.lang]
        if not self.script_path.get():
            messagebox.showerror(s['error_no_script_title'], s['error_no_script_msg'])
            return

        self.pack_btn.config(state=tk.DISABLED, text="打包中...")
        self.clear_log()
        self.append_log("开始打包任务...")
        self.start_progress()

        thread = threading.Thread(target=self.pack_thread, daemon=True)
        thread.start()

    def pack_thread(self):
        s = self.strings[self.lang]
        try:
            pack_script(
                script_path=self.script_path.get(),
                output_dir=self.output_dir.get() or "./dist",
                name=self.app_name.get().strip() or None,
                icon=self.icon_path.get().strip() or None,
                onefile=self.onefile.get(),
                console=self.console.get(),
                extra_resources=self.extra_resources if self.extra_resources else None,
                callback=self.append_log
            )
        except Exception as e:
            self.append_log(f"错误: {e}")
            self.root.after(0, lambda: messagebox.showerror(s['error_pack_fail_title'], str(e)))
        finally:
            self.root.after(0, lambda: self.pack_btn.config(state=tk.NORMAL, text=self.strings[self.lang]['btn_pack']))
            self.root.after(0, lambda: self.append_log("打包任务结束。"))
            self.root.after(0, self.stop_progress)

def main():
    root = tk.Tk()
    app = PackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
