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
# options.add_argument("--headless=new")  # 调试时建议注释掉，方便观察页面
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Edge(options=options)
driver.get("https://www.hoyolab.com/article/39056688/")

wait = WebDriverWait(driver, 20)
time.sleep(5)

# 打印部分页面源码，便于调试
print(driver.page_source[:4000])

# 检查并切换到登录iframe（如果存在）
iframe_switched = False
try:
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "hyv-account-frame")))
    iframe_switched = True
    print("已切换到登录iframe")
except Exception as e:
    print("未检测到登录iframe，尝试在主页面查找", e)

# 1. 尝试关闭登录弹窗（主页面和iframe都查找一次）
def try_close_login_dialog(driver, wait):
    # 主页面查找
    try:
        driver.switch_to.default_content()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".el-dialog")))
        close_login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-dialog__headerbtn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", close_login_btn)
        close_login_btn.click()
        print("已关闭登录弹窗（主页面）")
        return True
    except Exception as e:
        print("主页面未检测到登录弹窗", e)
    # iframe 查找
    try:
        driver.switch_to.frame("hyv-account-frame")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".el-dialog")))
        close_login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-dialog__headerbtn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", close_login_btn)
        close_login_btn.click()
        print("已关闭登录弹窗（iframe）")
        driver.switch_to.default_content()
        return True
    except Exception as e:
        print("iframe未检测到登录弹窗", e)
        driver.switch_to.default_content()
    return False

try_close_login_dialog(driver, wait)

# 2. 尝试点击“跳过”按钮
try:
    skip_btn = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[span[text()='跳过']]")
    ))
    driver.execute_script("arguments[0].scrollIntoView(true);", skip_btn)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='跳过']]")))
    skip_btn.click()
    print("已点击跳过按钮")
except Exception as e:
    print("未检测到跳过按钮", e)

# 切回主页面（如果切换过iframe）
if iframe_switched:
    driver.switch_to.default_content()

# 3. 悬停头像区域
try:
    avatar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".header-avatar")))
    ActionChains(driver).move_to_element(avatar).perform()
    print("已悬停头像")
except Exception as e:
    print("找不到头像，可能未登录", e)

# 4. 点击当前语言项
try:
    lang_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".header-account-menu-item__val")))
    lang_button.click()
    print("点击语言菜单成功")
except Exception as e:
    print("语言菜单未找到", e)

# 5. 选择简体中文
try:
    lang_zhcn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mhy-selectmenu__item--zh-cn")))
    lang_zhcn.click()
    print("已切换为简体中文")
except Exception as e:
    print("找不到简体中文选项，可能已是中文或加载失败", e)

time.sleep(5)
driver.quit()
