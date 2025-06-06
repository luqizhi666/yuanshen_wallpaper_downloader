from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from selenium.webdriver.edge.options import Options
import tempfile

sys.stdout.reconfigure(encoding='utf-8') # 设置标准输出流的编码为utf-8


file = open("src.txt", "r", encoding="utf-8")
list = []

# 临时 user data 目录，避免冲突
temp_user_data_dir = tempfile.mkdtemp()

# 配置 Edge 启动选项
options = Options()
options.add_argument("--headless=new")  # 新版无头模式
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=zh_CN")  # 设置中文语言
options.add_argument("--inprivate")  # 隐私模式
options.add_argument(f"--user-data-dir={temp_user_data_dir}")  # 指定唯一 user-data-dir

# 设置 Edge 二进制路径（GitHub Actions 上必须）
options.binary_location = "/usr/bin/microsoft-edge"

# 启动 driver
driver = webdriver.Edge(options=options)

# 设置全局 Accept-Language 请求头（CDP）
try:
    driver.execute_cdp_cmd(
        "Network.setExtraHTTPHeaders",
        {"headers": {"Accept-Language": "zh-CN,zh;q=0.9"}}
    )
    driver.execute_cdp_cmd("Network.enable", {})
except Exception as e:
    print("全局设置Accept-Language失败", e)

driver.get("https://www.hoyolab.com/creatorCollection/526679?utm_source=hoyolab&utm_medium=tools&lang=zh-cn&bbs_theme=light&bbs_theme_device=1")

# time.sleep(20)
driver.implicitly_wait(10)

# ActionChains(driver)\
#     .key_down(Keys.DOWN)\
#     .perform()

time.sleep(30)
for i in range(10):    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

print(driver.page_source[:4000])  # 打印部分页面源码，便于调试
# driver.implicitly_wait(0.5)

# ActionChains(driver)\
#     .key_up(Keys.DOWN)\
#     .perform()

# driver.implicitly_wait(10)

# element = driver.find_element(By.CLASS_NAME, ".mhy-router-link mhy-article-card__link")

# print (element)

try:
    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.CLASS_NAME, ".mhy-router-link.mhy-article-card__link"))
    # )
    
    elements = driver.find_elements(By.CLASS_NAME, "mhy-router-link.mhy-article-card__link")

    # print(element)
    # print("元素文本内容:", element.text)
    for element in elements:
        print("元素href属性:", element.get_attribute("href"))
        list.append(element.get_attribute("href"))
except Exception as e:
    print(f"元素未找到: {e}")

# element.click()
driver.quit()

havegot=file.readlines()
print("got:",list)
file.close()
shoulddownload = [x for x in list if x not in havegot]
print("shoulddownload:", shoulddownload)
with open("shoulddownload.txt", "w", encoding="utf-8") as file:
    for i in shoulddownload:
        file.write(i)
        file.write("\n")
    # file.write(str(list))
