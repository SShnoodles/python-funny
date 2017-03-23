# -*- coding:utf-8 -*-

import pymysql.cursors


tag_table_sql = 'CREATE TABLE tag (' \
    ' id int(11) NOT NULL AUTO_INCREMENT,' \
    ' name varchar(255) DEFAULT NULL,' \
    ' href varchar(255) DEFAULT NULL,'\
    ' num int(11) DEFAULT NULL,'\
    ' PRIMARY KEY (id)'\
    ') ENGINE=InnoDB DEFAULT CHARSET=utf8'

book_table_sql = 'CREATE TABLE book ('  \
    '  id int(11) NOT NULL AUTO_INCREMENT,' \
    '  img_url varchar(255) DEFAULT NULL,'  \
    '  href varchar(255) DEFAULT NULL,' \
    '  title varchar(255) DEFAULT NULL,' \
    '  desc varchar(255) DEFAULT NULL,' \
    '  author varchar(255) DEFAULT NULL,' \
    '  translate_author varchar(255) DEFAULT NULL,' \
    '  press varchar(255) DEFAULT NULL,' \
    '  press_date datetime DEFAULT NULL,' \
    '  price decimal(10,0) DEFAULT NULL,' \
    '  score varchar(255) DEFAULT NULL,' \
    '  introduction varchar(255) DEFAULT NULL,' \
    '  tag_name varchar(255) DEFAULT NULL,' \
    '  PRIMARY KEY (id)' \
    ') ENGINE=InnoDB DEFAULT CHARSET=utf8;'

def connDb():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='123456',
                           db='douban',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    return conn, cursor

# 更新语句，可执行Update，Insert语句
def exeUpdate(conn, cursor, sql):

    sta = cursor.execute(sql)

    conn.commit()

    return sta

# 查询语句
def exeQuery(cursor, sql):

    cursor.execute(sql)

    return cursor

# 关闭所有连接
def connClose(conn, cursor):

    cursor.close()

    conn.close()





