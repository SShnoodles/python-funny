# -*- coding:utf-8 -*-

from sqlalchemy import Column, String, create_engine, BigInteger, Integer, Float, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Book(Base):
    # 表的名字:
    __tablename__ = 'book'

    # 表的结构:
    id = Column(BigInteger, primary_key=True)
    img_url = Column(String)
    href = Column(String)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    translate_author = Column(String)
    press = Column(String)
    press_date = Column(String)
    price = Column(String)
    score = Column(Float)
    introduction = Column(String)
    tag_name = Column(String)


class Tag(Base):
    # 表的名字:
    __tablename__ = 'tag'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String)
    href = Column(String)
    num = Column(Integer)


# 创建session
def create_session():
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/douban?charset=utf8')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    session = DBSession()
    return session


# 具操作
def dup_book(session, tag_name):
    # book_title_list = session.execute('SELECT title From book GROUP BY title HAVING count(title) > 1').fetchall()
    book_title_list = session.query(Book.title).group_by(Book.title).having(func.count(Book.title) > 1).all()
    book_titles = []
    if book_title_list:
        for titles in book_title_list:
            book_titles.append(titles[0])
    # book_id_list = session.execute('SELECT min(id) From book GROUP BY title HAVING count(title) > 1').fetchall()
    book_id_list = session.query(func.min(Book.id)).group_by(Book.title).having(func.count(Book.title) > 1).all()
    book_ids = []
    if book_id_list:
        for ids in book_id_list:
            book_ids.append(ids[0])

    if (not book_titles) and (not book_id_list):
        print tag_name, '0'
        return
    # rows = session.execute('SELECT title FROM book WHERE title in :title AND id NOT IN :id AND tag_name = :tag_name',
    # {'title': book_titles, 'id': book_ids, 'tag_name': tag_name}).fetchall()
    book_dup_all = session.query(Book).filter(Book.title.in_(book_titles), Book.tag_name == tag_name, ~Book.id.in_(book_ids))
    if not book_dup_all.all():
        print tag_name, '0'
        return

    # 删除时不进行同步，然后再让 session 里的所有实体都过期
    book_dup = book_dup_all.delete(synchronize_session=False)
    print tag_name, book_dup

    # 提交即保存到数据库:
    session.commit()


# 执行删重
def execute_dup():
    session = create_session()
    # 查 tag
    tag_all = session.query(Tag.name).all()
    if tag_all:
        for titles in tag_all:
            dup_book(session, titles[0])

    # 关闭session:
    session.close()

if __name__ == '__main__':
    execute_dup()


