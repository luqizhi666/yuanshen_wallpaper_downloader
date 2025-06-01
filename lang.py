from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import sys
import time

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

# 配置 Edge 浏览器
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=zh_CN")
options.add_argument("--inprivate")

driver = webdriver.Edge(options=options)
driver.get("https://www.hoyolab.com/creatorCollection/526679?utm_source=hoyolab&utm_medium=tools&lang=zh-cn&bbs_theme=light&bbs_theme_device=1")

wait = WebDriverWait(driver, 15)

# 1. 点击“跳过”按钮
try:
    skip_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".hyl-button.normal__quaternary.hyl-button__md.hyl-button-loading__md")
    ))
    skip_button.click()
    print("已点击跳过按钮")
except:
    print("未出现跳过按钮")

# 2. 悬停头像区域
try:
    avatar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-avatar")))
    ActionChains(driver).move_to_element(avatar).perform()
    print("悬停头像成功")
except:
    print("找不到头像，可能未登录或加载失败")
    driver.quit()
    exit()

# 3. 点击语言选项
try:
    lang_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header-account-menu-item__val")))
    lang_button.click()
    print("点击语言菜单成功")
except:
    print("语言菜单未找到")
    driver.quit()
    exit()

# 4. 点击“简体中文”项
try:
    lang_zhcn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mhy-selectmenu__item--zh-cn")))
    lang_zhcn.click()
    print("已切换为简体中文")
except:
    print("找不到简体中文选项，可能已是中文或加载失败")

# 保持几秒观察效果
time.sleep(5)
driver.quit()
