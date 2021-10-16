from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
import requests
import base64
import cv2
import numpy as np
import os
from findGap import getDistance

# 检测并反复尝试通过滑块验证
def detect_slider_verification(driver):
    while 1:
        try:
            # 找滑块
            # element = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element_by_css_selector('#app > div > main > div > div > div > div.mask > div > div.verifybox-bottom > div > div.verify-bar-area > div > div'))
            element = WebDriverWait(driver, timeout=5, poll_frequency=1).until(lambda d: d.find_element_by_css_selector('#app > div.v-application--wrap > main > div > div > div > div.mask > div > div.verifybox-bottom > div > div.verify-bar-area > div > div'))
        except:
            break
        try:
            # 找背景图
            base64_tem = driver.find_element_by_css_selector('#app > div > main > div > div > div > div.mask > div > div.verifybox-bottom > div > div.verify-img-out > div > img').get_attribute('src')
            imgdata = base64.b64decode(base64_tem.split(',')[1])
            with open('tem.png', 'wb') as f:
                f.write(imgdata)
            time.sleep(1)
            # 找图块
            base64_pat = driver.find_element_by_css_selector('#app > div > main > div > div > div > div.mask > div > div.verifybox-bottom > div > div.verify-bar-area > div > div > div > img').get_attribute('src')
            imgdata = base64.b64decode(base64_pat.split(',')[1])
            with open('pat.png', 'wb') as f:
                f.write(imgdata)
        except:
            break # 这种错是因为滑块已过，但页面没及时跳转，因此还是检测到了滑块，但紧跟着跳转后，已获取不到图片了，此时直接退出这个循环即可，开始扒下一页的图
        time.sleep(1)
        # 按住
        print(element)
        try:
            ActionChains(driver).click_and_hold(on_element=element).perform()
            # 获取距离
            distance = getDistance('./tem.png','./pat.png')
            # 位移
            ActionChains(driver).move_by_offset(xoffset=int(distance*1.35), yoffset=0).perform() # 网页上的图像大小比下载下来的大1.35倍
            time.sleep(0.5)
            # TODO: 这个可能要优化
            ActionChains(driver).release(on_element=element).perform()
            time.sleep(2)
        except:
            continue # 这种错是因为未知原因没有获取到滑块，但经观察，在这里报错时页面还在等待滑块验证，因此直接continue，重新获取一次滑块；也可能有其他原因
    return driver

# 初始化options
options = webdriver.ChromeOptions()
# 设置默认路径
out_path = r'C:\Users\ASUS\Desktop\imgs'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': out_path}
options.add_experimental_option('prefs', prefs)
# 初始化driver
driver = Chrome(options=options)
driver.maximize_window()

# 加载主页面
driver.get(url='https://bz.zzzmh.cn/index')
while 1:
    try:
        WebDriverWait(driver, timeout=5, poll_frequency=1).until(lambda d: d.find_element_by_css_selector('#app > div > main > div > div > div > div.index-tool-var > div > div:nth-child(2) > div > div > div.v-input__slot'))
        break # 能走到这儿还没抛出异常说明找到了，则退出循环
    except:
        continue # 没找到会抛出异常，此时循环继续找

# 爬第i页
def crawl_one_page(i, driver):
    print(f"第{i}页")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    if i > 1:
        # 换页
        button_ch = driver.find_element_by_css_selector('#app > div > main > div > div > div > div.text-center.pagination-bar > div > div > div > div > div > div.vue_pagination_message > input[type=text]')
        button_ch.send_keys(i)
        button_ch.send_keys(Keys.ENTER)
        time.sleep(2)
        driver = detect_slider_verification(driver)
        time.sleep(2)
    try:
        # 查是否跳转了，标志是
        element = WebDriverWait(driver, timeout=5, poll_frequency=1).until(lambda d: d.find_element_by_css_selector('#app > div > main > div > div > div > div:nth-child(2) > div:nth-child(1) > span.down-span > a'))
    except:
        print("pre-check: 第一种无")
        try:
            element = WebDriverWait(driver, timeout=5, poll_frequency=1).until(lambda d: d.find_element_by_css_selector('#app > div.v-application--wrap > main > div > div > div > div:nth-child(2) > div:nth-child(1) > span.down-span > a'))
        except:
            print("pre-check: 第二种也无")
            return
    for j in range(1, 25):
        try:
            login_btn = driver.find_element_by_css_selector(f'#app > div > main > div > div > div > div:nth-child(2) > div:nth-child({j}) > span.down-span > a')
            login_btn.click()
        except:
            print(i,j,"第一种无")
            try:
                login_btn = driver.find_element_by_css_selector(f'#app > div.v-application--wrap > main > div > div > div > div:nth-child(2) > div:nth-child({j}) > span.down-span > a')
                login_btn.click()
            except:
                print(i,j,"第二种也无, 因此判断广告")


def dynamic_change_download_dir(driver, path):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': path}}
    driver.execute("send_command", params)
    if not os.path.exists(path):
        os.makedirs(path)
    return driver

def detectCompletedDownloads():
    pass

# 选择分类
button_ch = driver.find_element_by_css_selector('#app > div > main > div > div > div > div.index-tool-var > div > div:nth-child(2) > div > div > div.v-input__slot')
button_ch.click()
time.sleep(1)
# # 选择二次元
# try:
#     button_ch = driver.find_element_by_css_selector('#list-item-130-3')
# except:
#     button_ch = driver.find_element_by_css_selector('#list-item-58-3')
# 选择人物
try:
    button_ch = driver.find_element_by_css_selector('#list-item-130-2')
except:
    button_ch = driver.find_element_by_css_selector('#list-item-58-2')
button_ch.click()

time.sleep(2)

# 爬取
for i in [246]:
    path = r'C:\Users\ASUS\Desktop\imgs\211-246\{}'.format(i)
    driver = dynamic_change_download_dir(driver, path)
    time.sleep(1)
    crawl_one_page(i, driver)
    time.sleep(4)