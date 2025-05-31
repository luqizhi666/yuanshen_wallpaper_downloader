from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.edge.options import Options


import os
import requests
import time

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

links=[]
driver = webdriver.Edge()
# 设置 Edge 无头模式
edge_options = Options()
edge_options.add_argument("--headless")  # 启用无头模式

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
for i in list:
    print(i.text)
    if "Calendar Wallpapers" in i.text :
        print(i.text)
        links.append(i.get_attribute("href"))
print(links)
a=0
for link in links:
    driver.get(link)
    time.sleep(1)
    imgs= driver.find_elements(By.CSS_SELECTOR, "img[style='border:none;vertical-align:middle;']")
    print(imgs)
    a+=1
    os.makedirs(os.path.join(os.getcwd(), f"{a}"), exist_ok=True)
    i=0
    for img in imgs:
        i+=1
        print(img.get_attribute("src"))
        response = requests.get(img.get_attribute("src"))
        with open(os.path.join(os.getcwd() + "\\" + f"{a}", f"{i}.jpg"), "wb") as file:
            file.write(response.content)