# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
from Tag import tag
import Db
from decimal import Decimal
import logging
import CurrentUrl

class book:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
        self.book_list_url = 'https://book.douban.com'
        # start = (page - 1) * 20
        self.book_page_url = '/tag/{0}?start={1}&type=S'
        self.tag = tag()
        self.current_page = 1
        self.current_page_total = 1
        self.error_count = 0

        self.set_log()

    @staticmethod
    def set_log():
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myapp.log',
                            filemode='w')

    def get_book(self):
        tagList = self.tag.query_tag()
        for tagObj in tagList:
            # 初始化数据
            self.current_page = 1
            self.current_page_total = 1
            self.error_count = 0
            logging.info(u'标题：' + tagObj['name'])
            self.get_book_info(tagObj['name'], tagObj['href'])

    def get_book_info(self, tag_name, url):
        logging.info(u'当前地址:' + self.book_list_url + url + '>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # 查下爬虫的历史记录
        current_url_obj = CurrentUrl.query_current_url(tag_name)
        if current_url_obj == None:
            # 没有就新增
            CurrentUrl.save_current_url(url, self.current_page, self.current_page_total, tag_name, self.error_count)
        else:
            if current_url_obj['error_count'] < 3:
                if current_url_obj['page'] > self.current_page:
                    # 大于现在的爬取位置 就从 历史开始
                    self.current_page = current_url_obj['page']
                    self.current_page_total = current_url_obj['total_page']
                    self.error_count = current_url_obj['error_count']
                    self.get_book_info(tag_name, current_url_obj['url'])
            if current_url_obj['error_count'] == 3:
                return

        if self.current_page > self.current_page_total:
            logging.warning(u'页面已到底，跳过。。。。')
            return
        time.sleep(10)

        try:
            response = requests.get(self.book_list_url + url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            li_all = soup.find(id='subject_list').find_all('li', class_='subject-item')

            # 页码
            page_all = soup.find(id='subject_list').find('div', class_='paginator').find_all('a')
            page = page_all[-2].get_text()
            self.current_page_total = int(page)

            logging.info(u'当前:' + str(self.current_page) + u'页')
            logging.info(u'一共：' + page + u'页')
            self.current_page += 1
        except BaseException, e:
            start = (self.current_page - 1) * 20
            logging.error(e)
            url = self.book_page_url.format(tag_name, start)
            # 超过 3次就 跳出
            self.error_count += 1
            if self.error_count > 3:
                logging.error(u'解析页面失败，跳过。。。。')
                return
            logging.info(
                '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            current_url_id = CurrentUrl.query_current_url(tag_name)['id']
            CurrentUrl.update_current_url(url, self.current_page, self.current_page_total, tag_name, self.error_count,
                                          current_url_id)
            self.get_book_info(tag_name, url)

        current_url_id = CurrentUrl.query_current_url(tag_name)['id']
        CurrentUrl.update_current_url(url, self.current_page, self.current_page_total, tag_name, self.error_count, current_url_id)

        try:
            for li in li_all:
                # 图
                img_url = li.find('img')['src']
                logging.info( u'图：' + img_url)
                div_info = li.find('div', class_='info')
                h2 = div_info.find('h2')
                # 书连接
                href = h2.find('a')['href']
                logging.info( u'书连接：' + href)
                # 书名
                title = h2.find('a')['title'].strip()
                logging.info( u'书名：' + title)
                # 描述 有可能空
                descc = h2.find('span')
                # desc = None if descc == None else descc.get_text()
                desc = descc and descc.get_text().replace(':', '').replace('\'', '').strip() or None
                logging.info( u'描述：' + (desc and desc or u'无'))

                # 书的 作者/译者/出版社/出版日期/价格
                infoStr = div_info.find(class_='pub').get_text().strip()
                counts = infoStr.count('/')

                # 作者
                author = ''
                # 译者 有可能空
                translate_author = ''
                # 出版社
                press = ''
                # 出版日期
                press_date = ''
                # 价格
                price = ''

                if counts == 3:
                    info = infoStr.split('/')
                    author = info[0].strip()
                    press = info[1].strip()
                    press_date = info[2].strip()
                    price = info[3].strip()
                elif counts == 4:
                    info = infoStr.split('/')
                    author = info[0].strip()
                    translate_author = info[1].strip()
                    press = info[2].strip()
                    press_date = info[3].strip()
                    price = info[4].strip()

                logging.info( u'作者：' + author)
                logging.info( u'译者：' + translate_author)
                logging.info( u'出版社：' + press)
                logging.info( u'出版日期：' + press_date)
                logging.info( u'价格：' + price)

                # 评分
                score = div_info.find('span', class_='rating_nums') and div_info.find('span', class_='rating_nums').get_text().strip() or None
                logging.info( u'评分：' + (score and score or u'无'))
                # 评分人数
                score_c = div_info.find('span', class_='pl') and div_info.find('span', class_='pl').get_text().strip() or '0'
                score_count = filter(str.isalnum, score_c.encode('utf-8'))
                logging.info(u'评分人数：' + (score_count and score_count or u'无'))

                # 简介
                introduction = div_info.find('p') and div_info.find('p').get_text().replace('\'', ' ') or None
                logging.info( u'简介：' + (introduction and introduction or u'无'))

                self.save_book(img_url, href, title, desc, author, translate_author, press, press_date, price, Decimal(score), introduction, tag_name, int(score_count))
                logging.info( '====================== ' + str(self.current_page - 1) + ' ' + tag_name + ' =======================')
        except BaseException, e:
            logging.error(e)

        start = (self.current_page - 1) * 20
        url = self.book_page_url.format(tag_name, start)
        logging.info(
            '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        self.get_book_info(tag_name, url)

    def save_book(self, *args):
        conn, cursor = Db.connDb()
        sql = 'INSERT INTO book (id, img_url, href, title, description, author, translate_author, press, press_date, price, score, introduction, tag_name, score_count) '\
            ' VALUES (NULL, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, \'{}\', \'{}\', {})'.format(
            args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10], args[11], args[12])
        Db.exeUpdate(conn, cursor, sql)
        Db.connClose(conn, cursor)


b = book()
b.get_book()
