import os
import glob
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import ctypes
import random
import threading

# 新增全局变量控制暂停和停止
stop_flag = False


def is_valid_wallpaper(image_path, required_width, required_height):
    with Image.open(image_path) as img:
        width, height = img.size
        # 增加对宽高比例的判断，确保符合横屏比例
        if is_wallpaper_var.get():
            ratio = width / height
            # 常见的横屏比例：16:9, 21:9, 4:3
            if not (ratio >= 1.77 and ratio <= 1.78) and not (ratio >= 2.33 and ratio <= 2.34) and not (ratio >= 1.33 and ratio <= 1.34):
                return False
        return width >= required_width and height >= required_height


def change_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)


def select_folder():
    folder_path = filedialog.askdirectory(title="选择文件夹")
    if folder_path:
        valid_wallpapers = []
        # 获取用户选择的分辨率
        resolution = resolution_var.get()
        if resolution == "最高":
            required_width, required_height = 0, 0
        else:
            required_width, required_height = map(int, resolution.split('x'))
        
        # 遍历所有子目录
        for root, dirs, files in os.walk(folder_path):
            image_paths = {}
            for file in files:
                if file.lower().endswith(('.jpg', '.png')):
                    # 将文件名转换为小写作为键，存储路径和分辨率
                    file_lower = file.lower()
                    image_path = os.path.join(root, file)
                    with Image.open(image_path) as img:
                        width, height = img.size
                        # 只添加当前目录下最高分辨率的图片
                        if file_lower not in image_paths or (width * height) > (image_paths[file_lower][1] * image_paths[file_lower][2]):
                            if resolution == "最高" or is_valid_wallpaper(image_path, required_width, required_height):
                                image_paths[file_lower] = (image_path, width, height)
            # 将当前目录下最高分辨率的图片添加到valid_wallpapers列表中
            if image_paths:
                highest_res_image = max(image_paths.values(), key=lambda x: x[1] * x[2])
                valid_wallpapers.append(highest_res_image[0])
        
        if valid_wallpapers:
            global selected_folder, valid_wallpapers_global
            selected_folder = folder_path
            valid_wallpapers_global = valid_wallpapers

            # 获取最高分辨率图片的信息
            highest_res_files = [os.path.basename(wallpaper) for wallpaper in valid_wallpapers]
            messagebox.showinfo(
                "文件夹选择成功",
                f"已选择文件夹：{folder_path}\n最高分辨率图片：{', '.join(highest_res_files)}"
            )
        else:
            messagebox.showinfo("没有有效壁纸", "在选定文件夹及其子目录中没有找到符合所选分辨率的壁纸。")
        # 更新列表显示
        update_wallpaper_list()


def update_wallpaper_list():
    if 'valid_wallpapers_global' in globals() and valid_wallpapers_global:
        wallpaper_listbox.delete(0, tk.END)
        for wallpaper in valid_wallpapers_global:
            # 获取图片的目录名
            dir_name = os.path.basename(os.path.dirname(wallpaper))
            # 在图片名前加上目录名
            wallpaper_listbox.insert(tk.END, f"{dir_name}/{os.path.basename(wallpaper)}")


def move_wallpaper_up():
    selection = wallpaper_listbox.curselection()
    if selection:
        index = selection[0]
        if index > 0:
            valid_wallpapers_global[index], valid_wallpapers_global[index - 1] = valid_wallpapers_global[index - 1], valid_wallpapers_global[index]
            update_wallpaper_list()
            wallpaper_listbox.select_set(index - 1)


def move_wallpaper_down():
    selection = wallpaper_listbox.curselection()
    if selection:
        index = selection[0]
        if index < len(valid_wallpapers_global) - 1:
            valid_wallpapers_global[index], valid_wallpapers_global[index + 1] = valid_wallpapers_global[index + 1], valid_wallpapers_global[index]
            update_wallpaper_list()
            wallpaper_listbox.select_set(index + 1)


