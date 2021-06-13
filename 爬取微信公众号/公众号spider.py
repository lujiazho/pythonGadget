# !/usr/bin/nev python
# -*-coding:utf8-*-

import tkinter as tk
from selenium import webdriver
import time, re, jsonpath, xlwt
from requests_html import HTMLSession
session = HTMLSession()


class GZHSpider(object):

    def __init__(self):
        """定义可视化窗口，并设置窗口和主题大小布局"""
        self.window = tk.Tk()
        self.window.title('公众号信息采集')
        self.window.geometry('800x600')

        """创建label_user按钮，与说明书"""
        self.label_user = tk.Label(self.window, text='需要爬取的公众号：', font=('Arial', 12), width=30, height=2)
        self.label_user.pack()
        """创建label_user关联输入"""
        self.entry_user = tk.Entry(self.window, show=None, font=('Arial', 14))
        self.entry_user.pack(after=self.label_user)

        """创建label_passwd按钮，与说明书"""
        self.label_passwd = tk.Label(self.window, text="爬取多少页：（小于100）", font=('Arial', 12), width=30, height=2)
        self.label_passwd.pack()
        """创建label_passwd关联输入"""
        self.entry_passwd = tk.Entry(self.window, show=None, font=('Arial', 14))
        self.entry_passwd.pack(after=self.label_passwd)

        """创建Text富文本框，用于按钮操作结果的展示"""
        self.text1 = tk.Text(self.window, font=('Arial', 12), width=85, height=22)
        self.text1.pack()

        """定义按钮1，绑定触发事件方法"""

        self.button_1 = tk.Button(self.window, text='爬取', font=('Arial', 12), width=10, height=1,
                                  command=self.parse_hit_click_1)
        self.button_1.pack(before=self.text1)

        """定义按钮2，绑定触发事件方法"""
        self.button_2 = tk.Button(self.window, text='清除', font=('Arial', 12), width=10, height=1,
                                  command=self.parse_hit_click_2)
        self.button_2.pack(anchor="e")


    def parse_hit_click_1(self):
        """定义触发事件1,调用main函数"""
        user_name = self.entry_user.get()
        pass_wd = int(self.entry_passwd.get())
        self.main(user_name, pass_wd)

    def parse_hit_click_2(self):
        """定义触发事件2，删除文本框中内容"""
        # self.entry_user.delete(0, "end")
        # self.entry_passwd.delete(0, "end")
        self.text1.delete("1.0", "end")

    def main(self, user_name, pass_wd):
        # 网页登录
        driver_path = r'E:\Anaconda3_files\envs\AIHUB\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.get('https://mp.weixin.qq.com/')
        time.sleep(2)
        # 网页最大化
        driver.maximize_window()
        # 拿微信扫描登录
        time.sleep(10)
        # 获得登录的cookies
        cookies_list = driver.get_cookies()
        # 转化成能用的cookie格式
        cookie = [item["name"] + "=" + item["value"] for item in cookies_list]
        cookie_str = '; '.join(item for item in cookie)
        # 请求头
        headers_1 = {
            'cookie': cookie_str,
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.77 Safari/537.36'
        }
        # 起始地址
        start_url = 'https://mp.weixin.qq.com/'
        response = session.get(start_url, headers=headers_1).content.decode()
        # 拿到token值，token值是有时效性的
        token = re.findall(r'token=(\d+)', response)[0]
        # 搜索出所有跟输入的公众号有关的
        next_url = f'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=5&query={user_name}&token=' \
                   f'{token}&lang=zh_CN&f=json&ajax=1'
        # 获取响应
        response_1 = session.get(next_url, headers=headers_1).content.decode()
        # 拿到fakeid的值，确定公众号，唯一的
        fakeid = re.findall(r'"fakeid":"(.*?)",', response_1)[0]
        # 构造公众号的url地址
        next_url_2 = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        data = {
            'action': 'list_ex',
            'begin': '0',
            'count': '5',
            'fakeid': fakeid,
            'type': '9',
            'query': '',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1'
        }
        headers_2 = {
            'cookie': cookie_str,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.77 Safari/537.36',
            'referer': f'https://mp.weixin.qq.com/cgi-bin/appmsgtemplate?action=edit&lang=zh_CN&token={token}',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-requested-with': 'XMLHttpRequest'
        }

        # 表的创建
        workbook = xlwt.Workbook(encoding='gbk', style_compression=0)
        sheet = workbook.add_sheet('test', cell_overwrite_ok=True)
        j = 1
        # 构造表头
        sheet.write(0, 0, '时间')
        sheet.write(0, 1, '标题')
        sheet.write(0, 2, '地址')
        # 循环翻页
        for i in range(pass_wd):
            data["begin"] = i * 5
            time.sleep(3)
            # 获取响应的json数据
            response_2 = session.get(next_url_2, params=data, headers=headers_2).json()
            # print(response_2)
            for per in response_2['app_msg_list']:
                if 'appmsg_album_infos' in per:
                    del per['appmsg_album_infos']
            # jsonpath 获取时间，标题，地址
            title_list = jsonpath.jsonpath(response_2, '$..title')
            # print("title_list", len(title_list))
            # print(title_list)
            url_list = jsonpath.jsonpath(response_2, '$..link')
            # print("url_list", len(url_list))
            # print(url_list)
            create_time_list = jsonpath.jsonpath(response_2, '$..create_time')
            # print("create_time_list", len(create_time_list))
            # print(create_time_list)

            # 将时间戳转化为北京时间
            list_1 = []
            for create_time in create_time_list:
                time_local = time.localtime(int(create_time))
                time_1 = time.strftime("%Y-%m-%d", time_local)
                time_2 = time.strftime("%H:%M:%S", time_local)
                time_3 = time_1 + ' ' + time_2
                list_1.append(time_3)
            # for循环遍历
            for times, title, url in zip(list_1, title_list, url_list):
                # 其中的'0-行, 0-列'指定表中的单元
                sheet.write(j, 0, times)
                sheet.write(j, 1, title)
                sheet.write(j, 2, url)
                j = j + 1
            # 窗口显示进程
            self.text1.insert("insert", f'*****************第{i+1}页爬取成功*****************')
            time.sleep(2)
            self.text1.insert("insert", '\n ')
            self.text1.insert("insert", '\n ')
        # 最后保存成功
        workbook.save(f'{user_name}公众号信息.xls')
        print(f"*********{user_name}公众号信息保存成功*********")


    def center(self):
        """创建窗口居中函数方法"""
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws / 2) - (800 / 2))
        y = int((hs / 2) - (600 / 2))
        self.window.geometry('{}x{}+{}+{}'.format(800, 600, x, y))

    def run_loop(self):
        """禁止修改窗体大小规格"""
        self.window.resizable(False, False)
        """窗口居中"""
        self.center()
        """窗口维持--持久化"""
        self.window.mainloop()


