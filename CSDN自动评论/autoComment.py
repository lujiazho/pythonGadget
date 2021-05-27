from selenium.webdriver import Chrome
import time

driver = Chrome()
driver.maximize_window()

driver.get(url='https://passport.csdn.net/login?code=public')
time.sleep(2)

# 找到账号密码登录并点击
login_button = driver.find_element_by_css_selector('#app > div > div > div.main > div.main-login > div.main-select > ul > li:nth-child(2) > a')
# print(login_button)
login_button.click()

# 账号密码输入框并且输入账号密码
all_input = driver.find_element_by_id('all') # 账号输入元素
paw_input = driver.find_element_by_id('password-number') # 密码输入元素
all_input.send_keys('***') # 需要修改
paw_input.send_keys('***') # 需要修改
# print(all_input, paw_input)

# 获取登录按钮点击登录
login_btn = driver.find_element_by_css_selector('#app > div > div > div.main > div.main-login > div.main-process-login > div > div:nth-child(6) > div > button')
login_btn.click()
time.sleep(3)
print(driver.current_url)

if 'login' not in driver.current_url:
    print('登录成功')

# 需要修改
driver.get('https://blog.csdn.net/****/article/details/****')
time.sleep(2)

commentArea = driver.find_element_by_id('comment_content')
commentArea.send_keys('好seilei啊')
time.sleep(2)
commentButton = driver.find_element_by_css_selector('#rightBox > a > input')
commentButton.click()

print(driver.current_url)