def delete_wallpaper():
    selection = wallpaper_listbox.curselection()
    if selection:
        index = selection[0]
        del valid_wallpapers_global[index]
        update_wallpaper_list()


def add_wallpaper():
    file_paths = filedialog.askopenfilenames(title="选择壁纸文件", filetypes=[("图片文件", "*.jpg;*.png")])
    if file_paths:
        # 获取用户选择的分辨率
        resolution = resolution_var.get()
        if resolution == "最高":
            required_width, required_height = 0, 0
        else:
            required_width, required_height = map(int, resolution.split('x'))
        
        for file_path in file_paths:
            # 再次检查图片是否符合壁纸要求
            if is_valid_wallpaper(file_path, required_width, required_height):
                valid_wallpapers_global.append(file_path)
        # 添加完成后，再次检查并删除不符合要求的壁纸
        for i in range(len(valid_wallpapers_global) - 1, -1, -1):
            if not is_valid_wallpaper(valid_wallpapers_global[i], required_width, required_height):
                del valid_wallpapers_global[i]
        update_wallpaper_list()


def start_changing_wallpaper():
    global stop_flag
    stop_flag = False

    if 'valid_wallpapers_global' not in globals() or not valid_wallpapers_global:
        messagebox.showinfo("未选择文件夹", "请先选择一个包含有效壁纸的文件夹。")
        return

    try:
        interval = int(interval_entry.get())
        if interval <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("无效输入", "请输入一个有效的正整数作为间隔时间。")
        return

    order = order_var.get()
    loop = loop_var.get()
    # 将壁纸更换逻辑放在一个单独的线程中
    threading.Thread(target=change_wallpaper_thread, args=(interval, order, loop), daemon=True).start()


def change_wallpaper_thread(interval, order, loop):
    global stop_flag
    while not stop_flag:
        if not check_pause_and_stop():
            if order == "sequential":
                while not stop_flag:
                    for wallpaper in valid_wallpapers_global:
                        if stop_flag:
                            break
                        change_wallpaper(wallpaper)
                        # 更新标签内容
                        current_wallpaper_label.config(text=f"当前壁纸: {os.path.basename(wallpaper)}\n路径: {wallpaper}")
                        time.sleep(interval)
                    # 如果未启用循环播放，则退出
                    if not loop:
                        stop_flag = True
                        break
            elif order == "random":
                while not stop_flag:
                    random.shuffle(valid_wallpapers_global)
                    for wallpaper in valid_wallpapers_global:
                        if stop_flag:
                            break
                        change_wallpaper(wallpaper)
                        # 更新标签内容
                        current_wallpaper_label.config(text=f"当前壁纸: {os.path.basename(wallpaper)}\n路径: {wallpaper}")
                        time.sleep(interval)
                    # 如果未启用循环播放，则退出
                    if not loop:
                        stop_flag = True
                        break


def check_pause_and_stop():
    global stop_flag
    return stop_flag


def stop_changing_wallpaper():
    global stop_flag
    stop_flag = True


def select_next_folder():
    global selected_folder, valid_wallpapers_global
    # 获取当前目录的父目录
    parent_folder = os.path.dirname(selected_folder)
    # 获取父目录下的所有子目录
    sub_folders = [f.path for f in os.scandir(parent_folder) if f.is_dir()]
    # 找到当前目录在子目录列表中的索引
    current_index = sub_folders.index(selected_folder)
    # 计算下一个目录的索引
    next_index = (current_index + 1) % len(sub_folders)
    # 选择下一个目录
    selected_folder = sub_folders[next_index]
    # 更新壁纸列表
    select_folder()


