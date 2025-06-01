from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import io
import tempfile
import os
import requests
import time
import re
import sys

# 设置控制台编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Starting calendar downloader...")

# 链接存储
links = []

# 创建临时用户数据目录
temp_user_data_dir = tempfile.mkdtemp()

# Edge 配置
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=zh_CN.UTF-8")
options.add_argument("--inprivate")
options.add_argument(f"--user-data-dir={temp_user_data_dir}")

# GitHub Actions 兼容路径
if os.name != "nt":
    options.binary_location = "/usr/bin/microsoft-edge"

# 启动 Edge
driver = webdriver.Edge(options=options)
driver.get("https://genshin.hoyoverse.com/en/news/398")

# 自动点击“加载更多”
while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        more_button = driver.find_element(By.CLASS_NAME, "news__more")
        more_button.click()
        print("Loading more news...")
        time.sleep(1)
    except:
        print("All news loaded.")
        break

# 获取标题列表
title_elements = driver.find_elements(By.CLASS_NAME, "news__title")

# 已下载的链接
downloaded = []
if os.path.exists("downloaded.txt"):
    with open("downloaded.txt", "r", encoding="utf-8") as f:
        downloaded = [line.strip() for line in f.readlines()]

# 查找日历壁纸
for el in title_elements:
    if "Calendar Wallpapers" in el.text:
        href = el.get_attribute("href")
        if href and href not in links:
            links.append(href)

should_download = [link for link in links if link not in downloaded]

print("Total found:", len(links))
print("Need to download:", len(should_download))

# 下载处理
for link in should_download:
    driver.get(link)
    time.sleep(1)

    # 滚动触发懒加载
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # 使用你原来的选择器
    imgs = driver.find_elements(By.CSS_SELECTOR, "img[style='border:none;vertical-align:middle;']")
    print(f"Found {len(imgs)} images in {link}")

    # 清理标题作为文件夹名
    title = driver.title
    folder_name = re.sub(r'[\\/*?:"<>|]', "_", title)
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # 下载图片
    for idx, img in enumerate(imgs, 1):
        src = img.get_attribute("src")
        if not src:
            continue
        print("Downloading:", src)
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(src, headers=headers)
            if response.status_code == 200:
                img_path = os.path.join(folder_path, f"{idx}.jpg")
                with open(img_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Failed to get image (status {response.status_code})")
        except Exception as e:
            print("Error downloading:", e)

# 写入已下载链接
with open("downloaded.txt", "a", encoding="utf-8") as f:
    for link in should_download:
        f.write(link + "\n")

driver.quit()
print("✅ All tasks complete.")
