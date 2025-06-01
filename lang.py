from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time
import sys

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

# Edge 配置
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=zh_CN")
options.add_argument("--inprivate")

driver = webdriver.Edge(options=options)
driver.get("https://www.hoyolab.com/creatorCollection/526679?utm_source=hoyolab&utm_medium=tools&lang=zh-cn&bbs_theme=light&bbs_theme_device=1")

wait = WebDriverWait(driver, 15)

# 1. 尝试关闭登录弹窗
try:
    close_login_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "el-dialog__headerbtn")))
    close_login_btn.click()
    print("已关闭登录弹窗")
except:
    print("未检测到登录弹窗")

# 2. 尝试点击“跳过”按钮
try:
    skip_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".hyl-button.normal__quaternary.hyl-button__md.hyl-button-loading__md")
    ))
    skip_btn.click()
    print("已点击跳过按钮")
except:
    print("未检测到跳过按钮")

# 3. 悬停头像区域
try:
    avatar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-avatar")))
    ActionChains(driver).move_to_element(avatar).perform()
    print("已悬停头像")
except:
    print("找不到头像，可能未登录")

# 4. 点击当前语言项
try:
    lang_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "header-account-menu-item__val")))
    lang_button.click()
    print("点击语言菜单成功")
except:
    print("语言菜单未找到")

# 5. 选择简体中文
try:
    lang_zhcn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mhy-selectmenu__item--zh-cn")))
    lang_zhcn.click()
    print("已切换为简体中文")
except:
    print("找不到简体中文选项，可能已是中文或加载失败")

time.sleep(5)
driver.quit()
