from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.edge.options import Options
import io
import tempfile
import os
import requests
import time
import re

import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 存储下载链接
links = []

# 临时 user data 目录，避免冲突
temp_user_data_dir = tempfile.mkdtemp()

# 配置 Edge 启动选项
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=zh_CN.UTF-8")
options.add_argument("--inprivate")
options.add_argument(f"--user-data-dir={temp_user_data_dir}")

# GitHub Actions 或 Linux 环境下设置浏览器路径
if os.name != "nt":
    options.binary_location = "/usr/bin/microsoft-edge"

# 启动 WebDriver
driver = webdriver.Edge(options=options)

# 打开原神新闻页
driver.get("https://genshin.hoyoverse.com/en/news/398")

# 自动点击“加载更多”直到结束
while True:
    try:
        driver.execute_script("window.scrollTo(0, 100);")
        driver.implicitly_wait(50)
        more_button = driver.find_element(By.CLASS_NAME, "news__more")
        more_button.click()
        driver.execute_script("window.scrollTo(0, 100);")
        time.sleep(1)
        print("Loading more...")
    except:
        print("Load complete.")
        break

# 获取所有标题
title_elements = driver.find_elements(By.CLASS_NAME, "news__title")

# 读取已下载链接
downloaded = []
if os.path.exists("downloaded.txt"):
    with open("downloaded.txt", "r", encoding="utf-8") as file:
        downloaded = [line.strip() for line in file.readlines()]

# 提取壁纸相关链接
for el in title_elements:
    title_text = el.text
    if "Calendar Wallpapers" in title_text:
        link = el.get_attribute("href")
        if link and link not in links:
            links.append(link)

# 过滤掉已经下载的链接
should_download = [link for link in links if link not in downloaded]

print("Total found:", len(links))
print("Need download:", len(should_download))

# 遍历下载页面
for link in should_download:
    driver.get(link)
    time.sleep(1)

    imgs = driver.find_elements(By.CSS_SELECTOR, "img[style='border:none;vertical-align:middle;']")
    print(f"Found {len(imgs)} images in {link}")

    # 使用标题作为文件夹名，清理非法字符
    raw_title = driver.title
    folder_name = re.sub(r'[\\/*?:"<>|]', "_", raw_title)
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # 下载所有图片
    for idx, img in enumerate(imgs, 1):
        src = img.get_attribute("src")
        if not src:
            continue
        print("Downloading:", src)
        try:
            response = requests.get(src)
            img_path = os.path.join(folder_path, f"{idx}.jpg")
            with open(img_path, "wb") as file:
                file.write(response.content)
        except Exception as e:
            print("Error downloading image:", e)

# 写入已下载链接
with open("downloaded.txt", "a", encoding="utf-8") as file:
    for link in should_download:
        file.write(link + "\n")

driver.quit()
print("All tasks complete.")
