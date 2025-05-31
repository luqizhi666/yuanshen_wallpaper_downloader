from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from selenium.webdriver.edge.options import Options

sys.stdout.reconfigure(encoding='utf-8') # 设置标准输出流的编码为utf-8


file = open("src.txt", "w", encoding="utf-8")
list = []

options = webdriver.EdgeOptions()
options.add_argument('lang=zh_CN.UTF-8') # 设置中文
driver = webdriver.Edge(options=options)
edge_options = Options()
    
# 无头模式配置（新版语法）
options.add_argument("--headless=new")

# Linux 必需参数
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 方案1：使用隐私模式（推荐）
options.add_argument("--inprivate")

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

driver.quit()
print(list)
for i in list:
    file.write(i)
    file.write("\n")
# file.write(str(list))
file.close()