def apply_and_check():
    if 'valid_wallpapers_global' in globals() and valid_wallpapers_global:
        # 获取用户选择的分辨率
        resolution = resolution_var.get()
        if resolution == "最高":
            required_width, required_height = 0, 0
        else:
            required_width, required_height = map(int, resolution.split('x'))
        
        # 检查并删除不符合要求的壁纸
        for i in range(len(valid_wallpapers_global) - 1, -1, -1):
            if not is_valid_wallpaper(valid_wallpapers_global[i], required_width, required_height):
                del valid_wallpapers_global[i]
        
        update_wallpaper_list()
        messagebox.showinfo("应用成功", "已应用配置并检查壁纸列表。")


def main():
    root = tk.Tk()
    root.title("壁纸更换器")
    root.geometry("800x500")

    # 创建左侧控件框架
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=20, pady=20)

    select_button = tk.Button(left_frame, text="选择文件夹", command=select_folder)
    select_button.pack(pady=10)

    global interval_entry
    interval_label = tk.Label(left_frame, text="更换间隔（秒）：")
    interval_label.pack(pady=5)
    interval_entry = tk.Entry(left_frame, width=20)
    interval_entry.pack(pady=5)

    global order_var
    order_var = tk.StringVar(value="sequential")
    order_label = tk.Label(left_frame, text="顺序：")
    order_label.pack(pady=5)
    sequential_radio = tk.Radiobutton(left_frame, text="顺序", variable=order_var, value="sequential")
    sequential_radio.pack(anchor=tk.W)
    random_radio = tk.Radiobutton(left_frame, text="随机", variable=order_var, value="random")
    random_radio.pack(anchor=tk.W)

    global loop_var
    loop_var = tk.BooleanVar(value=True)
    loop_check = tk.Checkbutton(left_frame, text="循环播放", variable=loop_var)
    loop_check.pack(pady=5)

    global resolution_var
    resolution_var = tk.StringVar(value="1920x1080")
    resolution_label = tk.Label(left_frame, text="分辨率：")
    resolution_label.pack(pady=5)
    resolution_options = ["1920x1080", "2560x1440", "3840x2160", "最高"]
    resolution_menu = tk.OptionMenu(left_frame, resolution_var, *resolution_options)
    resolution_menu.pack(pady=5)

    global is_wallpaper_var
    is_wallpaper_var = tk.BooleanVar(value=True)
    is_wallpaper_check = tk.Checkbutton(left_frame, text="是否为电脑壁纸", variable=is_wallpaper_var)
    is_wallpaper_check.pack(pady=5)

    start_button = tk.Button(left_frame, text="确定", command=start_changing_wallpaper)
    start_button.pack(side=tk.LEFT, pady=10, padx=5)

    apply_button = tk.Button(left_frame, text="应用", command=apply_and_check)
    apply_button.pack(side=tk.LEFT, pady=10, padx=5)

    stop_button = tk.Button(left_frame, text="停止", command=stop_changing_wallpaper)
    stop_button.pack(side=tk.LEFT, pady=10, padx=5)

    # 创建右侧壁纸列表管理框架
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

    global wallpaper_listbox
    wallpaper_listbox = tk.Listbox(right_frame, width=50, height=15)
    wallpaper_listbox.pack(side=tk.LEFT)

    list_buttons_frame = tk.Frame(right_frame)
    list_buttons_frame.pack(side=tk.RIGHT, padx=10)

    move_up_button = tk.Button(list_buttons_frame, text="上移", command=move_wallpaper_up)
    move_up_button.pack(pady=5)

    move_down_button = tk.Button(list_buttons_frame, text="下移", command=move_wallpaper_down)
    move_down_button.pack(pady=5)

    delete_button = tk.Button(list_buttons_frame, text="删除", command=delete_wallpaper)
    delete_button.pack(pady=5)

    add_button = tk.Button(list_buttons_frame, text="添加", command=add_wallpaper)
    add_button.pack(pady=5)

    global current_wallpaper_label
    current_wallpaper_label = tk.Label(left_frame, text="当前壁纸: 无", wraplength=400, justify="left")
    current_wallpaper_label.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()