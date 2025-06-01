from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import numpy as np # 导入numpy库并简写为np
import wget
def progress_bar(current, total, width=80):
    progress = current / total
    bar = '#' * int(progress * width)
    percentage = round(progress * 100, 2)
    print(f'[{bar:<{width}}] {percentage}%')
sys.stdout.reconfigure(encoding='utf-8') # 设置标准输出流的编码为utf-8
list = []
file = open("src.txt", "r", encoding="utf-8")
lines = file.read().splitlines()
for line in lines:
    print(line)
    list.append(line)
print(list)
file.close()
download_url = []

webimg = []

options = webdriver.EdgeOptions()
options.add_argument('lang=zh_CN.UTF-8') # 设置中文
driver = webdriver.Edge(options=options)

driver.get("https://www.hoyolab.com/article/14617222")
time.sleep(np.random.randint(5, 6))

title_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "mhy-article-page__title"))
)

title = driver.find_element(By.CLASS_NAME, "mhy-article-page__title").find_element(By.TAG_NAME, "h1").get_attribute('textContent')


print(title)

# for i in range(4):    
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(np.random.randint(3, 5))
# time.sleep(np.random.randint(3, 6))




# title = driver.find_element(By.CLASS_NAME, "mhy-article-page__main mhy-container").find_element(By.TAG_NAME, "h1").text



# elements = driver.find_elements(By.CLASS_NAME, "blot-link")
# for element in elements:
#     print("元素href属性:", element.get_attribute("href"))
#     if len(element.get_attribute("href"))<=26:
#         download_url.append(element.get_attribute("href"))
#         wget.download(element.get_attribute("href"), out=title + "/" + element.get_attribute("href").split("/")[-1], bar=progress_bar)
#     else:
#         print("未找到下载链接,开始查询页面图片")
#         imgelements = driver.find_elements(By.CLASS_NAME, "ql-image-mask-wrapper")
#         for img in imgelements:
#             print(img.find_element(By.TAG_NAME, "img").get_attribute("large"))
#             webimg.append(img.find_element(By.TAG_NAME, "img").get_attribute("large"))
#             wget.download(img.find_element(By.TAG_NAME, "img").get_attribute("large"), out=title + "/" + img.find_element(By.TAG_NAME, "img").get_attribute("large").split("/")[-1], bar=progress_bar)
#     time.sleep(np.random.randint(3, 6))
# print(webimg)
# time.sleep(np.random.randint(3, 6))
# driver.quit()
