from selenium.webdriver import Chrome
import random
import time

comments = [
    '由浅入深，适合有基础的技术人员。大佬可否给小弟回个赞感谢万分',
    '作者辛苦了，学习的道路上一起进步。期待大佬的回访和关注~',
    '创作不易，给你打气，继续创作优质好文！',
    '学习了，感谢您的分享，让我受益良多！',
    '给大佬递茶，最近也在学习相关知识，希望得到大佬的肯定和支持！',
    '看完大佬的文章，我的心情竟是久久不能平静。正如老子所云：大音希声，大象无形。我现在终于明白我缺乏的是什么了。',
    '赞啊，写得真棒，一篇佳作，期待您的回复与关注！',
    '忍不住就是一个赞，写得很棒，欢迎回赞哦~',
    '都是博主辛苦创作，我来支持一下，奥利给！',
    '学会了，感谢大佬分享，继续努力！',
    '我真是服了，像你这种人就是欠赞和关注，哼~',
    '君之妙笔，令鄙不及，佩服佩服，如若能给小弟回个赞，必将感激涕尽！',
    '哇，好棒啊，崇拜的小眼神，欢迎回赞，回评哦~',
    '你好，我是警察，你因为太有才华被逮捕了，去我的博客瞅瞅才能释放你~',
    '代码之路任重道远，愿跟博主努力习之。',
    '666，反手就是一个赞，欢迎回赞哦~',
    '写得好，很nice，欢迎一起交流！',
    '果然是大佬，就是和我们这种普通开发不一样！',
    '满满的干货，我嗅到了知识的芬芳~'
]

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
commentArea.send_keys(random.choice(comments))
time.sleep(2)
commentButton = driver.find_element_by_css_selector('#rightBox > a > input')
commentButton.click()

print(driver.current_url)
