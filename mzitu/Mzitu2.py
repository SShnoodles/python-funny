# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import os
from Download import request
from pymongo import MongoClient
import sys

class mzitu:
    def __init__(self, name):
        self.down = name
        self.timeout = 3

    # request.get
    def request(self, url):
        return request.get(url, self.timeout)

    # 创建文件夹
    def mkdir(self, path):
        # 去除 /n
        path = path.strip()
        is_exists = os.path.exists(os.path.join(self.down, path))
        if not is_exists:
            print u'create dir : ' + path
            os.makedirs(os.path.join(self.down, path))
            return True
        else:
            print u'dir : ' + path + u'is exist'
            return False

    # 保存
    def save(self, img_url):
        # 截取http://i.meizitu.net/2016/11/01b20.jpg   01b20 做文件名
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    # 找到图片
    def img(self, page_url):
        # 访问每个子页面
        img_html = self.request(page_url)
        img_soup = BeautifulSoup(img_html.text, 'lxml')
        # 图片地址
        img_url = img_soup.find('div', class_='main-image').find('img')['src']
        return img_url

    def do_spider(self, all_url):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        start_html = self.request(all_url)
        Soup = BeautifulSoup(start_html.text, 'lxml')
        # 找到所有的<div class="all" > 下的 <a>
        a_list = Soup.find('div', class_='all').find_all('a')
        for a in a_list:

            # 标题 用作文件夹名
            title = a.get_text()
            # 去除标题的 非法字符
            path = str(title).replace('?', '_').replace(' ', '_')
            # 创建目录
            self.mkdir(path.decode('utf-8'))
            # 切换目录
            os.chdir(os.path.join(self.down, path.decode('utf-8')))

            # href
            href = a['href']

            html = self.request(href)
            html_soup = BeautifulSoup(html.text, 'lxml')
            # 获取最大页码
            max_span = html_soup.find_all('span')[10].get_text()

            for page in range(1, int(max_span) + 1):

                page_url = href + '/' + str(page)
                img = self.img(page_url)

                print img
                self.save(img)


Mzitu = mzitu('H:/mzitu')
Mzitu.do_spider('http://www.mzitu.com/all')