if __name__ == '__main__':
    g = GZHSpider()
    g.run_loop()


'''
{'app_msg_cnt': 255, 'app_msg_list': [
{'aid': '2247485828_1', 'album_id': '1419400457193406467', 
'appmsg_album_infos': [{'album_id': 1419400457193406467, 'appmsg_album_infos': [], 'id': '1419400457193406467', 'title': 'USC 发布'}],
 'appmsgid': 2247485828, 'checking': 0, 'copyright_type': 1, 'cover': 'https://mmbiz.qlogo.cn/mmbiz_jpg/jem9rQicR7ajKhM7g5uS5thyW992tfe6dribw1usHwfW6EMD1dP7jyKYMb8NNK4KU6AbjX7cWy5mhkR0XdWDEjSw/0?wx_fmt=jpeg', 'create_time': 1623402990, 'digest': '疫情之后，Fall21国际新生专属Next Step Checklist在这里！', 'has_red_packet_cover': 0, 'is_pay_subscribe': 0, 'item_show_type': 0, 'itemidx': 1, 'link': 'http://mp.weixin.qq.com/s?__biz=MzIxMDY2NjQ3Nw==&mid=2247485828&idx=1&sn=e7bc71ee667f0ee477c92d5fceda9702&chksm=97605f06a017d61013b516a055ae51a2454a8072ec51b5e8d98d97fc1307069978b9a2774586#rd', 'media_duration': '0:00', 'mediaapi_publish_status': 0, 'pay_album_info': {'appmsg_album_infos': []}, 'tagid': [], 'title': 'Next-Step | Fall2021 VITERBI 国际新生必看！', 'update_time': 1623402989}, 

 {'aid': '2247485816_1', 'album_id': '1419400457193406467', 
 'appmsg_album_infos': [{'album_id': 1419400457193406467, 'appmsg_album_infos': [], 'id': '1419400457193406467', 'title': 'USC 发布'}], 
 'appmsgid': 2247485816, 'checking': 0, 'copyright_type': 1, 'cover': 'https://mmbiz.qlogo.cn/mmbiz_jpg/jem9rQicR7ahBuToAmIRE0HxwtLrprKoUxQibY7G9aRkM53KvLic4gCceymTC3GExpnP57CcTsLvZllaibpGQETmOg/0?wx_fmt=jpeg', 'create_time': 1623224615, 'digest': 'Academic Webinar注册信息来咯！同学们按照自己专业所在的系选择自己的对应时间注册哦！', 'has_red_packet_cover': 0, 'is_pay_subscribe': 0, 'item_show_type': 0, 'itemidx': 1, 'link': 'http://mp.weixin.qq.com/s?__biz=MzIxMDY2NjQ3Nw==&mid=2247485816&idx=1&sn=61b7bff9e16eaeaa8be6bea66f20c643&chksm=97605ffaa017d6ecd13ee05ef62944d15b48f2692825c87e82f21ac594c6d21fde045b7f15b4#rd', 'media_duration': '0:00', 'mediaapi_publish_status': 0, 'pay_album_info': {'appmsg_album_infos': []}, 'tagid': [], 'title': '【Viterbi新生】Academic Webinar注册信息', 'update_time': 1623224615}, 

 {'aid': '2247485808_1', 'album_id': '1419400457193406467', 
 'appmsg_album_infos': [{'album_id': 1419400457193406467, 'appmsg_album_infos': [], 'id': '1419400457193406467', 'title': 'USC 发布'}], 
 'appmsgid': 2247485808, 'checking': 0, 'copyright_type': 0, 'cover': 'https://mmbiz.qlogo.cn/mmbiz_jpg/jem9rQicR7aiaE4CHZ5iajPcG9E4fMQ1n5W7mGpMIK3SKb6NLg1f4ibfUN86aHG0hYfX4YqeIy8WpDXWDdv5AQiaapA/0?wx_fmt=jpeg', 'create_time': 1622784080, 'digest': '【Viterbi研究生新生】MS Enrollment Plan and Late Arrival', 'has_red_packet_cover': 0, 'is_pay_subscribe': 0, 'item_show_type': 0, 'itemidx': 1, 'link': 'http://mp.weixin.qq.com/s?__biz=MzIxMDY2NjQ3Nw==&mid=2247485808&idx=1&sn=ee7dc1393bd16bd558abf4d06b0b5f47&chksm=97605ff2a017d6e4a6845a0d8e3e748cf0ce106da95667d90fea6618f9a5d530105b0970e54c#rd', 'media_duration': '0:00', 'mediaapi_publish_status': 0, 'pay_album_info': {'appmsg_album_infos': []}, 'tagid': [], 'title': '【Viterbi新生】研究生Enrollment Plan and Late Arrival', 'update_time': 1622784080}, 

 {'aid': '2247485798_1', 'album_id': '1428046429968547841', 
 'appmsg_album_infos': [{'album_id': 1428046429968547841, 'appmsg_album_infos': [], 'id': '1428046429968547841', 'title': 'VITERBI FAQ'}], 
 'appmsgid': 2247485798, 'checking': 0, 'copyright_type': 0, 'cover': 'https://mmbiz.qlogo.cn/mmbiz_jpg/jem9rQicR7ahR0I1LqSncMPuc9RsFwGgEibIF6rncy3bK21ic1hT8N5SjGxCEJAAdRE57xBfkWv4PRlNovNiaITJUQ/0?wx_fmt=jpeg', 'create_time': 1622536111, 'digest': 'USC VITERBI 21Fall 入学新生版本F.A.Q.', 'has_red_packet_cover': 0, 'is_pay_subscribe': 0, 'item_show_type': 0, 'itemidx': 1, 'link': 'http://mp.weixin.qq.com/s?__biz=MzIxMDY2NjQ3Nw==&mid=2247485798&idx=1&sn=a66ae6c3912ff06da191fdcb9e4013b4&chksm=97605fe4a017d6f2e4ce49c2a7ccdc10070b9a9681fa96067eb014b206b3cf0d6320ce48f4e8#rd', 'media_duration': '0:00', 'mediaapi_publish_status': 0, 'pay_album_info': {'appmsg_album_infos': []}, 'tagid': [], 'title': 'FAQ | Fall2021新生入学FAQ', 'update_time': 1622536111}, 

 {'aid': '2247485789_1', 'album_id': '1419400457193406467', 
 'appmsg_album_infos': [{'album_id': 1419400457193406467, 'appmsg_album_infos': [], 'id': '1419400457193406467', 'title': 'USC 发布'}], 
 'appmsgid': 2247485789, 'checking': 0, 'copyright_type': 0, 'cover': 'https://mmbiz.qlogo.cn/mmbiz_jpg/jem9rQicR7ahficspRPZRmqicEPtyX2YXHmRktuCicdLUumQnspO6N3MXJmqwCZyauYKvvNkiabNm48aKNfCThxxqibw/0?wx_fmt=jpeg', 'create_time': 1622446825, 'digest': '【Viterbi研究生新生】New Students Website， Passport Verification在这里哦！', 'has_red_packet_cover': 0, 'is_pay_subscribe': 0, 'item_show_type': 0, 'itemidx': 1, 'link': 'http://mp.weixin.qq.com/s?__biz=MzIxMDY2NjQ3Nw==&mid=2247485789&idx=1&sn=e47452ba6afa59646ebf16e29b864baa&chksm=97605fdfa017d6c9f9054447ba35c6c6936a2e378bdcc05f7dcc331bdeecc05385cf9078b0f7#rd', 'media_duration': '0:00', 'mediaapi_publish_status': 0, 'pay_album_info': {'appmsg_album_infos': []}, 'tagid': [], 'title': '【Viterbi Master新生】New Students Website & Passport Verification', 'update_time': 1622446825}], 'base_resp': {'err_msg': 'ok', 'ret': 0}}
'''