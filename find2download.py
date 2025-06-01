import requests,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import sys
import time
import os
import numpy as np
import tempfile
import re

# 清理文件名
def clean_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = re.sub(r'(\.png|\.jpg).*$', r'\1', filename)
    return filename

# 进度条
def progress_bar(current, total, width=80):
    progress = current / total
    bar = '#' * int(progress * width)
    percentage = round(progress * 100, 2)
    print(f'\r[{bar:<{width}}] {percentage}%', end='')

# 下载函数，带重试
def download_with_retry(url, path, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            total_length = int(response.headers.get('content-length', 0))
            with open(path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress_bar(downloaded, total_length)
            print(f'\nDownloaded: {url}')
            return True
        except Exception as e:
            print(f'\nFailed attempt {attempt + 1} for {url}: {e}')
            time.sleep(2)
    return False

sys.stdout.reconfigure(encoding='utf-8')
list = []
with open("shoulddownload.txt", "r", encoding="utf-8") as file:
    list = file.readlines()
print('gotfile',list)

download_url = []
webimg = []
failed = []

temp_user_data_dir = tempfile.mkdtemp()
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=zh_CN")
options.add_argument("--inprivate")
options.add_argument(f"--user-data-dir={temp_user_data_dir}")
options.binary_location = "/usr/bin/microsoft-edge"

driver = webdriver.Edge(options=options)





# wait = WebDriverWait(driver, 15)
# def change_language():
#     try:
#         close_login_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "el-dialog__headerbtn")))
#         close_login_btn.click()
#         print("已关闭登录弹窗")
#     except:
#         print("未检测到登录弹窗")

#     # 2. 尝试点击“跳过”按钮
#     try:
#         time.sleep(2)
#         skip_btn = wait.until(EC.element_to_be_clickable(
#             (By.CSS_SELECTOR, ".hyl-button.normal__quaternary.hyl-button__md.hyl-button-loading__md")
#         ))
#         skip_btn.click()
#         print("已点击跳过按钮")
#     except:
#         print("未检测到跳过按钮")

#     # 3. 悬停头像区域
#     try:
#         avatar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-avatar")))
#         ActionChains(driver).move_to_element(avatar).perform()
#         print("已悬停头像")
#     except:
#         print("找不到头像，可能未登录")

#     # 4. 点击当前语言项
#     try:
#         lang_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header-account-menu-item__val")))
#         lang_button.click()
#         print("点击语言菜单成功")
#     except:
#         print("语言菜单未找到")

#     # 5. 选择简体中文
#     try:
#         lang_zhcn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mhy-selectmenu__item--zh-cn")))
#         lang_zhcn.click()
#         print("已切换为简体中文")
#     except:
#         print("找不到简体中文选项，可能已是中文或加载失败")
















for url in list:
    driver.get(url)
    time.sleep(np.random.randint(5, 6))
    for i in range(4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(np.random.randint(3, 5))
    time.sleep(np.random.randint(3, 6))
    # change_language()
    title = driver.find_element(By.CLASS_NAME, "mhy-article-page__title").find_element(By.TAG_NAME, "h1").get_attribute('textContent')
    print(title)
    if not os.path.exists(title):
        os.mkdir(title)
    elements = driver.find_elements(By.CLASS_NAME, "blot-link")

    if elements:
        for element in elements:
            href = element.get_attribute("href")
            print("元素href属性:", href)
            if len(href) <= 26:
                download_url.append(href)
                base_name = href.split("/")[-1]
                extract_path = os.path.join(title, base_name)
                zip_path = os.path.join(title, base_name + ".zip")
                if not os.path.exists(extract_path) and not os.path.exists(zip_path):
                    success = download_with_retry(href, zip_path)
                    if not success:
                        failed.append(href)
                else:
                    print("文件已存在")
            else:
                print("未找到下载链接,开始查询页面图片")
                imgelements = driver.find_elements(By.CLASS_NAME, "ql-image-mask-wrapper")
                for img in imgelements:
                    src = img.find_element(By.TAG_NAME, "img").get_attribute("large")
                    print(src)
                    webimg.append(src)
                    img_path = os.path.join(title, clean_filename(src.split("/")[-1]))
                    if not os.path.exists(img_path):
                        success = download_with_retry(src, img_path)
                        if not success:
                            failed.append(src)
                    else:
                        print("文件已存在")
    else:
        print("未找到任何链接,开始查询页面图片")
        imgelements = driver.find_elements(By.CLASS_NAME, "ql-image-mask-wrapper")
        for img in imgelements:
            src = img.find_element(By.TAG_NAME, "img").get_attribute("large")
            print(src)
            webimg.append(src)
            img_path = os.path.join(title, clean_filename(src.split("/")[-1]))
            if not os.path.exists(img_path):
                success = download_with_retry(src, img_path)
                if not success:
                    failed.append(src)
            else:
                print("文件已存在")

# 保存数据
with open("download.txt", "w", encoding="utf-8") as file:
    for url in download_url:
        file.write(url + "\n")

with open("webimg.txt", "w", encoding="utf-8") as file:
    for url in webimg:
        file.write(url + "\n")

with open("failed.txt", "w", encoding="utf-8") as file:
    print("下载失败的链接:", failed)
    for url in failed:
        file.write(url + "\n")

with open("src.txt", "a", encoding="utf-8") as file:
    for url in list:
        file.write(url + "\n")

with open("shoulddownload.txt", "w", encoding="utf-8") as file:
    file.write("i'm finished!")
