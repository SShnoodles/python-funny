# -*- coding:utf-8 -*-
import Db

def query_current_url(tag_name):
    conn, cursor = Db.connDb()
    sql = 'SELECT * FROM current_url WHERE tag_name = \'{}\''
    Db.exeQuery(cursor, sql.format(tag_name))
    result = cursor.fetchone()
    Db.connClose(conn, cursor)
    return result

def save_current_url(url, page, total_page, tag_name, error_count):
    conn, cursor = Db.connDb()
    sql = 'INSERT INTO current_url (id, url, page, total_page, tag_name, error_count) VALUES (NULL, \'{}\', {}, {}, \'{}\', {})'
    Db.exeUpdate(conn, cursor, sql.format(url, page, total_page, tag_name, error_count))
    Db.connClose(conn, cursor)

def update_current_url(url, page, total_page, tag_name, error_count, id):
    conn, cursor = Db.connDb()
    sql = 'UPDATE current_url SET url= \'{}\', page= {}, total_page= {}, tag_name= \'{}\', error_count= {} WHERE id = {};'
    Db.exeUpdate(conn, cursor, sql.format(url, page, total_page, tag_name, error_count, id))
    Db.connClose(conn, cursor)