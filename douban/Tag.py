# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import Db



class tag:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
        self.tag_url = 'https://book.douban.com/tag/'

        reload(sys)
        sys.setdefaultencoding('utf-8')

        # 初始化 tag 表
        # self.insert_table()

    @staticmethod
    def insert_table():
        conn, cursor = Db.connDb()
        Db.exeUpdate(conn, cursor, Db.tag_table_sql)
        Db.connClose(conn, cursor)

    def insert_tag(self):
        conn, cursor = Db.connDb()

        response = requests.get(self.tag_url, headers=self.headers)
        soup_html = BeautifulSoup(response.text, 'lxml')
        find_all = soup_html.find_all(class_='tagCol')
        for table in find_all:
            td_find_all = table.find_all('td')
            for td in td_find_all:
                name = td.find('a').get_text()
                href = td.find('a')['href']
                num = td.find('b').get_text()[1:-1]

                count = int(num)
                Db.exeUpdate(conn, cursor, 'INSERT INTO tag (id, name, href, num) VALUES (NULL, \'{0}\', \'{1}\', {2})'.format(name, href, count))

        Db.connClose(conn, cursor)

    def query_tag(self):
        conn, cursor = Db.connDb()
        sql = 'SELECT * FROM TAG'
        Db.exeQuery(cursor, sql)
        result = cursor.fetchall()
        Db.connClose(conn, cursor)
        return result

t = tag()
t.query_tag()