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

import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

links=[]

# 临时 user data 目录，避免冲突
temp_user_data_dir = tempfile.mkdtemp()

# 配置 Edge 启动选项
options = Options()
options.add_argument("--headless=new")  # 新版无头模式
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=zh_CN.UTF-8")  # 设置中文语言
options.add_argument("--inprivate")  # 隐私模式
options.add_argument(f"--user-data-dir={temp_user_data_dir}")  # 指定唯一 user-data-dir

if os.name != "nt":
    # 设置 Edge 二进制路径（GitHub Actions 上必须）
    options.binary_location = "/usr/bin/microsoft-edge"

# 启动 driver
driver = webdriver.Edge(options=options)

driver.get("https://genshin.hoyoverse.com/en/news/398")
while True:
    try:
        
        driver.execute_script("window.scrollTo(0, 100);")
        driver.implicitly_wait(50)
        anniu = driver.find_element(By.CLASS_NAME, "news__more")
        anniu.click()
        driver.execute_script("window.scrollTo(0, 100);")
        time.sleep(1)
        print("try")

    except:
        print("end")
        break
list= driver.find_elements(By.CLASS_NAME, "news__title")
print(list)

with open("downloaded.txt", "r") as file:
    downloaded=file.readlines()


for i in list:
    print(i.text)
    if "Calendar Wallpapers" in i.text :
        print(i.text)
        links.append(i.get_attribute("href"))

shoulddownload = [x for x in links if x not in downloaded]
print('got:',links)
print('should:',shoulddownload)

for link in links:
    driver.get(link)
    time.sleep(1)
    imgs= driver.find_elements(By.CSS_SELECTOR, "img[style='border:none;vertical-align:middle;']")
    print(imgs)
    a = driver.title
    os.makedirs(os.path.join(os.getcwd(), f"{a}"), exist_ok=True)
    i=0
    for img in imgs:
        i+=1
        print(img.get_attribute("src"))
        response = requests.get(img.get_attribute("src"))
        with open(os.path.join(os.getcwd() + "\\" + f"{a}", f"{i}.jpg"), "wb") as file:
            file.write(response.content)
driver.quit()

with open("downloaded.txt", "a") as file:
    alllinks = downloaded + shoulddownload
    for link in alllinks:
        file.write(link + "\n")